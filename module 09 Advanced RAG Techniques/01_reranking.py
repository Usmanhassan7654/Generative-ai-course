# ============================================================
#  01  RE-RANKING  -  "Selectors pick 15, the coach picks the XI"
# ============================================================
# FLOW:  load chunks -> fast search (shortlist) -> re-rank -> compare
# ------------------------------------------------------------

# bring in the helper functions we need from easy_rag.py
from easy_rag import load_chunks, semantic_search, rerank, show

# read all farm files and cut them into small pieces (chunks)
chunks = load_chunks("farm_docs")
# the customer's question
question = "What is the price of milk today?"

# STEP 1 - fast search (same as Module 08): get a shortlist of 4 pieces
shortlist = semantic_search(question, chunks, k=4)
# print the shortlist in its original order
show(shortlist, "BEFORE: fast semantic search")

# STEP 2 - the re-ranker reads (question + piece) together for the SAME 4 pieces
best = rerank(question, shortlist, top_n=4)
# print the same pieces in their new order
show(best, "AFTER: re-ranked")

# WHAT TO NOTICE:
# the same 4 pieces come back, only the ORDER changed.
# 'Milk costs Rs 220 per litre' jumps from #3 to #1.

# ---- YOUR TURN -------------------------------------------
# 1) Change the question to "How do staff fix a wrong record?"
# 2) Try k=2 instead of k=4. Is the right answer still there?
#    (Re-ranking can only re-order what search already found!)
