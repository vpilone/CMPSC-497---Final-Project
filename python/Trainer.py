import torch._dynamo.config
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    BitsAndBytesConfig,
    DataCollatorForLanguageModeling,
)
from datasets import load_dataset
import numpy as np
import evaluate
import bitsandbytes

torch._dynamo.config.suppress_errors = True

modelname = "Qwen/Qwen2.5-1.5B"

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-1.5B")

dataset = load_dataset(
    "csv",
    data_files={
        "train": "/Users/vpilone/Documents/Classes SP25/CMPSC 497/Final Project/python/databaseTrain.csv",
        "test": "/Users/vpilone/Documents/Classes SP25/CMPSC 497/Final Project/python/databaseTest.csv",
    },
)


def tokenize(examples):
    return tokenizer(
        examples["question"], padding="max_length", truncation=True, max_length=300
    )


dataset = dataset.map(tokenize, batched=True)

small_train = dataset["train"].shuffle(seed=42).select(range(100))
small_test = dataset["test"].shuffle(seed=42).select(range(100))

print(dataset)

originalModel = AutoModelForCausalLM.from_pretrained(modelname)

metric = evaluate.load("mtzig/cross_entropy_loss")

tokenizer.pad_token = tokenizer.eos_token
data_collector = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)


def compute_metrics(eval_pred):
    predictions, references = eval_pred
    return metric.compute(predictions=predictions, references=references, lang="en")


training_args = TrainingArguments(
    output_dir="/Users/vpilone/Documents/Classes SP25/CMPSC 497/Final Project/python/trainedModel",
    eval_strategy="steps",
    save_strategy="best",
    overwrite_output_dir=True,
    fp16_full_eval=True,
    logging_strategy="epoch",
    num_train_epochs=2,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    metric_for_best_model="loss",
    eval_steps=0.1,
)
trainer = Trainer(
    model=originalModel,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    data_collator=data_collector,
)

trainer.train()
