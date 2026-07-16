# Task Description for NTCIR-19

!!! bug ""
    :construction: Under Construction. Stay Tuned.

!!! warning "Important Rules"

    - All development, training, and testing must be done on `train/dev` datasets
    - You cannot change/train/test your instruction method using `test` datasets
    - You cannot use qrels data of `test` datasets
    - You must generate log files using `test` datasets for [run submission](run-submission.md)
    - You cannot edit the generated log files except session names

## Customisable parameters

:bulb: This is your design space to explore. Making changes to any of these parameters could potentially change the output of a LLM-based search agent.

## Index names

- You need to select an index name that matches your selection of dataset and IR model.

=== "English"

    |Index name|Dataset|IR Model|
    |:--|:--|:--|
    |robust_2004_bm25|Robust 2004|BM25|
    |robust_2004_splade|Robust 2004|Sparse Encoder|
    |robust_2005_bm25|Robust 2005|BM25|
    |robust_2005_splade|Robust 2005|Sparse Encoder|

=== "Japanese"

    |Index name|Dataset|IR Model|
    |:--|:--|:--|
    |ntcir1_adhoc_bm25|NTCIR-1 AdHoc|BM25|
    |ntcir1_adhoc_splade|NTCIR-1 AdHoc|Sparse Encoder|
    |ntcir2_adhoc_bm25|NTCIR-2 AdHoc|BM25|
    |ntcir2_adhoc_splade|NTCIR-2 AdHoc|Sparse Encoder|

## Fixed parameters

:bulb: Don't change these parameters in your experiment.

=== "Task Description"

    ```python
    task=TaskDescription(
        name="High-Recall Retrieval",
        description="Find as many different relevant documents as possible for a given search topic from a given document collection using a provided search tool.",
        measurement=[ir_measures.nDCG@10, ir_measures.Recall@10],
        start_offset=0,
        serp_size=10,
    )
    ```

=== "Corpus Description"

    ```python
    # Robust 2004 (Train/Dev)
    corpus=CorpusDescription(
        name="Aquaint",
        description="A document collection of about 1M English newswire text. Sources include the Xinhua News Service (1996-2000), the New York Times News Service (1998-2000), and the Associated Press Worldstream News Service (1998-2000).",
        index_name="[index name]",
    )
    # Robust 2005 (Test)
    corpus=CorpusDescription(
        name="Aquaint",
        description="A document collection of about 1M English newswire text. Sources include the Xinhua News Service (1996-2000), the New York Times News Service (1998-2000), and the Associated Press Worldstream News Service (1998-2000).",
        index_name="[index name]",
    )
    # NTCIR-1 AdHoc (Train/Dev)
    corpus=CorpusDescription(
        name="Aquaint",
        description="A document collection of about 1M English newswire text. Sources include the Xinhua News Service (1996-2000), the New York Times News Service (1998-2000), and the Associated Press Worldstream News Service (1998-2000).",
        index_name="[index name]",
    )
    # NTCIR-3 AdHoc (Test)
    corpus=CorpusDescription(
        name="Aquaint",
        description="A document collection of about 1M English newswire text. Sources include the Xinhua News Service (1996-2000), the New York Times News Service (1998-2000), and the Associated Press Worldstream News Service (1998-2000).",
        index_name="[index name]",
    )
    ```

## How to change IR model

=== "BM25"

    ```python
    tools=[
        ToolDescription(
            name="opensearch",
            ranking_model="bm25",
            index_name="[index name]",
            host=os.getenv("OPENSEARCH_HOST"),
            port=9200,
            description="It allows you to perform searches using keywords only and employs the BM25 ranking model to order results.",
        )
    ]
    ```

=== "Sparse Encoder"

    ```python
    tools=[
        ToolDescription(
            name="opensearch",
            ranking_model="splade",
            index_name="[index name]",
            host=os.getenv("OPENSEARCH_HOST"),
            port=9200,
            description="It allows you to perform searches using keywords only and employs a sparse encoder ranking model to order results.",
        )
    ]
    ```

## How to change datasets

=== "TREC Robust 2004 (Fold 1/2)"

    ```python
    topicset=TopicDescription(
        name="disks45/nocr/trec-robust-2004/fold1",
        # name="disks45/nocr/trec-robust-2004/fold2",
        type="ir_datasets",
        topic_class=FullTopic
    )
    ...
    corpus=CorpusDescription(
        name="Aquaint",
        description="A document collection of about 1M English newswire text. Sources include the Xinhua News Service (1996-2000), the New York Times News Service (1998-2000), and the Associated Press Worldstream News Service (1998-2000).",
        index_name="[index name]",
    )
    ```

=== "TREC Robust 2005"

    ```python
    topicset=TopicDescription(
        name="aquaint/trec-robust-2005",
        type="ir_datasets",
        topic_class=FullTopic
    )
    ...
    corpus=CorpusDescription(
        name="Aquaint",
        description="A document collection of about 1M English newswire text. Sources include the Xinhua News Service (1996-2000), the New York Times News Service (1998-2000), and the Associated Press Worldstream News Service (1998-2000).",
        index_name="[index name]",
    )
    ```

=== "NTCIR-1 AdHoc"

    ```python
    topicset=TopicDescription(
        name="ntcir1_adhoc",
        type="ir_datasets",
        topic_class=FullTopic
    )
    ...
    corpus=CorpusDescription(
        name="Aquaint",
        description="A document collection of about 1M English newswire text. Sources include the Xinhua News Service (1996-2000), the New York Times News Service (1998-2000), and the Associated Press Worldstream News Service (1998-2000).",
        index_name="[index name]",
    )
    ```


=== "NTCIR-2 AdHoc"

    ```python
    topicset=TopicDescription(
        name="ntcir2_adhoc",
        type="ir_datasets",
        topic_class=FullTopic
    )
    ...
    corpus=CorpusDescription(
        name="Aquaint",
        description="A document collection of about 1M English newswire text. Sources include the Xinhua News Service (1996-2000), the New York Times News Service (1998-2000), and the Associated Press Worldstream News Service (1998-2000).",
        index_name="[index name]",
    )
    ```

## Advanced instructions

:bulb: Tips for hacking `geniie-lab` code base to achieve advanced method of generating instructions.

:bulb: You might need to re-run `python -m pip install -e .` to activate the change.

=== "Instruction template"

    - See `https://github.com/geniie-lab/geniie-lab/blob/dev/geniie_lab/dataclasses/instruction.py`
    - Example of template for query formulation

    ```python
        instruction = f"""
            **Instruction**:
            {self.instruction}
            ============================
            **Task Description**: {self.task.description}
            **Corpus Description**: {self.corpus.description}
            **Search Tool Description**: {self.tool.description}
            **Topic Description**: {self.topic}
        """
    ```

=== "Description of structured output"

    - See `https://github.com/geniie-lab/geniie-lab/blob/dev/geniie_lab/response.py`
    - Example of descriptions in Query output

    ```python
    class Query(BaseModel):
        """A model for submitting a query to a search tool."""
        query: str = Field(
            ...,
            title="query",
            description="The query string submitted to the search tool."
        )
        start: int = Field(
            0,
            title="start",
            description=(
                "The starting index of the search results. Defaults to 0. "
            )
        )
        size: int = Field(
            10,
            title="size",
            description=(
                "The number of documents per search result page. Defaults to 10. "
            )
        )
        reason: str = Field(
            ...,
            title="reason",
            description="A brief explanation of the intent behind your query."
        )
    ```

## FAQ

??? question "Can I use a locally deployed gpt-oss-120b?"

    Yes. `geniie-lab` supports ollama and vllm for local models. See `Model Description` of [Common settings](https://github.com/geniie-lab/geniie-lab/blob/dev/docs/experiments/common_settings.md)

??? question "How can I resume my experiment from a failed topic?"

    If you have a total of 50 topics, and your experiment stopped at `N`th topic, then

    > `topic_ids="N:50"`

    allows you to resume the experiment from `N`th topic.

??? question "What should I do when LLM failed on the same topic multiple times?"

    - Based on my experience, submitting the same instruction (prompts) will eventually get through to generate valid responses, without changing any parameters.
    - Sometimes, you might need to try several times.
    - However, if the problem persists, you can relax the `temperature` and `top_p` parameters **only for those problematic topics**, to maximise the reproducibility of experimental results.

    ```python
    models=[
        ModelDescription(
            ...,
            temperature=0.7,
            top_p=0.95
        )
    ]
    ```

!!! question "Need help?"

    Contact us via [Discord server](http://discord.gg/zvXkNKtEGa) or email `agenticinstruction-org at googlegroups dot com`.