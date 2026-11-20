"""
cost_estimator.py  -  Module 11: what does MY fine-tuning cost?
================================================================
Designed by Engr Usman Hasan  (Bano Qabil Generative AI course)

WHY THIS FILE EXISTS
  Fine-tuning has three bills:
    1. TRAINING on a GPU            (one time)
    2. or TRAINING on a hosted API  (one time, priced per 1 million tokens)
    3. RUNNING the model every day  (every month, forever!)
  Everything depends on TOKENS (small pieces of words), so we count them first.

THE FLOW
  train.jsonl -> count tokens per example -> x epochs = training tokens
             -> put in prices (YOU look them up, they change often) -> the bills

HOW TO RUN
  python cost_estimator.py demo_data
  python cost_estimator.py demo_data --epochs 3 --train-seconds 420
  python cost_estimator.py demo_data --api-price 5 --run-price 0.6 --requests-per-day 500

  --train-seconds  : 'train_runtime' printed at the end of your Colab training
  --gpu-price      : $ per hour for a rented GPU (free Colab = 0)
  --api-price      : $ per 1M training tokens on a hosted fine-tuning service
  --run-price      : $ per 1M tokens to RUN a model (input + output, simple average)
All prices are YOUR inputs. Check the provider's pricing page on the day you calculate.
"""

# 'argparse' reads options like --epochs 3
import argparse
# 'json' reads the .jsonl files
import json
# 'os' builds file paths
import os

# the tokenizer of the model we fine-tune (used if 'transformers' is installed)
TOKENIZER = "Qwen/Qwen2.5-0.5B-Instruct"


# ---------------------------------------------------------------------
# STEP 1: a function that counts tokens
# ---------------------------------------------------------------------

# returns a function: text -> number of tokens
def make_counter():
    # 'try' the real tokenizer first (exact counts)
    try:
        # transformers is installed in Colab
        from transformers import AutoTokenizer
        # download/load the tokenizer (small, a few MB)
        tok = AutoTokenizer.from_pretrained(TOKENIZER)
        # tell the student which method is used
        print(f"Counting tokens with the real tokenizer ({TOKENIZER})")
        # count = length of the token id list
        return lambda text: len(tok(text)["input_ids"])
    # no transformers (or no internet): use a rule of thumb
    except Exception:
        # explain the fallback
        print("transformers not available: estimating 1 token = 4 characters")
        # about 4 characters per token
        return lambda text: len(text) // 4 + 1


# ---------------------------------------------------------------------
# STEP 2: count the tokens of the training file
# ---------------------------------------------------------------------

# returns (number of examples, list of tokens per example)
def count_dataset(path, count):
    # tokens of each example
    sizes = []
    # open the file
    with open(path, encoding="utf-8") as f:
        # one example per line
        for line in f:
            # skip empty lines
            if not line.strip():
                # next line
                continue
            # read the example
            example = json.loads(line)
            # join all message texts (system + user + assistant)
            text = " ".join(m["content"] for m in example["messages"])
            # count its tokens (+10 for the chat-template special tokens)
            sizes.append(count(text) + 10)
    # give back the list
    return sizes


# format dollars nicely: 0.0123 -> "$0.01"
def money(x):
    # two decimals, or "< $0.01" for tiny amounts
    return f"${x:,.2f}" if x >= 0.01 or x == 0 else "< $0.01"


# ---------------------------------------------------------------------
# main
# ---------------------------------------------------------------------

# the main function
def main():
    # describe the options
    p = argparse.ArgumentParser(description="Estimate fine-tuning and running cost")
    # folder with train.jsonl (and test.jsonl)
    p.add_argument("folder")
    # how many times the model reads the whole dataset
    p.add_argument("--epochs", type=int, default=3)
    # measured training time from Colab, in seconds
    p.add_argument("--train-seconds", type=float, default=0)
    # rented GPU price per hour (free Colab = 0)
    p.add_argument("--gpu-price", type=float, default=0)
    # hosted fine-tuning price per 1M training tokens
    p.add_argument("--api-price", type=float, default=0)
    # price per 1M tokens to RUN a model
    p.add_argument("--run-price", type=float, default=0)
    # how many customer messages per day the bot will answer
    p.add_argument("--requests-per-day", type=int, default=1000)
    # read the options
    a = p.parse_args()

    # the token counter
    count = make_counter()
    # count tokens in train.jsonl
    sizes = count_dataset(os.path.join(a.folder, "train.jsonl"), count)
    # tokens in one pass over the data
    per_epoch = sum(sizes)
    # total tokens the model reads during training
    total = per_epoch * a.epochs
    # average size of one example (= roughly one request when running)
    avg = per_epoch / len(sizes)

    # ---- report 1: the dataset
    print("\n1) YOUR DATASET")
    # number of examples
    print(f"   examples in train.jsonl     : {len(sizes)}")
    # average tokens
    print(f"   average tokens per example  : {avg:.0f}")
    # one epoch
    print(f"   tokens in one epoch         : {per_epoch:,}")
    # all epochs
    print(f"   training tokens ({a.epochs} epochs)  : {total:,}")

    # ---- report 2: training on a GPU
    print("\n2) TRAINING ON A GPU (one time)")
    # did the student give the measured time?
    if a.train_seconds:
        # convert seconds to hours
        hours = a.train_seconds / 3600
        # time used
        print(f"   your training time          : {a.train_seconds/60:.1f} minutes")
        # price (free Colab = 0)
        print(f"   cost at {money(a.gpu_price)}/hour        : {money(hours * a.gpu_price)}"
              + ("   (free Colab T4!)" if a.gpu_price == 0 else ""))
    # no time given yet
    else:
        # tell them where to find it
        print("   add --train-seconds <train_runtime from Colab> to calculate")

    # ---- report 3: training on a hosted API
    print("\n3) TRAINING ON A HOSTED FINE-TUNING API (one time)")
    # price given?
    if a.api_price:
        # cost = millions of tokens x price per million
        print(f"   {total/1e6:.3f}M tokens x {money(a.api_price)} per 1M = {money(total/1e6*a.api_price)}")
    # no price given
    else:
        # show the formula
        print(f"   cost = {total/1e6:.3f}M tokens x (price per 1M tokens). Add --api-price")

    # ---- report 4: running the model every month
    print("\n4) RUNNING THE MODEL (every month!)")
    # tokens per month = requests per day x 30 days x tokens per request
    monthly_tokens = a.requests_per_day * 30 * avg
    # print the volume
    print(f"   {a.requests_per_day:,} requests/day x 30 days x {avg:.0f} tokens = {monthly_tokens/1e6:.1f}M tokens/month")
    # price given?
    if a.run_price:
        # monthly bill
        print(f"   at {money(a.run_price)} per 1M tokens = {money(monthly_tokens/1e6*a.run_price)} per month")
    # no price given
    else:
        # show the formula
        print("   add --run-price to calculate the monthly bill")

    # the lesson
    print("\nLESSON: training is paid ONCE. Running is paid EVERY MONTH. "
          "A small fine-tuned model is often cheaper to run than a big prompted one.")


# run only when started directly
if __name__ == "__main__":
    # start the program
    main()
