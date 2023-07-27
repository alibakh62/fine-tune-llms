# fine-tune-llms
In this repository, we try two different methods to fine-tune an LLM model.

## 1. Fine-tuning with using peft and SFTTrainer
As you can see in the `train.py`, we're using the `tatsu-lab/alpaca` dataset from HuggingFace Datasets. It's an instruction dataset and we're using this data to fine-tune the Salesforce base LLM, i.e. XGen. We're using the `peft` and `SFTTrainer` to fine-tune the model. 

## 2. Fine-tuning using the `auto-train` library from HuggingFace
A simpler way to fine-tune the model is to use the `auto-train` library from HuggingFace. This way, we don't need to write any code. You can find an example implementation below:

```bash
autotrain llm --train --project_name output --model Salesforce/xgen-7b-8k-base --data_path tatsu-lab/alpaca --use_peft --use_int4 --trainer sft --learning_rate 2e-4 
```

