"""
retriever.py — Hybrid retrieval for Rural Scheme Navigator
===========================================================
Combines dense (FAISS cosine) + sparse (BM25 keyword) retrieval
for robust scheme matching.

GenAI concept: HYBRID RAG RETRIEVAL
  Dense retrieval: finds semantically similar schemes even with
  different words. "Poor cultivator" matches "marginal farmer".

  Sparse retrieval (BM25): finds exact keyword matches.
  "MGNREGS" or "Kisan Credit Card" match precisely.

  Hybrid = best of both worlds. Neither alone is sufficient.

Run standalone test:
    python rag/retriever.py
"""

import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi

# ── Paths ──
INDEX_PATH = "faiss_index/schemes.index"
META_PATH  = "faiss_index/chunks_meta.pkl"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class SchemeRetriever:
    """
    Hybrid retriever: FAISS dense + BM25 sparse, score-fused.
    Call retrieve(query, k=5) to get top-k scheme chunks.
    """

    def __init__(self):
        print("Loading FAISS index...")
        self.index = faiss.read_index(INDEX_PATH)

        print("Loading chunk metadata...")
        with open(META_PATH, "rb") as f:
            self.chunks = pickle.load(f)

        print(f"Loading embedding model: {MODEL_NAME}")
        self.model = SentenceTransformer(MODEL_NAME)

        # Build BM25 index over tokenized chunk texts
        # BM25 works on token lists, not raw strings
        print("Building BM25 index...")
        tokenized = [
            c["chunk_text"].lower().split()
            for c in self.chunks
        ]
        self.bm25 = BM25Okapi(tokenized)

        print(f"Retriever ready. {len(self.chunks)} chunks indexed.\n")

    def retrieve(
        self,
        query: str,
        k: int = 5,
        dense_weight: float = 0.7,
        sparse_weight: float = 0.3,
    ) -> list[dict]:
        """
        Retrieve top-k most relevant scheme chunks for a query.

        Hybrid scoring:
            final_score = (dense_weight × dense_score)
                        + (sparse_weight × bm25_score_normalized)

        Args:
            query:         natural language query from user
            k:             number of results to return
            dense_weight:  weight for semantic similarity (0-1)
            sparse_weight: weight for keyword match (0-1)

        Returns:
            list of chunk dicts with added 'score' and 'rank' fields
        """

        # ── Dense retrieval via FAISS ──
        query_vec = self.model.encode(
            [query],
            normalize_embeddings=True
        ).astype(np.float32)

        # Retrieve top-20 candidates from FAISS (overretrieve, then re-rank)
        n_candidates = min(20, len(self.chunks))
        dense_scores, dense_indices = self.index.search(query_vec, n_candidates)
        dense_scores  = dense_scores[0]   # shape (n_candidates,)
        dense_indices = dense_indices[0]

        # ── Sparse retrieval via BM25 ──
        bm25_scores = self.bm25.get_scores(query.lower().split())

        # Normalize BM25 scores to [0, 1] for fair fusion
        bm25_max = bm25_scores.max()
        if bm25_max > 0:
            bm25_scores_norm = bm25_scores / bm25_max
        else:
            bm25_scores_norm = bm25_scores

        # ── Hybrid score fusion ──
        # Only score the FAISS candidates (not all 28) for efficiency
        scored = []
        for dense_rank, idx in enumerate(dense_indices):
            if idx < 0:  # FAISS returns -1 for unfilled slots
                continue
            hybrid_score = (
                dense_weight  * float(dense_scores[dense_rank]) +
                sparse_weight * float(bm25_scores_norm[idx])
            )
            scored.append((hybrid_score, idx))

        # Sort by hybrid score descending
        scored.sort(key=lambda x: -x[0])

        # ── Build result list ──
        results = []
        for rank, (score, idx) in enumerate(scored[:k]):
            chunk = dict(self.chunks[idx])  # copy to avoid mutating cache
            chunk["score"] = round(score, 4)
            chunk["rank"]  = rank + 1
            results.append(chunk)

        return results


def format_result(chunk: dict) -> str:
    """Pretty-print a single retrieved chunk for debugging."""
    lines = [
        f"  Rank {chunk['rank']} | Score: {chunk['score']} | {chunk['scheme_name']}",
        f"  State: {chunk['state']} | Category: {chunk['category']}",
        f"  Benefits: {chunk['benefits'][:120]}...",
    ]
    return "\n".join(lines)


# ── Standalone test ──
if __name__ == "__main__":
    retriever = SchemeRetriever()

    test_queries = [
        "schemes for farmers in Bihar",
        "schemes for unemployed youth who want to start a business",
        "health insurance for poor families",
    ]

    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: \"{query}\"")
        print(f"{'='*60}")
        results = retriever.retrieve(query, k=3)
        for r in results:
            print(format_result(r))
            print()