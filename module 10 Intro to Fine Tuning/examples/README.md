# Example datasets (copy the PATTERN, not the data)

> Module 10 · Designed by **Engr Usman Hasan**

Each folder shows one **type** of fine-tuning task. All farm data is made up for class.

| Folder | Task type | Input → Output | Size | Note |
|---|---|---|---|---|
| `01_farm_order_slips` | **Extraction** | WhatsApp message → JSON order slip | 150 | Includes 22 non-orders and messages with missing info (edge cases) |
| `02_roman_urdu_sentiment` | **Classification** | Customer message → `positive` / `negative` / `neutral` | 94 | Labels are balanced. Just under 100 on purpose: the validator warns. Can you add 6+? |
| `03_formal_customer_replies` | **Style / tone** | Casual manager note → formal English message | 30 | Small "mini" example. Style tasks need 100+ for real training |
| `04_bad_dataset` | **Spot the mistakes** | 12 broken lines | 12 | Game for class. Answers in `ANSWERS.md` (no peeking!) |

Every folder (except 04) has:
- `examples.csv`: the spreadsheet (columns `input`, `output`)
- `system_prompt.txt`: the one instruction used in every example
- `train.jsonl`, `val.jsonl`, `test.jsonl`: made by `make_dataset.py`

Rebuild any of them:
```bash
python make_dataset.py examples/01_farm_order_slips
python validate_dataset.py examples/01_farm_order_slips
```
