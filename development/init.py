from rerankers import Reranker
from development import enums
from development.search import Search
from development.tools import Documents
from development.retriever import Retriever, BM25, VectorStore
from development.experiments import experiments_factory
from langchain_huggingface import HuggingFaceEmbeddings

class Resources:
    def __init__(self, reranker_name: str = None, reranker_type: str = None):
        self.bm25 = None
        self.vector_store = None
        self.reranker = None
        self.documents = None
        self.experiments_map = {}
        self.reranker_name = reranker_name
        self.reranker_type = reranker_type

    def initialize_resources(self, add_documents=False, max_documents=5000):
        # Load documents
        self.documents = Documents(
            path="ashraq/fashion-product-images-small",
            max_documents=max_documents,
            id_column="id",
            text_column="productDisplayName",
        )

        # Initialize Embeddings
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': False}
        )

        # Initialize Vector Store
        self.vector_store = VectorStore(
            collection_name="search_ecommerce",
            embeddings=embeddings,
            persist_path="/Users/fabio.florez/Documents/external/search-ecommerce/chroma",
            documents=self.documents,
            add_documents=add_documents
        )

        # Initialize BM25
        self.bm25 = BM25(self.documents)

        if self.reranker_name:
            # Initialize Cross-Encoder
            self.reranker = Reranker(model_name=self.reranker_name, model_type=self.reranker_type)

        for experiment in enums.experiments:
            self.experiments_map[experiment] = experiments_factory(self.documents.df, experiment)

if __name__ == "__main__":
    # Initialize Process
    r = Resources(reranker_name='cross-encoder/stsb-distilroberta-base', reranker_type="cross-encoder")
    r.initialize_resources()

    # Initialize Search
    search = Search(r.vector_store, r.bm25, r.documents, r.reranker)

    metrics = search.calculate_metrics(
        retriever_type="similarity",
        rerank=True,
        experiments=r.experiments_map,
    )

    print(metrics)


