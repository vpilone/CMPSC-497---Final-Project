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
    # return tokenizer(
    #     [" ".join(x) for x in examples["question"]],
    #     padding="max_length",
    #     truncation=True,
    # )


# def group_text(examples):
#     block_size = 350
#     # Concatenate all texts.
#     concatenated_examples = {k: examples[k] for k in examples.keys()}
#     total_length = len(concatenated_examples)
#     # We drop the small remainder, we could add padding if the model supported it instead of this drop, you can
#     # customize this part to your needs.
#     if total_length >= block_size:
#         total_length = (total_length // block_size) * block_size
#     # Split by chunks of block_size.
#     result = {
#         k: [t[i : i + block_size] for i in range(0, total_length, block_size)]
#         for k, t in concatenated_examples.items()
#     }
#     result["labels"] = result["input_ids"].copy()
#     return result


# dataset = dataset.map(
#     tokenize, batched=True, remove_columns=dataset["train"].column_names
# )
dataset = dataset.map(tokenize, batched=True)
# dataset = dataset.map(group_text, batched=True)
small_train = dataset["train"].shuffle(seed=42).select(range(4))
small_test = dataset["test"].shuffle(seed=42).select(range(4))

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
    eval_strategy="epoch",
    save_strategy="epoch",
    # save_strategy="best",
    overwrite_output_dir=True,
    fp16_full_eval=True,
    logging_strategy="epoch",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
)
trainer = Trainer(
    model=originalModel,
    args=training_args,
    train_dataset=small_train,
    eval_dataset=small_test,
    data_collator=data_collector,
    # compute_metrics=compute_metrics,
)

trainer.train()
