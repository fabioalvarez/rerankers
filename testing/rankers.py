# This is the only rerankers import you'll ever need for inference
from rerankers import Reranker

# We want to compute the similarity between the query sentence
query = "A man is eating pasta."

# With all sentences in the corpus
corpus = [
    "A man is eating food.",
    "A man is eating a piece of bread.",
    "The girl is carrying a baby.",
    "A man is riding a horse.",
    "A woman is playing violin.",
    "Two men pushed carts through the woods.",
    "A man is riding a white horse on an enclosed ground.",
    "A monkey is playing drums.",
    "A cheetah is running behind its prey.",
]

# Cross-encoder
# ranker = Reranker(model_name='cross-encoder/ms-marco-MiniLM-L-6-v2', model_type="cross-encoder")

# ColBERT
# ranker = Reranker(model_name='colbert-ir/colbertv2.0', model_type="colbert")

# FlashRank
ranker = Reranker(model_name='ms-marco-MiniLM-L-12-v2', model_type="flashrank")

# Text-embeddings-inference
results = ranker.rank(query=query, docs=corpus)

for result in results:
    print(result)

if __name__ == "__main__":
    pass



