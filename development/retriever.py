from typing import List
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from development.tools import Documents
from langchain_chroma import Chroma

from abc import ABC, abstractmethod

class Retriever(ABC):

    @abstractmethod
    def retriever(self, rewrite_k: int):
        pass

    @abstractmethod
    def retrieve(self, query: str):
        pass

class BM25(Retriever):
    def __init__(self, documents: Documents, k: int = 10):
        self.document_list, self.metadata = self.format_documents(documents)
        self.__retriever = self.retriever(k)

    def retriever(self, rewrite_k: int):
        retriever = BM25Retriever.from_texts(self.document_list, metadatas=self.metadata)
        retriever.k = rewrite_k
        return retriever

    def retrieve(self, query: str):
        return self.__retriever.invoke(query)

    @staticmethod
    def format_documents(documents):
        document_list = []
        metadata = []

        for idx, document in enumerate(documents.formated):
            document_list.append(document.page_content)
            metadata.append({"id":document.metadata["id"],  "source": "bm25"})

        return document_list, metadata

class VectorStore(Retriever):
    def __init__(
            self,
            collection_name:str,
            embeddings,
            persist_path: str,
            documents: Documents,
            add_documents=False,
            k: int = 10,
    ):
        self.vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=embeddings,
            persist_directory=persist_path
        )

        if add_documents:
            self.vector_store.add_documents(
                documents=self.format_documents(documents),
                ids=documents.uuids,
            )

        self.__retriever = self.retriever(k)

    def retriever(self, rewrite_k):
        return self.vector_store.as_retriever(search_kwargs={"k": rewrite_k})

    def retrieve(self, query: str):
        return self.__retriever.invoke(query)

    @staticmethod
    def format_documents(documents: Documents):
        return documents.formated

class EnsembleRetrievers(Retriever):
    def __init__(self, bm25: BM25, vector_store: VectorStore, hybrid_weights: List = None, k: int = 10):
        self.__bm25 = bm25
        self.__vector_store = vector_store
        self.hybrid_weights = hybrid_weights or [0.0, 1]
        self.__retriever = self.retriever(k)

    def retriever(self, rewrite_k: int):
        # Divide k by 2 to split the k between the two retrievers
        k = rewrite_k // 2

        bm25_retriever = self.__bm25.retriever(k)
        vector_store_retriever = self.__vector_store.retriever(k)

        return EnsembleRetriever(
            retrievers=[bm25_retriever,vector_store_retriever],
            weights=self.hybrid_weights,
        )

    def retrieve(self, query: str):
        return self.__retriever.invoke(query)
