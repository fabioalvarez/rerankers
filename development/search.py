from typing import List, Any, Dict
import pandas as pd
pd.set_option('display.max_rows', None)

from development import enums
from development.metrics import precision_at_k, recall_at_k
from development.retriever import VectorStore, BM25, EnsembleRetrievers
from development.tools import Documents

class Search:
    def __init__(self, vector_store: VectorStore, bm25: BM25, documents: Documents, reranker = None):
        self.bm25 = bm25
        self.vector_store = vector_store
        self.reranker = reranker
        self.documents = documents
        self.k_to_eval = enums.k_to_eval

    def retriever(self, retriever_type: str, k: int, hybrid_weights: List):
        match retriever_type:
            case "bm25":
                return self.bm25.retriever(k)
            case "similarity":
                return self.vector_store.retriever(k)
            case "hybrid":
                ensemble = EnsembleRetrievers(self.bm25, self.vector_store, hybrid_weights or [0.5, 0.5])
                return ensemble.retriever(k)
            case _:
                raise ValueError(f"{retriever_type} is not a valid retriever")

    def retrieve(self, query: str, retriever_type: str, k: int, hybrid_weights=None):
        retriever = self.retriever(retriever_type, k, hybrid_weights)
        return retriever.invoke(query)

    def rerank(self, query, results):
        # Format for ranking
        document_list, document_index = self.format_for_ranking(results)

        # Rank
        ranker_results = self.reranker.rank(query, document_list)

        return self.format_back(ranker_results, document_index)

    @staticmethod
    def format_for_ranking(result):
        document_list = []
        document_index_map = {}

        for idx, document in enumerate(result):
            document_list.append(document.page_content)
            document_index_map[idx] = document

        return document_list, document_index_map

    @staticmethod
    def format_back(ranker_results, document_index):
        return [document_index[result.doc_id] for result in ranker_results]

    def calculate_metrics(self, retriever_type: str, rerank: bool, experiments: Dict[str, Any], hybrid_weights=None):
        metrics = enums.metrics
        rerank = self.reranker and rerank

        for query, exp_relevant_results in experiments.items():
            max_relevant_products = len(exp_relevant_results)

            for k in self.k_to_eval:
                k, is_max = self.is_max_k(k, max_relevant_products)

                if rerank:
                    k = k * 10

                results = self.retrieve(query, retriever_type, k, hybrid_weights)

                if rerank:
                    k = k // 10
                    results = self.rerank(query, results)
                    results = results[:k]

                result_product_ids, source = self.format_result(results)

                metrics = self.build_metrics(
                    metrics,
                    query,
                    k,
                    max_relevant_products,
                    exp_relevant_results,
                    result_product_ids,
                    source,
                )

                if is_max:
                    break

        return pd.DataFrame(metrics)

    @staticmethod
    def format_result(results):
        product_ids = []
        source = []

        for result in results:
            product_ids.append(result.metadata["id"])
            source.append(result.metadata["source"])

        return product_ids, source

    @staticmethod
    def build_metrics(metrics, query, k , max_relevant_products, exp_relevant_results, result_product_ids, source):
        metrics["query"].append(query)
        metrics["k"].append(k)
        metrics["max_k"].append(max_relevant_products)
        metrics["precision"].append(precision_at_k(exp_relevant_results, result_product_ids, k))
        metrics["recall"].append(recall_at_k(exp_relevant_results, result_product_ids, k))
        metrics["results"].append(result_product_ids)
        metrics["source"].append(source)

        return metrics

    @staticmethod
    def is_max_k(k, max_relevant_products):
        if k > max_relevant_products:
            return max_relevant_products, True

        return k, False
