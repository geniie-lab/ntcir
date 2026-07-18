# FAQ

??? question "How did you index the document collection?"

    - We used an out-of-the-box version of [OpenSearch (ver. 3.5.0)](https://hub.docker.com/r/opensearchproject/opensearch/tags?name=3.5.0) to index documents.
    - For sparse encoding, we used [opensearch-project/opensearch-neural-sparse-encoding-multilingual-v1](https://huggingface.co/opensearch-project/opensearch-neural-sparse-encoding-multilingual-v1) for English and Japanese.
    - See [indexing](https://github.com/geniie-lab/geniie-backend/blob/dev/indexing/opensearch/README.md) and [model hosting](https://github.com/geniie-lab/geniie-backend/blob/dev/model_hosting/README.md) for replicating our environment.

??? question "Can I use a locally deployed gpt-oss-120b?"

    Yes. `geniie-lab` supports ollama and vllm for local models. See `Model Description` of [Common settings](https://github.com/geniie-lab/geniie-lab/blob/dev/docs/experiments/common_settings.md)

??? question "How can I resume my experiment from a particular topic?"

    If you have a total of 50 topics, and your experiment stopped at `N`th topic, then

    > `topic_ids="N:50"`

    allows you to resume the experiment from `N`th topic.

??? question "What should I do when experiments failed on the same topic multiple times?"

    - In most cases, submitting the same instruction (prompts) will eventually get through to generate valid responses, without changing any parameters.
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

??? question "How can I see the exact transaction between the LLM and `geniie-lab`?"

    Set `full_log=True`

??? question "How much will Amazon Bedrock usage cost?"

    - `gpt-oss-120b` on Amazon Bedrock is priced at $0.15 per million input tokens and $0.60 per million output tokens (check the current prices at [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing/)).
    - The pilot experiment in [Getting Started](getting-started.md) costs well under $0.01.
    - A full session of five iterations uses roughly 0.4-0.6M tokens per topic, so one 50-topic experiment is approximately 25M tokens, or **about $5**.
    - One run (BM25 + Sparse Encoder) is roughly $10-15; a full participation of three runs in both languages, including development overhead, is on the order of $60-90.

!!! question "Not finding answers?"

    Contact us via [Discord server](http://discord.gg/zvXkNKtEGa) or email `agenticinstruction-org at googlegroups dot com`.