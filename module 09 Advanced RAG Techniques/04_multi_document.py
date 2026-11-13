# ============================================================
#  04  MULTI-DOCUMENT  -  one question, two files
# ============================================================
# FLOW:  2-part question -> split into parts -> search each part
#        -> join the evidence -> check which files were used
# ------------------------------------------------------------

# bring in the functions we need
from easy_rag import load_chunks, current_only, smart_search, multi_search, show

# load chunks and drop the old (archived) files
chunks = current_only(load_chunks("farm_docs"))
# one question that needs TWO facts from TWO files
question = "What is the milk price and when do orders close?"

# try ONE search for both parts; look at the scores (below 0 = unsure)
show(smart_search(question, chunks, top_n=3), "ONE search for both parts")

# split the question into its two parts by hand
parts = ["What is the milk price?", "When do orders close?"]
# search each part separately and join the results (1 best piece per part)
evidence = multi_search(parts, chunks, k=1)
# print the joined evidence
show(evidence, "MULTI search: one per part")

# print the set of file names that supplied the evidence
print("\nFiles used:", sorted({p['source'] for p in evidence}))

# ---- YOUR TURN -------------------------------------------
# Make your own 2-part question:
#   "How many wanda bags are left and when does the vet come?"
# Write the parts list yourself and run multi_search.
