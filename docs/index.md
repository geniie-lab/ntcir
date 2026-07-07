# Welcome to NTCIR Agentic Instruction Task

!!! note "Stay in touch"
    - Follow [@agenticinstruct](https://x.com/agenticinstruct) for latest updates
    - Join our [Discord server](http://discord.gg/zvXkNKtEGa) for quick questions and chats
    - Email Task organiser for any enquiries: `agenticinstruction-org at googlegroups dot com`

!!! abstract "What is Agentic Instruction Task?"
    > Agentic Instruction Task seeks to identify effective and robust instructions for guiding Large Language Models (LLMs) in search agent roles. Participants are invited to submit instructions and generation methods covering four key search stages: query formulation, document selection (clicks), relevance judgment, and query reformulation. AgenticInstruction-1 centers on a high-recall Ad Hoc retrieval scenario in both Japanese and English. Developed instructions will be evaluated in an iterative search setting, with performance measured at the session level. The task aims to establish best practices for instruction design in agentic search applications.

    :point_right: Please look at our slides and video of [NTCIR-19 kick-off event](https://research.nii.ac.jp/ntcir/ntcir-19/kickoffcfp.html#kickoff-resources) to learn more about the task.

!!! warning "Notable changes from the kick-off event"
    - Use of docker image was cancelled due to technical/license issues
    - Only `gpt-oss-120b` will be used as an official LLM in NTCIR-19.
        - Participants are welcome to test other LLMs as additional analyses and report your findings in the participant paper.
    - Only BM25 and Sparse Encoder will be used as official IR models in NTCIR-19.
        - Participants are welcome to index the dataset with other models as additional analyses and report your findings in the participant paper.

!!! tip "Three steps to successful participation"
    1. [Getting Started with the datasets and tools](getting-started.md)
    1. [Follow Task Description](task-description.md)
    1. [Submit Runs](run-submission.md)

!!! success "Important Dates"
    :warning: Some schedule is differernt from NTCIR-19 official one.

    |Date|Event/Task|Role|
    |:--|:--|:--:|
    |July 10th, 2026|Task registration due|Participant|
    |August 10th, 2026|Run submission due|Participant|
    |September 1st, 2026|Evaluation results release|Organiser|
    ||Task overview paper (draft) release|Organiser|
    |October 1st, 2026|Participant paper (complete-ish draft) due|Participant|
    |October 15th, 2026|Review feedback on participant paper release|Organiser|
    |November 1st, 2026|Participant paper (camera-ready) due|Participant|
    |December 8-10th, 2026|NTCIR-19 Conference (NII, Tokyo, Japan)|All|
