class CodebaseRetriever:
    """
    Improved retriever with better ranking logic for code vs docs.
    """

    def __init__(self, vector_store):
        self.vector_store = vector_store

    def retrieve(self, query, k=6):
        """
        Retrieve more candidates first, then filter intelligently.
        """

        # Step 1: fetch more results than needed
        results = self.vector_store.similarity_search(query, k=k * 2)

        # Step 2: rank results (code files get priority)
        ranked = sorted(
            results,
            key=self._score_chunk,
            reverse=True
        )

        # Step 3: return top k best chunks
        return ranked[:k]

    def _score_chunk(self, doc):
        """
        Heuristic scoring system to prioritize useful chunks.
        """

        source = doc.metadata.get("source", "")

        score = 0

        # PRIORITY 1: Python code files
        if source.endswith(".py"):
            score += 10

        # PRIORITY 2: core app logic files
        if any(x in source for x in ["main.py", "loader", "chunker", "vector", "retrieval"]):
            score += 5

        # PENALTY: README or docs
        if "README" in source or source.endswith(".md"):
            score -= 5

        # BONUS: longer code chunks usually more useful
        score += min(len(doc.page_content) / 1000, 3)

        return score

    def format_context(self, docs):
        """
        Convert retrieved docs into LLM-ready context.
        """

        context = ""

        for i, doc in enumerate(docs):
            source = doc.metadata.get("source", "unknown file")

            context += f"\n--- Chunk {i+1} ---\n"
            context += f"Source: {source}\n"
            context += f"{doc.page_content}\n"

        return context