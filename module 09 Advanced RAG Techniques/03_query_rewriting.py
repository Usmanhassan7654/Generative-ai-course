# ============================================================
#  03  QUERY REWRITING  -  ask the question clearly
# ============================================================
# FLOW:  messy question -> rewrite -> search with rewrite
#        -> (later) answer the ORIGINAL question
# ------------------------------------------------------------

# bring in the functions we need
from easy_rag import load_chunks, semantic_search, rewrite_query, show

# read all farm files and cut them into chunks
chunks = load_chunks("farm_docs")
# the customer writes in Roman Urdu
question = "wanda ki kitni boriyan bachi hain?"

# rewrite it with the small dictionary in easy_rag.py
search_query = rewrite_query(question)
# show the original question
print("Original :", question)
# show the rewritten search query
print("Rewritten:", search_query)

# search with the ORIGINAL question, print top 2
show(semantic_search(question, chunks, k=2), "Searching the ORIGINAL")
# search with the REWRITTEN question, print top 2
show(semantic_search(search_query, chunks, k=2), "Searching the REWRITTEN")

# WHAT TO NOTICE:
# the score of the right piece jumps from about 0.26 to about 0.75!
# GOLDEN RULE:
#   rewritten question -> for SEARCH
#   original question  -> for the ANSWER (so the meaning never changes)

# ---- YOUR TURN -------------------------------------------
# 1) Try: "doodh ka rate kya hai?"
# 2) Add a new word to ROMAN_URDU inside easy_rag.py and test it.
# 3) With an API key in .env, try: rewrite_query(question, use_llm=True)
