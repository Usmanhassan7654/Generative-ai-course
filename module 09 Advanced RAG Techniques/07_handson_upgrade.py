# ============================================================
#  07  HANDS-ON  -  upgrade the bot and PROVE it got better
# ============================================================
# FLOW:  exam paper -> old bot takes exam -> new bot takes SAME exam
#        -> compare marks -> final answer with the new bot
# ------------------------------------------------------------

# bring in the functions we need
from easy_rag import (load_chunks, current_only, semantic_search, smart_search,
                      rewrite_query, ask_llm, show)

# read all farm files and cut them into chunks
chunks = load_chunks("farm_docs")

# the exam paper: (question, words the #1 piece MUST contain to get a mark)
test_paper = [
    # plain English price question
    ("What is the price of milk today?",          "Rs 220"),
    # same question in Roman Urdu
    ("aaj farm par doodh ka rate?",               "Rs 220"),
    # a staff rule asked in normal words
    ("How do staff correct a wrong milk record?", "SH-14"),
    # the same rule asked by its code
    ("What does rule SH-14 say?",                 "SH-14"),
    # a local word
    ("How is barseem given to cows?",             "barseem"),
    # Roman Urdu stock question
    ("wanda ki kitni boriyan bachi hain?",        "22 bags"),
    # very short Roman Urdu question
    ("order kab tak?",                            "7:00 PM"),
    # a brand name
    ("Can I pay with JazzCash?",                  "JazzCash"),
    # old file says Rs 15, current file says Rs 20
    ("How much extra for home delivery?",         "Rs 20"),
    # simple English question
    ("When does the vet come?",                   "Thursday"),
    # Roman Urdu delivery question
    ("ghar delivery ka rate kitna hai?",          "Rs 20"),
    # health rule
    ("Is milk sold from a cow on antibiotics?",   "antibiotics"),
]


# the OLD bot from Module 08: semantic search only
def old_bot(q):
    # top 3 pieces by meaning, from ALL files
    return semantic_search(q, chunks, k=3)


# the NEW bot from Module 09: every power-up together
def new_bot(q):
    # rewrite -> current files only -> hybrid + re-rank -> top 3
    return smart_search(rewrite_query(q), current_only(chunks), top_n=3)


# give the exam to one bot and return its marks
def exam(bot):
    # start at zero marks
    marks = 0
    # ask every question on the paper
    for q, must_have in test_paper:
        # text of the bot's #1 piece
        first = bot(q)[0]["text"]
        # True if the right words are inside it
        ok = must_have in first
        # True counts as 1, False as 0
        marks += ok
        # print PASS or FAIL for this question
        print(("  PASS " if ok else "  FAIL ") + q)
    # total marks for this bot
    return marks


# heading for the old bot
print("OLD BOT")
# old bot takes the exam
old = exam(old_bot)
# heading for the new bot
print("NEW BOT")
# new bot takes the SAME exam
new = exam(new_bot)
# show the scoreboard
print(f"\nSCOREBOARD   old bot: {old}/12   new bot: {new}/12")

# final answer for a 2-part question using the new bot for each part
q = "What is the milk price and when do orders close?"
# join the evidence from both parts and ask the LLM
print("\n" + ask_llm(q, new_bot("What is the milk price?") + new_bot("When do orders close?")))

# ---- YOUR TURN -------------------------------------------
# Add 3 new questions to test_paper (one in Roman Urdu!) and run again.
