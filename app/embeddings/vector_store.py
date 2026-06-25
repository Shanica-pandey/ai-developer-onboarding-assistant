from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.config import CHROMA_PERSIST_DIR, GEMINI_API_KEY


def get_embedding_model():
    """
    Create the embedding model used throughout the application.
    """
    return GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-2-preview",
        google_api_key=GEMINI_API_KEY,
    )


def create_vector_store(
    documents,
    persist_directory=CHROMA_PERSIST_DIR,
):
    """
    Create and persist a Chroma vector store from documents.
    """
    embeddings = get_embedding_model()

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_directory,
    )

    return vector_store