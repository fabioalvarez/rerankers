import pandas as pd
from datasets import load_dataset
from uuid import uuid4
from langchain_core.documents import Document


class Documents:
    def __init__(self, path, max_documents, id_column, text_column, split="train", load_local=False):
        self.path = path
        self.max_documents = max_documents
        self.id_column = id_column
        self.text_column = text_column
        self.split = split
        self.uuids = []

        self.df = self.load_dataset_local() if load_local else self.load_dataset()
        self.formated = self.format_documents()


    def load_dataset(self):
        documents = load_dataset(self.path, split=self.split).remove_columns("image")
        df = pd.DataFrame(documents)
        df = df.loc[:self.max_documents]

        return df

    def load_dataset_local(self):
        df = pd.read_csv(self.path)
        df = df.loc[:self.max_documents]

        return df

    def format_documents(self):
        formated = []

        for idx in range(self.max_documents):
            doc = self.df.loc[idx]

            self.uuids.append(str(uuid4()))

            formated.append(
                Document(
                    page_content=doc[self.text_column],
                    metadata={"id": int(doc[self.id_column]), "source": "sim"},
                    id=idx,
                )
            )

        return formated

def not_relevant_products(results_df, relevant_products):
    results = results_df["id"].tolist()
    difference = set(results) - set(relevant_products)

    return results_df[results_df["id"].isin(list(difference))]

def filter_results(results_df, df, query: str):
    experiments = results_df["query"].unique().tolist()
    if query not in experiments:
        raise ValueError(f"Query {query} not found in experiments")

    final_result = results_df[results_df["query"] == query].iloc[-1]["results"]
    filtered_df = df[df["id"].isin(final_result)].copy()
    filtered_df["sort_id"] = pd.Categorical(filtered_df["id"], categories=final_result, ordered=True)
    filtered_df.sort_values('sort_id', inplace=True)

    return filtered_df

if __name__ == "__main__":
    pass