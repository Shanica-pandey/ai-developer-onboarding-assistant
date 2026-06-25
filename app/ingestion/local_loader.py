from pathlib import Path
from langchain_core.documents import Document

EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
}

SUPPORTED_EXTENSIONS = {
    ".py",
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
}


def load_project(project_path: str):
    root = Path(project_path)

    if not root.exists():
        raise FileNotFoundError(f"Project path does not exist: {project_path}")

    documents = []

    for file_path in root.rglob("*"):
        if not file_path.is_file():
            continue

        if any(part in EXCLUDED_DIRS for part in file_path.parts):
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        try:
            content = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "source": str(file_path.relative_to(root))
                },
            )
        )

    return documents