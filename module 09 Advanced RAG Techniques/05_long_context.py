# ============================================================
#  05  LONG CONTEXT  -  send the useful pages, not the whole book
# ============================================================
# FLOW:  find best piece -> add its neighbour -> pack inside a budget
# ------------------------------------------------------------

# bring in the functions we need
from easy_rag import load_chunks, current_only, smart_search, add_neighbours, pack_context, show

# load chunks and drop the old (archived) files
chunks = current_only(load_chunks("farm_docs"))

# A) How big would "send everything" be? Join all chunk texts together
everything = " ".join(c["text"] for c in chunks)
# count the words of the whole library
print("Whole library:", len(everything.split()), "words")

# B) Small chunks can cut a rule away from its condition
question = "What is the milk price?"
# take only the single best piece
best = smart_search(question, chunks, top_n=1)
# it has the price, but not WHERE the price applies
show(best, "Best piece only")

# bring the next piece from the same file as well
with_next = add_neighbours(best, chunks)
# now we also see 'only at the farm gate'
show(with_next, "Best piece + its neighbour")

# C) Put the pieces into a context with a 60-word budget
context, used = pack_context(with_next, max_words=60)
# print exactly what the LLM would receive
print("\nCONTEXT SENT TO LLM:\n" + context)
# print how much of the budget we used
print("Words used:", used, "of 60")

# ---- YOUR TURN -------------------------------------------
# Change max_words to 5. What gets dropped? Is the answer still complete?
