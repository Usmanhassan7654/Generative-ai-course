# 🎓 Module 10: Intro to Fine-Tuning (Marhaba Cattle & Dairy Farm)

> Designed by **Engr Usman Hasan** · Bano Qabil Generative AI course

**Topics:** fine-tuning basics (when and why) · fine-tuning vs prompting vs RAG · preparing a dataset · hands-on: prepare a fine-tuning dataset for a specific task

**Big idea:** prompting gives the model *instructions*, RAG gives it *knowledge*, fine-tuning gives it *habits*. And habits are only as good as your examples.

No GPU and no API key needed today. Only Python's built-in modules.

## Option A: Google Colab (easiest)
1. Open https://colab.research.google.com → **Upload** → `Module10_Dataset_Lab.ipynb`
2. Run the cells top to bottom (`Shift + Enter`). The notebook creates its own example files.
3. The last cell downloads your finished dataset as a zip.

## Option B: VS Code
```bash
# open this folder in VS Code, then in the terminal:
python make_dataset.py examples/01_farm_order_slips      # CSV -> train/val/test.jsonl
python validate_dataset.py examples/01_farm_order_slips  # check it
python validate_dataset.py examples/04_bad_dataset/bad_examples.jsonl   # spot-the-mistakes game

# your own project:
#   copy templates/my_project, fill examples.csv + system_prompt.txt, then
python make_dataset.py my_project
python validate_dataset.py my_project
```

## Files
| File / folder | What it is |
|---|---|
| `Module_10_Intro_to_Fine_Tuning.pptx` | Class slides with speaker notes (Roman Urdu) |
| `make_dataset.py` | Spreadsheet (CSV) → `train/val/test.jsonl`. Every line commented |
| `validate_dataset.py` | The "dataset doctor": finds format problems with line numbers. Every line commented |
| `examples/` | 3 finished example datasets (extraction, classification, style) + 1 bad dataset game |
| `templates/my_project/` | Starter folder for students' own datasets |
| `HOMEWORK.md` | Student brief: dataset due next class |
| `Module10_Dataset_Lab.ipynb` | Colab version of the whole hands-on |

Next module (11): fine-tune with LoRA / QLoRA on these datasets, then compare base vs fine-tuned.

---
© Module 10 course material designed by **Engr Usman Hasan**.
