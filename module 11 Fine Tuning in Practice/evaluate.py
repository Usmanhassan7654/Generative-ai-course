"""
evaluate.py  -  Module 11: give every model the SAME exam and print a scoreboard
================================================================================
Designed by Engr Usman Hasan  (Bano Qabil Generative AI course)

WHAT IT DOES
  Reads a predictions file where every line is one test question:

    {"input": "...", "reference": "the perfect answer",
     "base": "what the base model said",
     "finetuned": "what our fine-tuned model said",
     "groq": "what a big prompted model said"}       <- optional extra columns

  Every key except "input" and "reference" is treated as one MODEL.

THE FLOW
  1. read the predictions file
  2. look at the reference answers and decide the task type:
       JSON task (extraction)  ->  valid JSON?  every field right?  each field right?
       label task (classify)   ->  is the label right?
       text task (style)       ->  how many of the right words did it use? (overlap)
  3. score every model the same way
  4. print the scoreboard + a few examples where the models disagree

HOW TO RUN
  python evaluate.py demo_results/farm_predictions.jsonl
  python evaluate.py predictions.jsonl            <- the file your Colab run downloads

No extra packages needed: only Python's built-in modules.
"""

# 'json' reads the predictions file and checks if answers are valid JSON
import json
# 're' (regular expressions) finds a {...} block inside a messy answer
import re
# 'sys' reads the file name typed after the script name
import sys
# Counter counts how often each label appears
from collections import Counter

# these two keys are NOT models
NOT_MODELS = ("input", "reference")


# ---------------------------------------------------------------------
# STEP 1: read the file
# ---------------------------------------------------------------------

# read every line of a .jsonl file into a list of dictionaries
def read_predictions(path):
    # open the file (utf-8 for Urdu letters and emojis)
    with open(path, encoding="utf-8") as f:
        # one dictionary per non-empty line
        return [json.loads(line) for line in f if line.strip()]


# find the model columns, e.g. ["base", "finetuned", "groq"]
def model_names(rows):
    # keep the order in which keys appear in the first row
    names = [k for k in rows[0] if k not in NOT_MODELS]
    # give the list back
    return names


# ---------------------------------------------------------------------
# small helpers that clean up model answers
# ---------------------------------------------------------------------

# models often wrap JSON in ```json ... ``` - take out the {...} part
def extract_json(text):
    # find the first '{' up to the last '}' (re.S lets '.' match new lines)
    match = re.search(r"\{.*\}", text or "", re.S)
    # nothing that looks like JSON
    if not match:
        # signal "not valid"
        return None
    # try to read it as JSON
    try:
        # json.loads turns the text into a Python dictionary
        value = json.loads(match.group(0))
    # broken JSON
    except ValueError:
        # signal "not valid"
        return None
    # only accept a dictionary (an object), not a list or number
    return value if isinstance(value, dict) else None


# make a label easy to compare: "Negative." -> "negative"
def clean_label(text):
    # lowercase and strip spaces
    text = (text or "").strip().lower()
    # keep only the first word (models sometimes add an explanation)
    first = text.split()[0] if text.split() else ""
    # remove punctuation like . , ! " '
    return first.strip(".,!?:;\"'`*")


# split text into a list of lowercase words
def words(text):
    # \w+ = runs of letters/digits
    return re.findall(r"\w+", (text or "").lower())


# ---------------------------------------------------------------------
# STEP 2: decide the task type from the reference answers
# ---------------------------------------------------------------------

# returns "json", "label" or "text"
def detect_task(rows):
    # all the perfect answers
    refs = [r["reference"] for r in rows]
    # how many of them are JSON objects?
    json_count = sum(1 for r in refs if extract_json(r) is not None)
    # more than half are JSON -> extraction task
    if json_count > len(refs) / 2:
        # JSON task
        return "json"
    # short answers (max 3 words) with few different values -> labels
    if all(len(r.split()) <= 3 for r in refs) and len(set(refs)) <= 10:
        # classification task
        return "label"
    # everything else is free text (style / tone tasks)
    return "text"


# ---------------------------------------------------------------------
# STEP 3: the three ways of scoring
# ---------------------------------------------------------------------

# score one model on a JSON task
def score_json(rows, name):
    # counters
    valid = exact = 0
    # field_right[key] = how many times that field was correct
    field_right = Counter()
    # field_total[key] = how many times that field was asked
    field_total = Counter()
    # go through every test question
    for r in rows:
        # the perfect answer as a dictionary
        ref = extract_json(r["reference"])
        # the model's answer as a dictionary (or None)
        pred = extract_json(r.get(name, ""))
        # count valid JSON answers
        if pred is not None:
            # one more valid answer
            valid += 1
        # compare field by field
        all_ok = pred is not None
        # every key in the perfect answer
        for key, value in ref.items():
            # this field was asked once more
            field_total[key] += 1
            # correct only if the model has the same value
            if pred is not None and pred.get(key) == value:
                # one more correct field
                field_right[key] += 1
            # any wrong field means the slip is not fully correct
            else:
                # mark as not fully correct
                all_ok = False
        # all fields correct?
        if all_ok:
            # one more perfect slip
            exact += 1
    # number of questions
    n = len(rows)
    # average field accuracy over all fields
    fields_pct = 100 * sum(field_right.values()) / max(1, sum(field_total.values()))
    # per-field percentages, for the detailed table
    per_field = {k: 100 * field_right[k] / field_total[k] for k in field_total}
    # return everything as a dictionary
    return {"valid JSON %": 100 * valid / n, "all fields right %": 100 * exact / n,
            "field accuracy %": fields_pct, "per_field": per_field}


# score one model on a label task
def score_label(rows, name):
    # count correct labels
    right = sum(1 for r in rows if clean_label(r.get(name)) == clean_label(r["reference"]))
    # mistakes as (should be, model said) pairs, to see what gets confused
    mistakes = Counter((clean_label(r["reference"]), clean_label(r.get(name)))
                       for r in rows if clean_label(r.get(name)) != clean_label(r["reference"]))
    # return the score and the top confusions
    return {"accuracy %": 100 * right / len(rows), "confusions": mistakes.most_common(3)}


# score one model on a free-text task with word overlap (F1)
def score_text(rows, name):
    # list of F1 scores, one per question
    f1s = []
    # go through every question
    for r in rows:
        # words of the perfect answer
        ref = Counter(words(r["reference"]))
        # words of the model's answer
        pred = Counter(words(r.get(name)))
        # words that appear in both (counted fairly)
        common = sum((ref & pred).values())
        # no overlap at all
        if common == 0:
            # F1 is zero
            f1s.append(0.0)
            # next question
            continue
        # precision: how much of the model's answer was right
        precision = common / sum(pred.values())
        # recall: how much of the perfect answer the model covered
        recall = common / sum(ref.values())
        # F1 = balance of precision and recall
        f1s.append(2 * precision * recall / (precision + recall))
    # average over all questions, as a percentage
    return {"word overlap F1 %": 100 * sum(f1s) / len(f1s)}


# ---------------------------------------------------------------------
# STEP 4: run everything and print the scoreboard
# ---------------------------------------------------------------------

# score every model and return {model_name: scores}
def score_all(rows):
    # decide the task type once
    task = detect_task(rows)
    # pick the matching scoring function
    scorer = {"json": score_json, "label": score_label, "text": score_text}[task]
    # score every model with the SAME function (a fair exam)
    return task, {name: scorer(rows, name) for name in model_names(rows)}


# print the results nicely
def print_report(path):
    # read the predictions
    rows = read_predictions(path)
    # score them
    task, results = score_all(rows)
    # header
    print("=" * 64)
    # which file and task
    print(f"SCOREBOARD  ({len(rows)} test questions, task type: {task})")
    # separator
    print("=" * 64)
    # the main metric names (skip the detailed ones)
    metrics = [m for m in next(iter(results.values())) if m not in ("per_field", "confusions")]
    # table header row
    print(f"{'model':<14}" + "".join(f"{m:>22}" for m in metrics))
    # one row per model
    for name, scores in results.items():
        # model name followed by its numbers
        print(f"{name:<14}" + "".join(f"{scores[m]:>21.0f}%" for m in metrics))
    # extra details for JSON tasks
    if task == "json":
        # heading
        print("\nPer field (% correct):")
        # all field names
        fields = list(next(iter(results.values()))["per_field"])
        # header row with model names
        print(f"{'field':<16}" + "".join(f"{n:>12}" for n in results))
        # one row per field
        for field in fields:
            # field name followed by each model's score
            print(f"{field:<16}" + "".join(f"{results[n]['per_field'][field]:>11.0f}%" for n in results))
    # extra details for label tasks
    if task == "label":
        # heading
        print("\nMost common mistakes (should be -> model said):")
        # one line per model
        for name, scores in results.items():
            # print the confusions list
            print(f"  {name}: {scores['confusions']}")
    # show up to 3 questions where base and fine-tuned disagree
    if "base" in results and "finetuned" in results:
        # heading
        print("\nExamples where the two models disagree:")
        # rows with different answers
        diff = [r for r in rows if (r.get("base") or "").strip() != (r.get("finetuned") or "").strip()]
        # print the first three
        for r in diff[:3]:
            # the question
            print(f"\n  INPUT     : {r['input']}")
            # the perfect answer
            print(f"  REFERENCE : {r['reference']}")
            # base model answer (first 160 characters)
            print(f"  BASE      : {(r.get('base') or '')[:160]}")
            # fine-tuned answer
            print(f"  FINETUNED : {(r.get('finetuned') or '')[:160]}")
    # give the numbers back (the notebook uses them for a chart)
    return task, results


# run only when started directly
if __name__ == "__main__":
    # the file must be given
    if len(sys.argv) < 2:
        # show usage and stop
        sys.exit("Usage: python evaluate.py <predictions.jsonl>")
    # run the report
    print_report(sys.argv[1])
