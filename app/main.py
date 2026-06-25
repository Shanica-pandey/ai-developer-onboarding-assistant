from ingestion.local_loader import load_project
from indexing.chunker import split_documents


def main():
    documents = load_project(".")

    chunks = split_documents(documents)

    print(f"Loaded {len(documents)} files.")
    print(f"Created {len(chunks)} chunks.\n")

    for chunk in chunks[:3]:
        print("=" * 60)
        print(chunk.metadata)
        print(chunk.page_content[:250])
        print()


if __name__ == "__main__":
    main()