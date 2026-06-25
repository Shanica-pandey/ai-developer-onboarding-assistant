import ast
from langchain_core.documents import Document


def split_documents(documents):
    """
    AST-based chunking for Python files.
    Extracts functions and classes as individual chunks.
    """

    chunks = []

    for doc in documents:
        source = doc.metadata.get("source", "")
        content = doc.page_content

        # Only apply AST parsing to Python files
        if not source.endswith(".py"):
            chunks.append(doc)
            continue

        try:
            tree = ast.parse(content)
        except Exception:
            # fallback if parsing fails
            chunks.append(doc)
            continue

        # Extract function and class definitions
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                chunk = _extract_node_chunk(node, content, source)
                if chunk:
                    chunks.append(chunk)

            elif isinstance(node, ast.ClassDef):
                chunk = _extract_node_chunk(node, content, source)
                if chunk:
                    chunks.append(chunk)

    return chunks


def _extract_node_chunk(node, full_source, file_path):
    """
    Extract source code for a specific AST node.
    """

    try:
        start_line = node.lineno - 1

        # Python 3.8+ has end_lineno
        end_line = getattr(node, "end_lineno", None)

        lines = full_source.split("\n")

        if end_line:
            code = "\n".join(lines[start_line:end_line])
        else:
            code = lines[start_line]

        return Document(
            page_content=code,
            metadata={
                "source": file_path,
                "name": node.name,
                "type": type(node).__name__
            }
        )

    except Exception:
        return None