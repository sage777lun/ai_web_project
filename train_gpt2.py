import json
import torch
from datasets import Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer

model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)

# **解決 GPT-2 的填充問題**
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(model_name)

def load_data():
    with open("dialogue_data.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    inputs = tokenizer([d["input"] for d in data], padding="max_length", truncation=True, max_length=50, return_tensors="pt")
    labels = tokenizer([d["output"] for d in data], padding="max_length", truncation=True, max_length=50, return_tensors="pt")

    dataset = Dataset.from_dict({"input_ids": inputs["input_ids"], "labels": labels["input_ids"]})
    return dataset

train_dataset = load_data()

training_args = TrainingArguments(
    output_dir="./gpt2-finetuned",
    per_device_train_batch_size=4,  # ✅ 增加訓練批次，提高學習速度
    num_train_epochs=20,  # ✅ 增加訓練週期
    save_strategy="epoch",
    logging_dir="./logs"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset
)

trainer.train()
model.save_pretrained("./gpt2-finetuned")
print("✅ GPT-2 微調完成！")