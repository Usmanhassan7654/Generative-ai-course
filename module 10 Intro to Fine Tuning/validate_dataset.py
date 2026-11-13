"""
validate_dataset.py  -  Module 10: check a fine-tuning dataset BEFORE training
===============================================================================
Designed by Engr Usman Hasan  (Bano Qabil Generative AI course)

WHY THIS FILE EXISTS
  Training on a broken dataset wastes GPU time and teaches the model bad habits.
  This script is the "dataset doctor": it reads your .jsonl files and lists
  every problem it can find, with the LINE NUMBER, so you can fix it.

WHAT IT CHECKS
  Errors (must fix):                    Warnings (please look):
  - a line is not valid JSON            - different system prompts
  - "messages" list is missing          - the same input appears twice
  - wrong role order / empty text       - looks like a real phone / email / CNIC
  - last message is not "assistant"     - very long examples
  - JSON answers that do not parse      - fewer than 100 examples
  - JSON answers with different keys    - unbalanced labels
  - a test example also in train        - chatty answers ("Sure! Here is...")

  The script checks FORMAT.  Only a human can check MEANING
  (is the answer actually correct?).  Do both!

HOW TO RUN
  python validate_dataset.py examples/01_farm_order_slips      <- a folder (train/val/test)
  python validate_dataset.py examples/04_bad_dataset/bad_examples.jsonl   <- one file

No extra packages needed: only Python's built-in modules.
"""

# 'json' reads each line of the .jsonl file
import json
# 'os' checks whether a path is a folder or a file
import os
# 're' (regular expressions) finds patterns like phone numbers
import re
# 'sys' reads the path typed after the script name
import sys
# Counter counts things, e.g. how many times each label appears
from collections import Counter

# ---------------------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------------------

# homework minimum: fewer examples than this gives a warning
MIN_EXAMPLES = 100
# examples longer than this (roughly, in tokens) give a warning
MAX_TOKENS = 512
# patterns that look like private data (Pakistani mobile, email, CNIC)
PRIVATE_PATTERNS = {
    # e.g. 0321-4567890 or 03214567890 or +92 321 4567890
    "phone number": re.compile(r"(\+92[\s-]?|0)3\d{2}[\s-]?\d{7}"),
    # anything like name@site.com
    "email address": re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"),
    # CNIC format 42101-1234567-1
    "CNIC number": re.compile(r"\b\d{5}-\d{7}-\d\b"),
}
# answers that start like a chatbot instead of giving the clean answer
CHATTY_STARTS = ("sure", "here is", "here's", "of course", "certainly")


# ---------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------

# a rough token count: about 4 characters per token in English
def approx_tokens(text):
    # integer division; +1 so short texts never count as 0
    return len(text) // 4 + 1


# try to read text as a JSON object; return the dict, or None if it fails
def as_json_object(text):
    # 'try' = attempt it without crashing
    try:
        # turn the text into Python data
        value = json.loads(text)
    # json.loads raises ValueError for broken JSON
    except ValueError:
        # not valid JSON
        return None
    # we only accept a JSON object { ... }, not a list or a number
    return value if isinstance(value, dict) else None


# ---------------------------------------------------------------------
# read and check ONE file
# ---------------------------------------------------------------------

# returns a list of good examples plus lists of errors and warnings
def check_file(path):
    # problems that MUST be fixed
    errors = []
    # problems that SHOULD be looked at
    warnings = []
    # examples that passed the structure checks
    good = []
    # the short file name, used in messages
    name = os.path.basename(path)

    # open the file (utf-8 for Urdu letters and emojis)
    with open(path, encoding="utf-8") as f:
        # read all lines into a list
        lines = f.readlines()

    # go through every line; line numbers start at 1 like in VS Code
    for no, raw in enumerate(lines, start=1):
        # remove the new-line character and spaces at the ends
        raw = raw.strip()
        # skip completely empty lines (but tell the student)
        if not raw:
            # a warning, not an error
            warnings.append(f"{name} line {no}: empty line (delete it)")
            # go to the next line
            continue
        # CHECK 1: is the line valid JSON?
        try:
            # parse the line
            example = json.loads(raw)
        # broken JSON lands here
        except ValueError as e:
            # record the error with Python's explanation
            errors.append(f"{name} line {no}: not valid JSON ({e.msg})")
            # cannot check anything else on this line
            continue
        # CHECK 2: is there a "messages" list?
        messages = example.get("messages") if isinstance(example, dict) else None
        # missing or not a list = error
        if not isinstance(messages, list) or not messages:
            # record the error
            errors.append(f"{name} line {no}: no \"messages\" list")
            # next line
            continue
        # CHECK 3: every message needs a role and non-empty text
        roles = []
        # a flag that turns False when something is wrong
        ok = True
        # look at each message in the example
        for m in messages:
            # the role, e.g. "user"
            role = m.get("role") if isinstance(m, dict) else None
            # the text of the message
            content = m.get("content") if isinstance(m, dict) else None
            # role must be one of the three allowed words
            if role not in ("system", "user", "assistant"):
                # record the error
                errors.append(f"{name} line {no}: unknown role {role!r}")
                # mark this example as broken
                ok = False
            # content must be a string with real text in it
            elif not isinstance(content, str) or not content.strip():
                # record the error
                errors.append(f"{name} line {no}: empty {role} message")
                # mark as broken
                ok = False
            # remember the role order
            roles.append(role)
        # CHECK 4: role order must be (system), user, assistant, user, assistant ...
        turns = roles[1:] if roles and roles[0] == "system" else roles
        # the pattern we expect: user, assistant, user, assistant ...
        expected = ["user", "assistant"] * (len(turns) // 2 + 1)
        # compare the real order with the expected order
        if ok and (turns != expected[:len(turns)] or not turns or turns[-1] != "assistant"):
            # record the error and show the actual order
            errors.append(f"{name} line {no}: role order {roles} (must end with assistant)")
            # mark as broken
            ok = False
        # only keep examples that passed checks 1-4
        if ok:
            # store the example together with its line number
            good.append((no, messages))
    # give everything back
    return good, errors, warnings


# ---------------------------------------------------------------------
# checks that look at ALL examples of a file together
# ---------------------------------------------------------------------

# the system prompt, user text and answer of one example
def parts(messages):
    # the system message text, or "" if there is none
    system = next((m["content"] for m in messages if m["role"] == "system"), "")
    # the first user message
    user = next(m["content"] for m in messages if m["role"] == "user")
    # the LAST assistant message (the answer being taught)
    answer = [m["content"] for m in messages if m["role"] == "assistant"][-1]
    # return all three
    return system, user, answer


# look for patterns across all examples of one file
def check_together(name, good, errors, warnings):
    # nothing to compare if there are no good examples
    if not good:
        # stop here
        return
    # CHECK 5: is the system prompt the same everywhere?
    systems = Counter(parts(m)[0] for _, m in good)
    # more than one different system prompt = warning
    if len(systems) > 1:
        # the most common one is probably the "right" one
        main_prompt = systems.most_common(1)[0][0]
        # list the lines that use a different prompt
        odd = [no for no, m in good if parts(m)[0] != main_prompt]
        # record the warning
        warnings.append(f"{name}: {len(systems)} different system prompts (odd ones on lines {odd})")
    # CHECK 6: duplicate inputs
    seen = {}
    # go through the examples in order
    for no, m in good:
        # the user text, in lowercase so "Hi" and "hi" count as the same
        key = parts(m)[1].strip().lower()
        # already seen this input before?
        if key in seen:
            # record the warning with both line numbers
            warnings.append(f"{name} line {no}: duplicate of line {seen[key]}")
        # remember first appearance
        else:
            # store the line number
            seen[key] = no
    # CHECK 7: is this a JSON task? (most answers are JSON objects)
    answers = [(no, parts(m)[2]) for no, m in good]
    # count answers that parse as JSON objects
    json_count = sum(1 for _, a in answers if as_json_object(a) is not None)
    # if more than half are JSON, we treat the task as "answer must be JSON"
    if json_count > len(answers) / 2:
        # the most common set of keys = the expected format
        key_sets = Counter(tuple(sorted(as_json_object(a))) for _, a in answers if as_json_object(a) is not None)
        # the winner
        expected_keys = key_sets.most_common(1)[0][0]
        # check every answer
        for no, a in answers:
            # try to parse it
            obj = as_json_object(a)
            # not JSON at all
            if obj is None:
                # record the error and show the start of the answer
                errors.append(f"{name} line {no}: answer is not clean JSON -> {a[:45]!r}")
            # JSON, but with different keys
            elif tuple(sorted(obj)) != expected_keys:
                # show which keys are extra or missing
                extra = set(obj) - set(expected_keys)
                # keys that should be there but are not
                missing = set(expected_keys) - set(obj)
                # record the error
                errors.append(f"{name} line {no}: different keys (extra {sorted(extra)}, missing {sorted(missing)})")
    # not a JSON task: warn about chatty answers instead
    else:
        # check each answer
        for no, a in answers:
            # does it start like "Sure! Here is..."?
            if a.strip().lower().startswith(CHATTY_STARTS):
                # record the warning
                warnings.append(f"{name} line {no}: chatty answer start -> {a[:30]!r}")
    # CHECK 8: private data
    for no, m in good:
        # join all text of the example
        text = " ".join(x["content"] for x in m)
        # try every private-data pattern
        for label, pattern in PRIVATE_PATTERNS.items():
            # found something?
            if pattern.search(text):
                # record the warning
                warnings.append(f"{name} line {no}: looks like a real {label}. Use fake data!")
    # CHECK 9: very long examples
    for no, m in good:
        # rough size of the whole example
        size = approx_tokens(" ".join(x["content"] for x in m))
        # too long?
        if size > MAX_TOKENS:
            # record the warning
            warnings.append(f"{name} line {no}: about {size} tokens (keep under {MAX_TOKENS} for free Colab)")


# ---------------------------------------------------------------------
# label balance (only for classification tasks)
# ---------------------------------------------------------------------

# print a small bar chart if the answers look like labels
def show_labels(all_good, warnings):
    # all answers
    answers = [parts(m)[2].strip() for _, m in all_good]
    # count each different answer
    counts = Counter(answers)
    # labels = short answers (max 3 words) and only a few different ones
    if not answers or len(counts) > 10 or any(len(a.split()) > 3 for a in answers):
        # not a classification task, nothing to show
        return
    # heading
    print("\nLabel balance:")
    # the biggest count, used to scale the bars
    biggest = max(counts.values())
    # one row per label, most common first
    for label, n in counts.most_common():
        # bar of '#' characters, max 30 long
        bar = "#" * max(1, round(30 * n / biggest))
        # print label, bar and count
        print(f"  {label:<12} {bar} {n}")
    # warn if the biggest label is more than 3x the smallest
    if biggest > 3 * min(counts.values()):
        # record the warning
        warnings.append("labels are unbalanced (one label is more than 3x another). Add examples of the small label")


# ---------------------------------------------------------------------
# main: decide folder vs file, run all checks, print the report
# ---------------------------------------------------------------------

# the main function
def main():
    # a path must be given
    if len(sys.argv) < 2:
        # show usage and stop
        sys.exit("Usage: python validate_dataset.py <folder or file.jsonl>")
    # the path the student typed
    target = sys.argv[1]
    # a folder: check train/val/test that exist inside it
    if os.path.isdir(target):
        # the three standard file names, in this order
        files = [os.path.join(target, n) for n in ("train.jsonl", "val.jsonl", "test.jsonl")]
        # keep only the ones that exist
        files = [f for f in files if os.path.exists(f)]
    # a single file
    else:
        # a list with one file
        files = [target]
    # no files found
    if not files:
        # explain and stop
        sys.exit("No .jsonl files found. Run make_dataset.py first.")

    # collected results
    all_errors, all_warnings, all_good, per_file = [], [], [], {}
    # check each file
    for path in files:
        # structure checks (1-4)
        good, errors, warnings = check_file(path)
        # pattern checks (5-9)
        check_together(os.path.basename(path), good, errors, warnings)
        # collect errors
        all_errors += errors
        # collect warnings
        all_warnings += warnings
        # collect good examples
        all_good += good
        # remember good examples per file name (for the leakage check)
        per_file[os.path.basename(path)] = good

    # CHECK 10: leakage - a test or val input that is also in train
    if "train.jsonl" in per_file:
        # all training inputs in lowercase
        train_inputs = {parts(m)[1].strip().lower() for _, m in per_file["train.jsonl"]}
        # look in val and test
        for other in ("val.jsonl", "test.jsonl"):
            # go through that file's examples
            for no, m in per_file.get(other, []):
                # same input also in train = the exam questions were in the textbook!
                if parts(m)[1].strip().lower() in train_inputs:
                    # record the error
                    all_errors.append(f"{other} line {no}: also in train.jsonl (leakage, the exam is not fair)")

    # CHECK 11: enough examples in total?
    if len(all_good) < MIN_EXAMPLES:
        # record the warning
        all_warnings.append(f"only {len(all_good)} good examples (homework target: {MIN_EXAMPLES}+, better 200+)")

    # REPORT: how many examples per file
    print("=" * 60)
    # title line
    print("DATASET CHECK:", target)
    # separator
    print("=" * 60)
    # one line per file
    for name, good in per_file.items():
        # number of good examples in that file
        print(f"  {name:<20} {len(good)} good examples")
    # label bar chart (classification only)
    show_labels(all_good, all_warnings)
    # print all errors
    print(f"\nERRORS ({len(all_errors)})  - must fix:")
    # one per line
    for e in all_errors:
        # red cross for errors
        print("  [X]", e)
    # print all warnings
    print(f"\nWARNINGS ({len(all_warnings)})  - please look:")
    # one per line
    for w in all_warnings:
        # exclamation mark for warnings
        print("  [!]", w)
    # final verdict
    if all_errors:
        # cannot train yet
        print("\nRESULT: NOT READY. Fix the errors and run this check again.")
    # warnings only
    elif all_warnings:
        # can train, but look first
        print("\nRESULT: READY, but read the warnings first.")
    # perfect
    else:
        # all good
        print("\nRESULT: READY for fine-tuning next week!")
    # remind them of the human check
    print("Remember: this script checks FORMAT. Read 20 random examples yourself to check MEANING.")


# run main() only when this file is started directly
if __name__ == "__main__":
    # start the program
    main()
