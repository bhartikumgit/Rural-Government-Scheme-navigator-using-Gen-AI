"""
embed.py — Embedding pipeline for Rural Scheme Navigator
=========================================================
Loads schemes_seed.json, chunks each scheme into meaningful
text segments, embeds them using sentence-transformers, and
saves the FAISS index + a metadata lookup file.

GenAI concept: EMBEDDINGS
  Each scheme chunk is converted to a 384-dim dense vector
  capturing semantic meaning. Similar meaning = similar vector.
  This lets us find "schemes for poor farmers" even if the
  scheme text says "income support for cultivators".

Run:
    python rag/embed.py
"""

import json
import os
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

# ── Paths ──
DATA_PATH   = "data/schemes_seed.json"
INDEX_PATH  = "faiss_index/schemes.index"
META_PATH   = "faiss_index/chunks_meta.pkl"

# ── Embedding model ──
# all-MiniLM-L6-v2: 22M params, 384-dim, fast on CPU, Apache 2.0
# Downloads ~90MB on first run, cached after that
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def make_chunks(scheme: dict) -> list[dict]:
    """
    Chunking strategy: one chunk per scheme, combining all
    meaningful fields into a single rich text block.

    Why not split into smaller chunks?
    - Schemes are short (200-500 words each)
    - Keeping all fields together avoids context loss
    - Eligibility + benefits need to stay together for reasoning

    Each chunk carries full metadata for the eligibility engine.
    """
    # Build a rich text representation of the scheme
    text_parts = [
        f"Scheme: {scheme['scheme_name']}",
        f"Category: {scheme['category']}",
        f"State: {scheme['state']}",
        f"Ministry: {scheme['ministry']}",
        f"Description: {scheme['description']}",
        f"Benefits: {scheme['benefits']}",
    ]

    # Add eligibility as natural language for better semantic matching
    elig = scheme.get("eligibility", {})
    elig_parts = []
    if elig.get("occupation"):
        elig_parts.append(f"For: {', '.join(elig['occupation'])}")
    if elig.get("max_annual_income"):
        elig_parts.append(f"Income below Rs. {elig['max_annual_income']:,}")
    if elig.get("caste_category"):
        elig_parts.append(f"Caste: {', '.join(elig['caste_category'])}")
    if elig.get("residence"):
        elig_parts.append(f"Residence: {elig['residence']}")
    if elig.get("min_age"):
        elig_parts.append(f"Minimum age: {elig['min_age']}")
    if elig.get("max_age"):
        elig_parts.append(f"Maximum age: {elig['max_age']}")
    if elig_parts:
        text_parts.append("Eligibility: " + "; ".join(elig_parts))

    # Add tags for additional semantic signal
    if scheme.get("tags"):
        text_parts.append(f"Tags: {', '.join(scheme['tags'])}")

    chunk_text = "\n".join(text_parts)

    return [{
        "chunk_text":   chunk_text,
        "scheme_id":    scheme["scheme_id"],
        "scheme_name":  scheme["scheme_name"],
        "state":        scheme["state"],
        "category":     scheme["category"],
        "eligibility":  scheme["eligibility"],
        "benefits":     scheme["benefits"],
        "benefit_amount": scheme.get("benefit_amount"),
        "documents":    scheme.get("documents", []),
        "apply_steps":  scheme.get("apply_steps", []),
        "apply_url":    scheme.get("apply_url"),
        "ministry":     scheme["ministry"],
    }]


def build_index():
    """Load schemes, chunk, embed, and save FAISS index."""

    # ── Load schemes ──
    print(f"Loading schemes from {DATA_PATH}...")
    with open(DATA_PATH, encoding="utf-8") as f:
        schemes = json.load(f)
    print(f"  Loaded {len(schemes)} schemes")

    # ── Chunk ──
    print("Chunking schemes...")
    all_chunks = []
    for scheme in schemes:
        all_chunks.extend(make_chunks(scheme))
    print(f"  Created {len(all_chunks)} chunks")

    # ── Embed ──
    # GenAI concept: the model converts text → 384-dim float vector
    # First run downloads model weights (~90MB) to ~/.cache/huggingface
    print(f"Loading embedding model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)

    print("Embedding chunks (this takes ~30s on CPU)...")
    texts = [c["chunk_text"] for c in all_chunks]

    # batch_size=32 balances memory and speed on CPU
    embeddings = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True,
        normalize_embeddings=True  # L2 normalize for cosine similarity via dot product
    )
    print(f"  Embeddings shape: {embeddings.shape}")  # (28, 384)

    # ── Build FAISS index ──
    # GenAI concept: FAISS stores vectors and enables fast nearest-neighbor search
    # IndexFlatIP = Inner Product (= cosine similarity since vectors are normalized)
    dim = embeddings.shape[1]  # 384
    index = faiss.IndexFlatIP(dim)
    index.add(np.array(embeddings, dtype=np.float32))
    print(f"  FAISS index built: {index.ntotal} vectors, dim={dim}")

    # ── Save ──
    os.makedirs("faiss_index", exist_ok=True)
    faiss.write_index(index, INDEX_PATH)
    print(f"  FAISS index saved → {INDEX_PATH}")

    with open(META_PATH, "wb") as f:
        pickle.dump(all_chunks, f)
    print(f"  Chunk metadata saved → {META_PATH}")

    print("\nDone. Index is ready for retrieval.")


if __name__ == "__main__":
    build_index()