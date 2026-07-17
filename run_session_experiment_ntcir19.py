# Third-party libraries
import os
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
        # name="ntcir1_adhoc",
        # name="ntcir2_adhoc",
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
            type="groq",
            name="openai/gpt-oss-120b",
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
            index_name="[index_name]",
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
    # plan=["query", "ranking"],
    # plan=["query", "ranking", "click"],
    plan=["query", "ranking", "click", "relevance"],
    # plan=["query", "ranking", "click", "relevance"] + ["reformulate", "ranking", "click", "relevance"],
    # plan=["query", "ranking", "click", "relevance"] + ["reformulate", "ranking", "click", "relevance"] * 2,
    # plan=["query", "ranking", "click", "relevance"] + ["reformulate", "ranking", "click", "relevance"] * 3,
    # plan=["query", "ranking", "click", "relevance"] + ["reformulate", "ranking", "click", "relevance"] * 4,

    topic_ids="1:1",
    full_log=False
)

if __name__ == "__main__":

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    base_dir = "../logs"
    stdout_path = f"{base_dir}/{my_settings.name}_{timestamp}.jsonl"
    stderr_path = f"{base_dir}/{my_settings.name}_{timestamp}.log"

    runner = ExperimentRunner(settings=my_settings)
    with open(stdout_path, "w", encoding="utf-8") as fout, \
        open(stderr_path, "w", encoding="utf-8") as ferr:
        with redirect_stdout(fout), redirect_stderr(ferr):
            runner.run()
