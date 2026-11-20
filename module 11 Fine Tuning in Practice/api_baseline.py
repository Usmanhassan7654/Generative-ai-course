"""
api_baseline.py  -  Module 11: can a BIG prompted model beat our SMALL fine-tuned one?
======================================================================================
Designed by Engr Usman Hasan  (Bano Qabil Generative AI course)

WHY THIS FILE EXISTS
  Our fine-tuned model is tiny (0.5 billion parameters). Groq and Gemini give us
  free access to much bigger models. This script asks a big model the SAME test
  questions, with the SAME system prompt, and adds its answers as a new column
  in predictions.jsonl. Then evaluate.py can compare all of them fairly.

THE FLOW
  test.jsonl  ->  for each question: system prompt + user text  ->  Groq or Gemini
             ->  answer saved as a new column  ->  predictions.jsonl (updated)

HOW TO RUN  (you need a FREE key in a .env file or in Colab Secrets)
  pip install groq google-genai python-dotenv
  python api_baseline.py demo_data/test.jsonl demo_results/farm_predictions.jsonl --provider groq
  python api_baseline.py demo_data/test.jsonl demo_results/farm_predictions.jsonl --provider gemini
  python evaluate.py demo_results/farm_predictions.jsonl

Model names change over time. If you get "model not found", check:
  Groq:   https://console.groq.com/docs/models
  Gemini: https://ai.google.dev/gemini-api/docs/models
"""

# 'argparse' reads options like --provider groq from the command line
import argparse
# 'json' reads and writes .jsonl files
import json
# 'os' reads API keys from the environment
import os
# 'time' lets us wait between calls (free keys have speed limits)
import time

# try to read keys from a .env file (works without it too)
try:
    # python-dotenv reads .env into the environment
    from dotenv import load_dotenv
    # load GROQ_API_KEY / GEMINI_API_KEY
    load_dotenv()
# python-dotenv not installed
except ImportError:
    # fine: keys can also be set directly in the environment
    pass

# default model for each provider (change if the name has been retired)
DEFAULT_MODELS = {
    # Groq's big free model (70 billion parameters)
    "groq": "llama-3.3-70b-versatile",
    # Gemini alias that always points to the newest Flash model
    "gemini": "gemini-flash-latest",
}


# ---------------------------------------------------------------------
# the two providers
# ---------------------------------------------------------------------

# ask Groq one question and return the answer text
def ask_groq(client, model, system_prompt, user_text):
    # send system + user messages; temperature=0 = most stable answer
    reply = client.chat.completions.create(
        # which model to use
        model=model,
        # the conversation: instruction first, then the user's message
        messages=[{"role": "system", "content": system_prompt},
                  {"role": "user", "content": user_text}],
        # no randomness
        temperature=0,
    )
    # take the text out of the reply
    return reply.choices[0].message.content


# ask Gemini one question and return the answer text
def ask_gemini(client, model, system_prompt, user_text):
    # 'types' holds Gemini's settings classes
    from google.genai import types
    # send the user text; the system prompt goes in the config
    reply = client.models.generate_content(
        # which model to use
        model=model,
        # what the user says
        contents=user_text,
        # the instruction + no randomness
        config=types.GenerateContentConfig(system_instruction=system_prompt, temperature=0),
    )
    # the answer text ("" if Gemini returned nothing)
    return reply.text or ""


# build the right client for the chosen provider
def make_client(provider):
    # Groq
    if provider == "groq":
        # read the key
        key = os.getenv("GROQ_API_KEY")
        # stop with a clear message if it is missing
        if not key:
            # explain where to get it
            raise SystemExit("Set GROQ_API_KEY (free key: https://console.groq.com/keys)")
        # import the Groq package
        from groq import Groq
        # create the client and the ask-function
        return Groq(api_key=key), ask_groq
    # Gemini
    key = os.getenv("GEMINI_API_KEY")
    # stop with a clear message if it is missing
    if not key:
        # explain where to get it
        raise SystemExit("Set GEMINI_API_KEY (free key: https://aistudio.google.com/apikey)")
    # import the Google package
    from google import genai
    # create the client and the ask-function
    return genai.Client(api_key=key), ask_gemini


# ---------------------------------------------------------------------
# main
# ---------------------------------------------------------------------

# the main function
def main():
    # describe the command-line options
    parser = argparse.ArgumentParser(description="Add a big prompted model's answers to predictions.jsonl")
    # 1st argument: the test file (has the system prompt and questions)
    parser.add_argument("test_file")
    # 2nd argument: the predictions file to update (created if missing)
    parser.add_argument("predictions_file")
    # which provider
    parser.add_argument("--provider", choices=["groq", "gemini"], default="groq")
    # which model (optional)
    parser.add_argument("--model", default=None)
    # seconds to wait between calls (free keys allow only a few calls per minute)
    parser.add_argument("--wait", type=float, default=2.5)
    # read the options
    args = parser.parse_args()

    # the model to use: the one given, or the default for that provider
    model = args.model or DEFAULT_MODELS[args.provider]
    # column name in predictions.jsonl, e.g. "groq"
    column = args.provider
    # create the client
    client, ask = make_client(args.provider)

    # read the test questions
    with open(args.test_file, encoding="utf-8") as f:
        # one example per line
        tests = [json.loads(line) for line in f if line.strip()]
    # read the existing predictions, if the file exists
    if os.path.exists(args.predictions_file):
        # open it
        with open(args.predictions_file, encoding="utf-8") as f:
            # one row per line
            rows = [json.loads(line) for line in f if line.strip()]
    # no predictions file yet
    else:
        # start with input + reference only
        rows = [{"input": t["messages"][1]["content"], "reference": t["messages"][-1]["content"]} for t in tests]
    # both files must have the same number of questions in the same order
    if len(rows) != len(tests):
        # stop with a clear message
        raise SystemExit("test file and predictions file have a different number of lines")

    # ask every question
    for i, (test, row) in enumerate(zip(tests, rows), start=1):
        # the system prompt (first message)
        system_prompt = test["messages"][0]["content"]
        # the user's message (second message)
        user_text = test["messages"][1]["content"]
        # try up to 3 times (free keys sometimes say "too many requests")
        for attempt in range(3):
            # 'try' so one error doesn't stop everything
            try:
                # ask the model
                row[column] = ask(client, model, system_prompt, user_text).strip()
                # success: leave the retry loop
                break
            # any error (rate limit, network...)
            except Exception as e:
                # show what went wrong
                print(f"  question {i}: {type(e).__name__}, waiting 20s and retrying...")
                # wait before trying again
                time.sleep(20)
        # three failures: store an empty answer so the file stays complete
        else:
            # empty answer counts as wrong in evaluate.py
            row[column] = ""
        # progress line
        print(f"{i}/{len(tests)} done")
        # stay under the free speed limit
        time.sleep(args.wait)

    # save all rows back to the predictions file
    with open(args.predictions_file, "w", encoding="utf-8") as f:
        # one JSON object per line
        for row in rows:
            # ensure_ascii=False keeps Urdu letters readable
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    # tell the student what to do next
    print(f"\nAdded column '{column}' ({model}). Next: python evaluate.py {args.predictions_file}")


# run only when started directly
if __name__ == "__main__":
    # start the program
    main()
