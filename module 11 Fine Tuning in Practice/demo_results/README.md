# Demo results: farm order slips

> Module 11 · Designed by **Engr Usman Hasan**

A real training run of `Qwen/Qwen2.5-0.5B-Instruct` with LoRA (r = 16, alpha = 32, 3 epochs, 120 training examples).
This run was done on a plain CPU (about 17 minutes); on a Colab T4 GPU it is much faster.

| File | What it is |
|---|---|
| `farm_predictions.jsonl` | The 15 test questions with the perfect answer, the base model's answer and the fine-tuned model's answer |
| `farm_log_history.json` | Training and validation loss at every step |

Result (`python evaluate.py demo_results/farm_predictions.jsonl`):

| Model | Valid JSON | All fields right | Field accuracy |
|---|---|---|---|
| base | 100% | 0% | 20% |
| fine-tuned | 100% | 40% | 84% |

Add a big prompted model for comparison:
`python api_baseline.py demo_data/test.jsonl demo_results/farm_predictions.jsonl --provider groq`
