from langchain.embeddings import HuggingFaceEmbeddings
from transformers import AutoModel

# Initialize the embeddings model
embeddings_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/msmarco-distilbert-dot-v5"
)

# Load the model configuration directly
hidden_size = embeddings_model.client.config.hidden_size

print(f"The hidden vector size is: {hidden_size}")
