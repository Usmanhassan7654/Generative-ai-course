# ============================================================
#  02b  RRF BY HAND  -  how two ranked lists become one
# ============================================================
# FLOW:  get 2 ranked lists -> rank becomes points -> add points -> sort
#        then compare: (a) our RRF k=60  (b) k=0  (c) adding raw scores
# ------------------------------------------------------------

# bring in the two search functions
from easy_rag import load_chunks, semantic_search, keyword_search

# read all farm files and cut them into chunks
chunks = load_chunks("farm_docs")
# the question we use for the example
question = "How is barseem given to cows?"

# list 1: top 8 by meaning (each item has 'id', 'text', 'score')
meaning = semantic_search(question, chunks, k=8)
# list 2: top 8 by exact words
words = keyword_search(question, chunks, k=8)


# helper: find the rank (1, 2, 3 ...) of a chunk id in a list, or None
def rank_in(results, chunk_id):
    # go through the list with rank numbers starting at 1
    for rank, piece in enumerate(results, start=1):
        # is this the chunk we are looking for?
        if piece["id"] == chunk_id:
            # yes: return its rank
            return rank
    # not in this list at all
    return None


# helper: points for one rank using the RRF formula 1 / (k + rank)
def rrf_points(rank, k):
    # a piece that is not in the list gets 0 points
    if rank is None:
        # zero points
        return 0
    # the RRF formula
    return 1 / (k + rank)


# collect every chunk id that appears in at least one list (a set = no repeats)
all_ids = {p["id"] for p in meaning} | {p["id"] for p in words}
# a quick way to get a chunk's text from its id
text_of = {c["id"]: c["text"] for c in chunks}

# ---------------- (a) RRF with k = 60 (what easy_rag.py uses)
# print a table heading
print("\n(a) RRF, k = 60   ->  points = 1/(60+rank)")
# column titles
print(f"{'meaning':>8} {'words':>6} {'points':>8}   piece")
# rows = (total points, meaning rank, words rank, id) for every chunk
rows = []
# calculate the row for each chunk id
for cid in all_ids:
    # rank in the meaning list (or None)
    r1 = rank_in(meaning, cid)
    # rank in the words list (or None)
    r2 = rank_in(words, cid)
    # add the points from both lists
    total = rrf_points(r1, 60) + rrf_points(r2, 60)
    # store the row
    rows.append((total, r1, r2, cid))
# sort the rows from most points to least (row[0] = total points)
rows.sort(key=lambda row: row[0], reverse=True)
# print each row neatly ('-' means "not in this list")
for total, r1, r2, cid in rows:
    # show ranks or a dash, the total points, and the first 45 letters of text
    print(f"{r1 or '-':>8} {r2 or '-':>6} {total:>8.4f}   {text_of[cid][:45]}")

# ---------------- (b) same idea but k = 0  ->  points = 1/rank
# print a heading
print("\n(b) k = 0   ->  points = 1/rank   (rank 1 becomes TOO powerful)")
# empty list for the k = 0 results
rows0 = []
# calculate each chunk's total again, this time with k = 0
for cid in all_ids:
    # points from both lists using 1/rank
    total = rrf_points(rank_in(meaning, cid), 0) + rrf_points(rank_in(words, cid), 0)
    # store (total, id)
    rows0.append((total, cid))
# sort from most points to least
rows0.sort(key=lambda row: row[0], reverse=True)
# print the top 5
for total, cid in rows0[:5]:
    # total points and the start of the text
    print(f"{total:>8.3f}   {text_of[cid][:45]}")

# ---------------- (c) WRONG way: just add the raw scores
# print a heading
print("\n(c) Adding RAW scores (BM25 4.x + cosine 0.x)  ->  word list takes over")
# helper: the raw score of a chunk in a list, or 0 if it is not there
def raw_score(results, chunk_id):
    # look through the list
    for piece in results:
        # found the chunk?
        if piece["id"] == chunk_id:
            # return its original score (cosine or BM25)
            return piece["score"]
    # not in this list
    return 0


# empty list for the raw-score results
rows_raw = []
# add the two raw scores for every chunk
for cid in all_ids:
    # cosine score + BM25 score (different scales!)
    total = raw_score(meaning, cid) + raw_score(words, cid)
    # store (total, id)
    rows_raw.append((total, cid))
# sort from highest to lowest
rows_raw.sort(key=lambda row: row[0], reverse=True)
# print the top 5
for total, cid in rows_raw[:5]:
    # total raw score and the start of the text
    print(f"{total:>8.3f}   {text_of[cid][:45]}")

# WHAT TO NOTICE:
# (a) 'wanda' is #1 in ONE list only -> 0.0164. 'sick cow' is #5 and #2 in
#     BOTH lists -> 0.0315. With k=60, agreement between lists wins.
# (b) with k=0 the one-list winner 'wanda' jumps to #2: rank 1 is too strong.
# (c) with raw scores a milk-RECORD rule (SH-14) beats every meaning-only
#     result, because BM25 numbers are simply bigger.

# ---- YOUR TURN -------------------------------------------
# Change 60 to 10 in part (a). Does the order change?
