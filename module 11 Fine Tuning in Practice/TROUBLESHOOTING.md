# 🔧 Troubleshooting (Module 11)

> Module 11 · Designed by **Engr Usman Hasan**

| Problem | Fix |
|---|---|
| `No GPU found` / training is extremely slow | **Runtime → Change runtime type → T4 GPU → Save**, then run all cells again from the top |
| Colab asks to **restart** after `pip install` | Click **Restart session**, then continue from Step 1 (no need to install again) |
| `CUDA out of memory` | Set `BATCH_SIZE = 2` (or `1`) in the settings cell, then **Runtime → Restart session** and run again |
| `ModuleNotFoundError` after a restart | Re-run the install cell, restart once more, continue |
| Colab disconnected / "usage limits" | Free Colab has time limits. Wait a bit or use another Google account. The farm demo trains in minutes |
| Upload: `train.jsonl` not found | Your zip must contain `train.jsonl`, `val.jsonl`, `test.jsonl`. Check with the `os.listdir("my_data")` output; files may be in a sub-folder: set `DATA_DIR = "my_data/<folder name>"` |
| Validation loss goes UP while training loss goes DOWN | Overfitting: use `EPOCHS = 2`, or add more varied examples |
| Fine-tuned answers are still wrong | Check your dataset consistency (Module 10 validator), try `Qwen/Qwen2.5-1.5B-Instruct`, or train 1 more epoch |
| Groq / Gemini: `model not found` | Model names change. Check https://console.groq.com/docs/models or https://ai.google.dev/gemini-api/docs/models and change `DEFAULT_MODELS` in `api_baseline.py` |
| Groq / Gemini: `429` / rate limit | Free keys allow a few calls per minute. The script waits and retries; or run with `--wait 5` |
| Key not loaded in Colab | 🔑 Secrets: name must be exactly `GROQ_API_KEY` / `GEMINI_API_KEY`, and **Notebook access** must be ON |
