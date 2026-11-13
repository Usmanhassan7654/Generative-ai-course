# Answer key: 10 problems in bad_examples.jsonl

> Module 10 · Designed by **Engr Usman Hasan**

| Line | Problem | Caught by script? | Fix |
|---|---|---|---|
| 3 | Broken JSON (missing closing quote) | ✅ error | Never type JSONL by hand. Use a CSV + `make_dataset.py` |
| 4 | Different system prompt ("You are a helpful assistant.") | ✅ warning | Same system prompt in every example |
| 5 | Key `qty` instead of `quantity` | ✅ error | Same keys, same spelling, every time |
| 6 | Answer starts with "Sure! Here is your order:" | ✅ error | The answer must be ONLY what you want the model to output |
| 7 | Exact duplicate of line 1 | ✅ warning | Delete duplicates. They make the model over-learn one example |
| 8 | No assistant message | ✅ error | Every example needs the perfect answer |
| 9 | Real-looking phone number | ✅ warning | Replace personal data with fake data |
| 10 | Customer asked for **5** litres, answer says **3** | ❌ only a human can see this | Read your examples! A wrong answer teaches a wrong habit |
| 11 | Area written `dha ph6` instead of `DHA Phase 6` | ❌ only a human can see this | Keep one standard spelling in outputs |
| 12 | Empty user message | ✅ error | Every example needs an input |

**Lesson:** the script catches FORMAT problems (8 of 10). Only a human catches MEANING problems (lines 10 and 11).
