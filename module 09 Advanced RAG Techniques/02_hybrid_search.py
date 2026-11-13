# ============================================================
#  02  HYBRID SEARCH  -  meaning + exact words
# ============================================================
# FLOW:  search by meaning  +  search by words  ->  merge with RRF
# ------------------------------------------------------------

# bring in the three search functions and the printer
from easy_rag import load_chunks, semantic_search, keyword_search, hybrid_search, show

# read all farm files and cut them into chunks
chunks = load_chunks("farm_docs")
# 'barseem' is a local word; the meaning model hardly knows it
question = "How is barseem given to cows?"

# search 1: by MEANING (embeddings), print the top 3
show(semantic_search(question, chunks, k=3), "Search by MEANING (embeddings)")
# search 2: by exact WORDS (BM25), print the top 3
show(keyword_search(question, chunks, k=3), "Search by WORDS (BM25)")
# search 3: both searches merged with RRF, print the top 3
show(hybrid_search(question, chunks, k=3), "HYBRID (both, merged with RRF)")

# WHAT TO NOTICE:
# meaning search puts 'wanda' first and barseem only at #3.
# word search finds the exact word 'barseem' at #1.
# hybrid keeps the best of both: barseem at #1.
# (Open 02b_rrf_by_hand.py to see HOW the merge is calculated.)

# ---- YOUR TURN -------------------------------------------
# 1) Try: "What does rule SH-14 say?"  (codes and IDs!)
# 2) Try: "Can I pay with JazzCash?"
#    Which search wins each time? Make a small table in your notebook.
