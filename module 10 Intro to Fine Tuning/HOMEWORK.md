# 📝 Homework: build YOUR fine-tuning dataset (due next class)

> Module 10 · Designed by **Engr Usman Hasan**

Next week you will fine-tune a real model on **your own dataset** and compare it with the base model.
If your dataset is not ready, you cannot train. So this homework is the most important part of the module.

## 1. Pick a narrow task with a clear right answer
✅ **Good:** turn messages into JSON · classify complaints · detect sentiment in Roman Urdu · rewrite casual text as formal · tag a product category · extract names and dates
❌ **Bad:** "teach the model my company's facts" (that is RAG!) · "make it smarter" · "answer any question"

**Test your idea:** could two different people write the SAME correct answer for an input? If yes, it's a good task.

## 2. Set up your folder
Copy `templates/my_project` and rename it to your project, e.g. `ali_complaint_router`.
- `system_prompt.txt`: ONE clear instruction (same for every example)
- `examples.csv`: two columns, `input` and `output`. Write them in Excel or Google Sheets, then **File → Download → CSV**

## 3. The 10 rules
1. **At least 100 examples**, ideally 200–500.
2. **The output is the lesson.** Write exactly what you want the model to say. No "Sure! Here is…".
3. **Be consistent:** same keys, same spelling, same format every time.
4. **Variety:** short and long, Roman Urdu and English, typos, polite and angry.
5. **At least 10–15% edge cases:** missing info, off-topic messages, tricky inputs.
6. **Balanced labels** for classification (no label more than 3× another).
7. **No real personal data:** fake names, phones and addresses only.
8. **Short examples** (a few sentences), so training fits on free Colab.
9. **AI-drafted examples are allowed** only if you check and fix every one, and say so in your README.
10. **No duplicates.**

## 4. Build and check
```bash
python make_dataset.py my_project
python validate_dataset.py my_project
```
Fix every **error**. Read every **warning**. Then read **20 random examples yourself**, because the script cannot check meaning.

## 5. Bring to class
- `train.jsonl`, `val.jsonl`, `test.jsonl` (do NOT edit test.jsonl after you make it)
- A short `README.md`: your task, the output format, how you made the data, and 3 sample examples

Next week: `train.jsonl` → fine-tune → run base vs fine-tuned on `test.jsonl` → scoreboard! 🏆
