from app.embeddings.vector_store import create_vector_store
from app.ingestion.local_loader import load_project
from app.indexing.chunker import split_documents
from app.llm.generator import AnswerGenerator
from app.retrieval.retriever import CodebaseRetriever


def main():
    documents = load_project(".")
    chunks = split_documents(documents)

    print(f"Loaded {len(documents)} files.")
    print(f"Created {len(chunks)} chunks.")

    print("Creating vector store...")
    vector_store = create_vector_store(chunks)

    retriever = CodebaseRetriever(vector_store)
    llm = AnswerGenerator()

    print("\n🤖 AI Developer Assistant Ready!")

    while True:
        query = input("\nAsk a question (or 'exit'): ")

        if query.lower() == "exit":
            break

        results = retriever.retrieve(query)
        context = retriever.format_context(results)

        answer = llm.generate(query, context)

        print("\n--- AI Answer ---\n")
        print(answer)


if __name__ == "__main__":
    main()