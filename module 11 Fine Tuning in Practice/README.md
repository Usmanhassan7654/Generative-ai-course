# 🏋️ Module 11: Fine-Tuning in Practice (Marhaba Cattle & Dairy Farm)

> Designed by **Engr Usman Hasan** · Bano Qabil Generative AI course

Two classes, one mission: **train a model on YOUR Module 10 dataset and prove it got better.**

| Class | Slides | What happens |
|---|---|---|
| **Day 1, Saturday (2 h)** | `Module_11_Day1_Saturday_LoRA_and_Training.pptx` | The memory problem · PEFT · LoRA · QLoRA · training words · hosted vs open-source · **train on Colab** |
| **Day 2, Sunday (2 h)** | `Module_11_Day2_Sunday_Evaluation_and_Cost.pptx` | The sealed exam · scoreboard · small fine-tuned vs big prompted (Groq / Gemini) · cost and infrastructure · **student talks** |

**Syllabus:** fine-tuning with a hosted API or a lightweight open-source approach · evaluating fine-tuned model performance · cost and infrastructure · hands-on: fine-tune a model and compare it to the base model.

## Training: Google Colab (free T4 GPU)
1. Open https://colab.research.google.com → **Upload** → `Module11_FineTune_Lab.ipynb`
2. **Runtime → Change runtime type → T4 GPU**
3. Run cells top to bottom. Use the farm demo data, or upload your Module 10 zip (`train.jsonl`, `val.jsonl`, `test.jsonl`).
4. Optional bonus: add `GROQ_API_KEY` and/or `GEMINI_API_KEY` in Colab **🔑 Secrets** to compare with a big prompted model.

Model: `Qwen/Qwen2.5-0.5B-Instruct` with QLoRA (4-bit). Change `MODEL_NAME` to `Qwen/Qwen2.5-1.5B-Instruct` for better results.

## VS Code scripts (no GPU needed)
```bash
pip install -r requirements.txt

python evaluate.py demo_results/farm_predictions.jsonl     # scoreboard from a predictions file
python cost_estimator.py demo_data --train-seconds 300     # tokens + cost of a dataset
python api_baseline.py demo_data/test.jsonl demo_results/farm_predictions.jsonl --provider groq
python evaluate.py demo_results/farm_predictions.jsonl     # now with a 'groq' column
```
Put your free keys in a `.env` file (copy `.env.example`). Never share or upload `.env`.

## Files
| File / folder | What it is |
|---|---|
| `Module11_FineTune_Lab.ipynb` | Colab: QLoRA training, loss curve, base vs fine-tuned, Groq/Gemini bonus, save adapter, cost |
| `evaluate.py` | Gives every model the same exam and prints a scoreboard. Every line commented |
| `api_baseline.py` | Asks Groq or Gemini (free keys) the same test questions. Every line commented |
| `cost_estimator.py` | Counts tokens and estimates training + monthly running cost. Every line commented |
| `demo_data/` | Farm order-slip dataset from Module 10 (120 / 15 / 15) |
| `demo_results/` | Real results of a training run on the farm dataset (predictions + loss history) |
| `TROUBLESHOOTING.md` | Common Colab errors and fixes |

Prices and model names change often. The scripts take prices as inputs, and model names can be changed at the top of `api_baseline.py`.

---
© Module 11 course material designed by **Engr Usman Hasan**.
