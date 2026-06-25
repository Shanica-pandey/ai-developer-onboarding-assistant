from ingestion.local_loader import load_project


def main():
    project_to_read = "."

    documents = load_project(project_to_read)

    print(f"Loaded {len(documents)} files.\n")

    for doc in documents[:5]:
        print(f"- {doc['path']}")


if __name__ == "__main__":
    main()