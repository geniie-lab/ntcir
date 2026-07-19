# Third-party libraries
import importlib
import json
import os
import sys
import traceback
import ir_datasets
import ir_measures
from datetime import datetime
from dotenv import load_dotenv
from contextlib import redirect_stdout, redirect_stderr

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Local application imports
from geniie_lab.dataclasses.description import (
    CorpusDescription,
    ModelDescription,
    TaskDescription,
    ToolDescription,
    TopicDescription,
)
from geniie_lab.dataclasses.topic import (
    TitleDescriptionNarrativeTopic, FullTopic,
    TitleDescriptionTopic,
    TitleNarrativeTopic,
    TitleOnlyTopic
)
from geniie_lab.dataclasses.setting import ExperimentSettings, StageConfig
from geniie_lab.experiments.session_experiment import ExperimentRunner

load_dotenv()

my_settings = ExperimentSettings(
    name="my_session_experiment",
    task=TaskDescription(
        name="High-Recall Retrieval",
        description="Find as many different relevant documents as possible for a given search topic from a given document collection using a provided search tool.",
        measurement=[ir_measures.nDCG@10, ir_measures.MRR@10],
        start_offset=0,
        serp_size=10
    ),
    topicset=TopicDescription(
        name="disks45/nocr/trec-robust-2004/fold1",
        # name="disks45/nocr/trec-robust-2004/fold2",
        # name="aquaint/trec-robust-2005",
        # name="ntcir1-adhoc",
        # name="ntcir2-adhoc",
        type="ir_datasets",
        topic_class=FullTopic
    ),
    corpus=CorpusDescription(
        name="Disk45",
        description="A document collection of about 528,000 English news documents. Sources include the Financial Times (1991-1994), the Federal Register (1994), the Foreign Broadcast Information Service (1996), and the Los Angeles Times (1989-1990).",
        index_name="trec_robust_2004_bm25",
        # index_name="trec_robust_2004_splade",
    ),
    # corpus=CorpusDescription(
    #     name="Aquaint",
    #     description="A document collection of about 1M English newswire text. Sources include the Xinhua News Service (1996-2000), the New York Times News Service (1998-2000), and the Associated Press Worldstream News Service (1998-2000).",
    #     index_name="trec_robust_2005_bm25",
    #     # index_name="trec_robust_2005_splade",
    # ),
    # corpus=CorpusDescription(
    #     name="NTCIR1",
    #     description="A collection of about 340,000 Japanese academic documents. Sources include author abstracts of academic conference papers hosted by 65 Japanese academic societies (1988-1997).",
    #     index_name="ntcir1_bm25",
    #     # index_name="ntcir1_splade",
    # ),
    # corpus=CorpusDescription(
    #     name="NTCIR2",
    #     description="A collection of about 736,000 Japanese academic documents. Sources include author abstracts of academic conference papers hosted by Japanese academic societies (1997-1999) and extended summaries of grant reports (1986-1997).",
    #     index_name="ntcir2_bm25",
    #     # index_name="ntcir2_splade",
    # ),
    models=[
        ModelDescription(
            type="bedrock",
            name="openai.gpt-oss-120b",
            token_length=128000,  # set to your model's max input token length
            system_prompt="You're a helpful assistant",
            temperature=0.0,
            top_p=1.0,
        )
    ],
    tools=[
        ToolDescription(
            name="opensearch",
            ranking_model="bm25",
            index_name="trec_robust_2004_bm25", # Set your choice of index name
            host=os.getenv("OPENSEARCH_HOST"),
            port=9200,
            description="It allows you to perform searches using keywords only and employs the BM25 ranking model to order results.",
        ),
        # ToolDescription(
        #     name="opensearch",
        #     ranking_model="splade",
        #     encode_model="opensearch-project/opensearch-neural-sparse-encoding-multilingual-v1",
        #     index_name="[index_name]",
        #     host=os.getenv("OPENSEARCH_HOST"),
        #     port=9200,
        #     description="It allows you to perform searches using keywords only and employs a sparse encoder model to order results.",
        # ),
    ],
    stages={
        "query": StageConfig(
            instruction="""
                Review the provided descriptions of task, corpus, tool and search topic. Then, formulate a search query.
            """,
        ),
        "ranking": StageConfig(
            instruction=""
        ),
        "click": StageConfig(
            instruction="""
                Select a set of documents that are likely to contain relevant information to the search topic. Return an empty list if none of the results appears relevant.
            """,
        ),
        "relevance": StageConfig(
            instruction="""
                Evaluate the relevance of the document based on the search topic description and its narrative.
            """,
        ),
        "reformulate": StageConfig(
            instruction="""
                Formulate another search query to find new relevant documents.
            """,
        ),
    },

    # plan=["query"],
    plan=["query", "ranking"],
    # plan=["query", "ranking", "click"],
    # plan=["query", "ranking", "click", "relevance"],
    # plan=["query", "ranking", "click", "relevance"] + ["reformulate", "ranking", "click", "relevance"],
    # plan=["query", "ranking", "click", "relevance"] + ["reformulate", "ranking", "click", "relevance"] * 2,
    # plan=["query", "ranking", "click", "relevance"] + ["reformulate", "ranking", "click", "relevance"] * 3,
    # plan=["query", "ranking", "click", "relevance"] + ["reformulate", "ranking", "click", "relevance"] * 4,

    topic_ids="1:1",
    full_log=False
)

# The NTCIR datasets are custom ir_datasets loaders: importing the module
# registers the dataset name. Download the loader files (e.g. ntcir1_adhoc.py
# and ntcir1-adhoc.yaml) from geniie-backend into this scripts folder first;
# see the dataset table in Getting Started.
if my_settings.topicset.name.startswith("ntcir"):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    importlib.import_module(my_settings.topicset.name.replace("-", "_"))

def report_topic_statistics(jsonl_path):
    """Print per-topic statistics from a session log file:
    - unique relevant documents: clicked by the LLM, judged relevant by the
      LLM, and labeled relevant in the official qrels (see Task Description)
    - recall: unique relevant documents found / all relevant documents in the
      official qrels for the topic
    - total tokens sent to and produced by the LLM across all stages
    - total time in seconds, from the first to the last record of the topic
      (the first stage's LLM call happens before the first record is written,
      so its latency is not included)
    - per-iteration progression of the cumulative unique relevant documents
      (an iteration starts at each query/reformulation stage), plus an
      aggregate progression table to show where improvements level off
    """
    topics = {}
    dataset_names = set()
    with open(jsonl_path, encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            dataset_names.add(record["dataset"])
            stats = topics.setdefault(
                record["topic_id"],
                {"iterations": [], "total_tokens": 0, "timestamps": []}
            )
            if record.get("stage") in ("query", "reformulation") or not stats["iterations"]:
                stats["iterations"].append({"relevant_docids": set(), "tokens": 0})
            iteration = stats["iterations"][-1]
            tokens = record.get("total_token") or 0
            stats["total_tokens"] += tokens
            iteration["tokens"] += tokens
            stats["timestamps"].append(datetime.fromisoformat(record["created_at"]))
            if (record.get("stage") == "rel_judge"
                    and record.get("label") == "Relevance.RELEVANT"
                    and record.get("qrel_label", 0) >= 1):
                iteration["relevant_docids"].add(record["docid"])

    # Total relevant documents per topic from the official qrels
    total_relevant = {}
    for name in dataset_names:
        dataset = ir_datasets.load(name)
        if callable(dataset):
            dataset = dataset()
        for row in dataset.qrels_iter():
            if row.query_id in topics and row.relevance >= 1:
                total_relevant[row.query_id] = total_relevant.get(row.query_id, 0) + 1

    # Per-topic summary with the cumulative progression of unique rel docs
    print(f"\n{'Topic':<10}{'Unique rel docs':>17}{'Recall':>10}"
          f"{'Total tokens':>15}{'Total time (s)':>17}  Progression")
    for topic_id, stats in topics.items():
        seen, cumulative = set(), []
        for iteration in stats["iterations"]:
            seen |= iteration["relevant_docids"]
            cumulative.append(len(seen))
        available = total_relevant.get(topic_id, 0)
        recall = len(seen) / available if available else 0.0
        seconds = (max(stats["timestamps"]) - min(stats["timestamps"])).total_seconds()
        progression = "→".join(str(n) for n in cumulative)
        print(f"{topic_id:<10}{len(seen):>17}{recall:>10.3f}"
              f"{stats['total_tokens']:>15}{seconds:>17.1f}  {progression}")

    # Aggregate progression across topics: where do improvements stop?
    max_iterations = max((len(s["iterations"]) for s in topics.values()), default=0)
    if max_iterations > 1:
        print(f"\n{'Iteration':<10}{'Topics':>7}{'New rel docs':>14}"
              f"{'Cum rel docs':>14}{'Cum recall':>12}{'Tokens':>12}")
        for index in range(max_iterations):
            reached = [t for t, s in topics.items() if len(s["iterations"]) > index]
            new_docs = cum_docs = cum_recall = tokens = 0
            for topic_id in reached:
                iterations = topics[topic_id]["iterations"]
                before = set().union(*(i["relevant_docids"] for i in iterations[:index])) if index else set()
                after = before | iterations[index]["relevant_docids"]
                new_docs += len(after) - len(before)
                cum_docs += len(after)
                available = total_relevant.get(topic_id, 0)
                cum_recall += len(after) / available if available else 0.0
                tokens += iterations[index]["tokens"]
            n = len(reached)
            print(f"{index + 1:<10}{n:>7}{new_docs / n:>14.2f}"
                  f"{cum_docs / n:>14.2f}{cum_recall / n:>12.3f}{tokens / n:>12.0f}")


if __name__ == "__main__":

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    base_dir = "./logs"
    stdout_path = f"{base_dir}/{my_settings.name}_{timestamp}.jsonl"
    stderr_path = f"{base_dir}/{my_settings.name}_{timestamp}.log"

    runner = ExperimentRunner(settings=my_settings)
    with open(stdout_path, "w", encoding="utf-8") as fout, \
        open(stderr_path, "w", encoding="utf-8") as ferr:
        with redirect_stdout(fout), redirect_stderr(ferr):
            try:
                runner.run()
            except Exception:
                traceback.print_exc()   # lands in the .log via the redirect
                raise                   # still fail loudly on the console with exit code

    report_topic_statistics(stdout_path)
