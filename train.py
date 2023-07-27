import torch
from datasets import load_dataset
from peft import LoraConfig, get_peft_model, prepare_model_for_int8_training
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from trl import SFTTrainer


def train():
    train_dataset = load_dataset("tatsu-lab/alpaca", split="train")
    tokenizer = AutoTokenizer.from_pretrained(
        "Salesforce/xgen-7b-8k-base",
        trust_remote_code=True,
    )
    tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        "Salesforce/xgen-7b-8k-base",
        load_in_4bit=True,
        # torch_dtype=torch.float16,
        device_map="auto",
    )
    model.resize_token_embeddings(len(tokenizer))
    model = prepare_model_for_int8_training(model)
    peft_config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="causal_lm",
    )
    model = get_peft_model(model, peft_config)

    training_args = TrainingArguments(
        output_dir="./xgen-7b-tuned-alpaca-l1",
        overwrite_output_dir=True,
        per_device_train_batch_size=4,
        optim="adamw_torch",
        learning_rate=2e-4,
        warmup_ratio=0.1,
        lr_scheduler_type="linear",
        num_train_epochs=1,
        save_strategy="epoch",
        logging_dir="./logs",
        logging_steps=100,
        fp16=True,
    )

    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        tokenizer=tokenizer,
        dataset_text_field="text",
        max_seq_length=1024,
        packing=True,
        peft_config=peft_config,
    )

    trainer.train()
    trainer.save_model()
    # trainer.push_to_hub()


if __name__ == "__main__":
    train()
