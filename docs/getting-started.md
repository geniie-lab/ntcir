# How to get started with Agentic Instruction Task

1. [Register to NTCIR-19](https://research.nii.ac.jp/ntcir/ntcir-19/howto.html) and select `AgenticInstruction` as participating task
1. Decide which language(s) to participate (English only, Japanese only, or both)
1. Obtain a copy of datasets based on your language choice.
    - We suggest to start with train/dev datasets first.

    |Language|Set|Dataset|
    |:--|:--|:--|
    |English|Train/Dev|[TREC Robust 2004 with disk45/nocr](https://ir-datasets.com/disks45.html)|
    |English|Test|[TREC Robust 2005 with Aquaint](https://ir-datasets.com/aquaint.html)<br/>:bulb: Not free. Obtain the test set only when you decide to submit a run.|
    |Japanese|Train/Dev|[NTCIR-1 (IR and Term Extraction/Role Analysis Test Collections)](https://research.nii.ac.jp/ntcir/permission/perm-en.html#ntcir-1)|
    |Japanese|Test|[NTCIR-2 (IR Test Collection)](https://research.nii.ac.jp/ntcir/permission/perm-en.html#ntcir-2)<br/>:bulb: Obtain the test set only when you decide to submit a run.|

1. Run preprocessing notebooks to access datasets using `ir_datasets`

    |Language|Set|Notebook/Notes|
    |:--|:--|:--|
    |English|Train/Dev|[TREC Robust 2004 with disk45/nocr](https://github.com/geniie-lab/geniie-backend/blob/dev/dataset/trec-robust-2004/)<br/>:bulb: Use `disks45/nocr/trec-robust-2004/fold1` and `disks45/nocr/trec-robust-2004/fold2` as training.|
    |English|Test|[TREC Robust 2005 with Aquaint](https://github.com/geniie-lab/geniie-backend/blob/dev/dataset/trec-robust-2005/)|
    |Japanese|Train/Dev|[NTCIR-1 (IR and Term Extraction/Role Analysis Test Collections)](https://github.com/geniie-lab/geniie-backend/tree/dev/dataset/ntcir1-adhoc)<br/>:bulb: You need to download `ntcir1-adhoc.yaml` and `ntcir1_adhoc.py` to the same folder as the notebook.|
    |Japanese|Test|[NTCIR-2 (IR Test Collection)](https://github.com/geniie-lab/geniie-backend/tree/dev/dataset/ntcir2-adhoc)<br/>:bulb: You need to download `ntcir2-adhoc.yaml` and `ntcir2_adhoc.py` to the same folder as the notebook.|

1. Obtain a free API key from [groq](https://groq.com/)
    - Participants are expected to purchase additional API credits to complete experiments.

1. Clone the `dev` branch of [geniie-lab](https://github.com/geniie-lab/geniie-lab/tree/dev) repo
    - Set the environmental variables in `.env` file at the root of the repo folder
    - :bulb: Note that each registered group has its own username/password
        ```bash
        OPENSEARCH_HOST="[Contact the organiser to obtain the URL]"
        OPENSEARCH_ADMIN_USER="[Contact the organiser to obtain your username]"
        OPENSEARCH_ADMIN_PASS="[Contact the organiser to obtain your password]"
        GROQ_API_KEY="[your groq api key]"
        ```
    - Locate `scripts\run_session_experiment_ntcir19.py` and
        - Run the script to conduct a pilot experiment.
        - Check `logs` folder for outputs.
            - `.jsonl` is the search log file of experiments
            - `.log` is the error/warning log file for reference
    - Read the [documentation](https://github.com/geniie-lab/geniie-lab/blob/dev/docs/index.md) as needed

1. You're ready to go. Move on to [Task Description](task-description.md)

!!! question "Questions?"

    Contact us via [Discord server](http://discord.gg/zvXkNKtEGa) or email `agenticinstruction-org at googlegroups dot com`.
