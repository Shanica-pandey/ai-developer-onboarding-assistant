from pathlib import Path

# Folders we don't want to scan
EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
}

# File extensions we'll read for now
SUPPORTED_EXTENSIONS = {
    ".py",
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
}


def load_project(project_path: str):
    """
    Reads supported text files from a project directory.

    Returns:
        A list of dictionaries with:
        - path: relative file path
        - content: file contents
    """
    root = Path(project_path)

    if not root.exists():
        raise FileNotFoundError(f"Project path does not exist: {project_path}")

    documents = []

    for file_path in root.rglob("*"):
        if not file_path.is_file():
            continue

        # Skip excluded directories
        if any(part in EXCLUDED_DIRS for part in file_path.parts):
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        try:
            content = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            # Skip files that aren't valid UTF-8 text
            continue

        documents.append(
            {
                "path": str(file_path.relative_to(root)),
                "content": content,
            }
        )

    return documents