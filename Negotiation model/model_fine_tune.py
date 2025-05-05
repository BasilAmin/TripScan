import json
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    DataCollatorForLanguageModeling,
    Trainer,
    BitsAndBytesConfig
)
from datasets import load_dataset

# ──────────────────────────────────────────────────────────────────────────────
# 0) Ensure DeepSpeed is installed (raises if missing)
try:
    import deepspeed  # noqa: F401
except ImportError:
    raise ImportError(
        "DeepSpeed>=0.9.3 is required for ZeRO offload — "
        "please install it via 'pip install deepspeed' or 'pip install transformers[deepspeed]'"
    )

# 1) Load your JSONL dataset
dataset = load_dataset(
    "json",
    data_files="Raw_Data/travel_negotiation_dataset.jsonl",
    split="train"
)

# 2) Load tokenizer and set pad token
model_id = "mistralai/Mistral-7B-Instruct-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=True)
tokenizer.pad_token = tokenizer.eos_token  # ensure padding for causal LM

# 3) Configure 4‑bit quantization with fp32 CPU offload
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
    llm_int8_enable_fp32_cpu_offload=True
)

# 4) Load model with quantization & device mapping
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="auto",          # shard weights across GPU/CPU
    torch_dtype=torch.bfloat16
)

# 5) Enable gradient checkpointing to save activation memory
model.gradient_checkpointing_enable()

# 6) Preprocessing: truncate and pad to fixed length
def preprocess(example):
    prompt = f"### Input:\n{example['input']}\n### Output:\n{example['output']}"
    return tokenizer(
        prompt,
        truncation=True,
        padding=True,
        max_length=512
    )

tokenized_dataset = dataset.map(
    preprocess,
    remove_columns=dataset.column_names,
    batched=False
)

# 7) Data collator: pads batch & sets labels=input_ids
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False
)

# 8) Write DeepSpeed ZeRO‑3 offload configuration
ds_config = {
    "zero_optimization": {
        "stage": 3,
        "offload_param": {"device": "cpu", "pin_memory": True},
        "offload_optimizer": {"device": "cpu", "pin_memory": True},
        "overlap_comm": True,
        "contiguous_gradients": True
    },
    "fp16": {"enabled": True},
    "train_batch_size": 1,
    "gradient_accumulation_steps": 4
}
with open("ds_config.json", "w") as f:
    json.dump(ds_config, f)

# 9) Define TrainingArguments with DeepSpeed
training_args = TrainingArguments(
    output_dir="travel-negotiator-hf",
    num_train_epochs=3,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    learning_rate=2e-5,
    fp16=True,
    deepspeed="ds_config.json",
    logging_steps=10,
    save_steps=500,
    save_total_limit=2,
    report_to="none"
)

# 10) SafeTrainer: prevent re-moving of an accelerate-dispatched model
class SafeTrainer(Trainer):
    def _move_model_to_device(self, model, device):
        return model

# 11) Instantiate and run training
trainer = SafeTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    data_collator=data_collator,
    processing_class=tokenizer
)

print("Starting optimized training…")
trainer.train()
trainer.save_model("traveldate_negotiator_optimized")
print("Training complete!")
