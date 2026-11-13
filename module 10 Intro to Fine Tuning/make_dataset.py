"""
make_dataset.py  -  Module 10: turn a simple spreadsheet into a fine-tuning dataset
====================================================================================
Designed by Engr Usman Hasan  (Bano Qabil Generative AI course)

WHY THIS FILE EXISTS
  Writing JSONL by hand is slow and easy to break (one missing quote = broken file).
  So students write their examples in Excel / Google Sheets with TWO columns:

      input   |  output
      --------+---------------------------
      what the user says | the PERFECT answer

  ...then this script does the boring part.

THE FLOW
  your_folder/examples.csv  +  your_folder/system_prompt.txt
                     |
                     v
        1. read the system prompt (the same for every example)
        2. read every row of the CSV
        3. turn each row into one chat example (system / user / assistant)
        4. shuffle the examples (so the split is fair)
        5. split 80% train / 10% validation / 10% test
        6. write train.jsonl, val.jsonl, test.jsonl  (one example per line)

HOW TO RUN
  python make_dataset.py examples/01_farm_order_slips
  python make_dataset.py my_project            <- your own folder

No extra packages needed: only Python's built-in modules.
"""

# 'csv' reads spreadsheet files saved as .csv
import csv
# 'json' turns Python dictionaries into JSON text
import json
# 'os' builds file paths that work on Windows, Mac and Linux
import os
# 'random' shuffles the examples
import random
# 'sys' lets us read the folder name typed after the script name
import sys

# ---------------------------------------------------------------------
# SETTINGS  (change these if your teacher asks you to)
# ---------------------------------------------------------------------

# 80% of the examples go to training (the "textbook" the model studies)
TRAIN_SHARE = 0.80
# 10% go to validation (the "practice test" checked during training)
VAL_SHARE = 0.10
# the rest (about 10%) become the test set (the "final exam", kept sealed)
# a fixed seed means the shuffle gives the SAME result every time you run it
SEED = 42


# ---------------------------------------------------------------------
# STEP 1: read the system prompt
# ---------------------------------------------------------------------

# a function that reads system_prompt.txt from the folder
def read_system_prompt(folder):
    # build the full path, e.g. "examples/01_farm_order_slips/system_prompt.txt"
    path = os.path.join(folder, "system_prompt.txt")
    # if the file is missing, explain what to do and stop
    if not os.path.exists(path):
        # stop the program with a clear message
        sys.exit(f"Missing {path}. Create it and write ONE instruction for the model.")
    # open the file (utf-8 handles Urdu letters and emojis)
    with open(path, encoding="utf-8") as f:
        # read it and remove spaces/new lines at the start and end
        prompt = f.read().strip()
    # an empty system prompt is a mistake, so stop early
    if not prompt:
        # stop with a message
        sys.exit("system_prompt.txt is empty. Write the instruction for the model.")
    # give the prompt back
    return prompt


# ---------------------------------------------------------------------
# STEP 2: read the CSV rows
# ---------------------------------------------------------------------

# a function that reads examples.csv and returns a list of (input, output) pairs
def read_rows(folder):
    # full path to the CSV file
    path = os.path.join(folder, "examples.csv")
    # stop with a message if the file does not exist
    if not os.path.exists(path):
        # explain how to make the CSV
        sys.exit(f"Missing {path}. In Excel/Sheets: File > Download > CSV, columns 'input' and 'output'.")
    # the list we will fill
    rows = []
    # open the CSV; newline="" is the correct way to open CSV files in Python
    with open(path, encoding="utf-8-sig", newline="") as f:
        # DictReader uses the first row (the header) as column names
        reader = csv.DictReader(f)
        # check that the two needed columns exist
        if reader.fieldnames is None or "input" not in reader.fieldnames or "output" not in reader.fieldnames:
            # stop with a clear message
            sys.exit("The CSV must have a header row with the columns: input, output")
        # go through every row; line_no starts at 2 because line 1 is the header
        for line_no, row in enumerate(reader, start=2):
            # clean the input text (None becomes "")
            user_text = (row["input"] or "").strip()
            # clean the output text
            answer = (row["output"] or "").strip()
            # skip rows where one side is empty, and tell the student
            if not user_text or not answer:
                # print a warning with the line number so it is easy to fix
                print(f"  skipped line {line_no}: input or output is empty")
                # jump to the next row
                continue
            # keep this pair
            rows.append((user_text, answer))
    # give the list back
    return rows


# ---------------------------------------------------------------------
# STEP 3: turn one row into one chat example
# ---------------------------------------------------------------------

# build the dictionary that fine-tuning tools expect
def to_chat_example(system_prompt, user_text, answer):
    # every example is {"messages": [system, user, assistant]}
    return {
        # a list of three messages, in this exact order
        "messages": [
            # 1) the instruction: SAME in every example
            {"role": "system", "content": system_prompt},
            # 2) what the user/customer says
            {"role": "user", "content": user_text},
            # 3) the perfect answer: the model will learn to copy THIS
            {"role": "assistant", "content": answer},
        ]
    }


# ---------------------------------------------------------------------
# STEP 5 + 6: split and save
# ---------------------------------------------------------------------

# write a list of examples into a .jsonl file (one JSON object per line)
def write_jsonl(path, examples):
    # open the file for writing ("w" replaces any old file)
    with open(path, "w", encoding="utf-8") as f:
        # one example at a time
        for example in examples:
            # ensure_ascii=False keeps Urdu letters and emojis readable
            line = json.dumps(example, ensure_ascii=False)
            # write the JSON plus a new line, so each example is on its own line
            f.write(line + "\n")


# the main function: runs all the steps in order
def main():
    # the folder must be given after the script name
    if len(sys.argv) < 2:
        # show how to use the script, then stop
        sys.exit("Usage: python make_dataset.py <folder>   e.g.  python make_dataset.py my_project")
    # the folder name the student typed
    folder = sys.argv[1]

    # STEP 1: the system prompt
    system_prompt = read_system_prompt(folder)
    # STEP 2: the CSV rows
    rows = read_rows(folder)
    # we need at least 10 rows to make three files
    if len(rows) < 10:
        # stop with a message
        sys.exit(f"Only {len(rows)} usable rows. Write at least 10 (homework target: 200+).")

    # STEP 3: convert every row into a chat example
    examples = [to_chat_example(system_prompt, u, a) for u, a in rows]

    # STEP 4: shuffle with a fixed seed so the result is repeatable
    random.Random(SEED).shuffle(examples)

    # STEP 5: work out how many examples go into each file
    total = len(examples)
    # number for validation: at least 1
    n_val = max(1, round(total * VAL_SHARE))
    # number for test: at least 1, and roughly the same as validation
    n_test = max(1, total - round(total * TRAIN_SHARE) - n_val)
    # training gets everything that is left
    n_train = total - n_val - n_test
    # cut the shuffled list into three parts
    train = examples[:n_train]
    # the next n_val examples
    val = examples[n_train:n_train + n_val]
    # the last n_test examples
    test = examples[n_train + n_val:]

    # STEP 6: save the three files next to the CSV
    write_jsonl(os.path.join(folder, "train.jsonl"), train)
    # validation file
    write_jsonl(os.path.join(folder, "val.jsonl"), val)
    # test file (do NOT look at it while improving your data!)
    write_jsonl(os.path.join(folder, "test.jsonl"), test)

    # print a friendly summary
    print(f"\nDone! {total} examples from {folder}/examples.csv")
    # show the size of each file
    print(f"  train.jsonl : {len(train)}  (the textbook)")
    # validation size
    print(f"  val.jsonl   : {len(val)}  (the practice test)")
    # test size
    print(f"  test.jsonl  : {len(test)}  (the sealed final exam)")
    # remind the student of the next step
    print(f"\nNext: python validate_dataset.py {folder}")


# run main() only when this file is started directly (not when imported)
if __name__ == "__main__":
    # start the program
    main()
