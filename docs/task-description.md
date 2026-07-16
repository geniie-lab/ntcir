# Task Description for NTCIR-19

!!! bug ""
    :construction: Under Construction. Stay Tuned.

!!! warning "Important Rules"

    - All development, training, and testing must be done on `train/dev` datasets
    - You cannot change/train/test your instruction method using `test` datasets
    - You cannot use qrels data of `test` datasets
    - You must generate log files using `test` datasets for [run submission](run-submission.md)
    - You cannot edit the generated log files except session names

## Fixed parameters

:bulb: Don't change these parameters in your experiment.


## Customisable parameters

:bulb: This is your design space to explore.

## Advanced instructions

:bulb: Tips for hacking `geniie-lab` code base to achieve advanced method of generating instructions.


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