from __future__ import annotations

import json
import os
import shutil
from typing import Any

import chromadb
from sentence_transformers import SentenceTransformer

from config import (
    CHROMA_PATH,
    CHUNKS_PATH,
    COLLECTION_NAME,
    EMBEDDING_MODEL_NAME,
    TOP_K,
)

REQUIRED_CHUNK_FIELDS = {
    "chunk_id",
    "document_name",
    "source_url",
    "chunk_position",
    "text",
}

EVALUATION_QUERIES = [
    "Which Broadway show is a comedic reimagining of Titanic featuring Céline Dion songs?",
    "When does Giant close, and who stars in it?",
    "Where is The Play That Goes Wrong currently playing?",
]


def load_chunks() -> list[dict[str, Any]]:
    """Load and validate chunks created by ingest.py."""
    if not os.path.isfile(CHUNKS_PATH):
        raise FileNotFoundError(
            f"Chunks file not found: {CHUNKS_PATH}\n"
            "Run: python ingest.py"
        )

    with open(CHUNKS_PATH, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    if not isinstance(chunks, list) or not chunks:
        raise ValueError("No chunks were found.\nRun: python ingest.py")

    seen_chunk_ids: set[str] = set()

    for index, chunk in enumerate(chunks):
        if not isinstance(chunk, dict):
            raise ValueError(f"Chunk {index} must be a JSON object.")

        missing = REQUIRED_CHUNK_FIELDS - set(chunk)
        if missing:
            raise ValueError(
                f"Chunk {index} is missing required field(s): {sorted(missing)}\n"
                "Run: python ingest.py"
            )

        if not str(chunk["text"]).strip():
            raise ValueError(f"Chunk {index} has empty text.")

        chunk_id = str(chunk["chunk_id"])
        if chunk_id in seen_chunk_ids:
            raise ValueError(f"Duplicate chunk_id detected: {chunk_id}")

        seen_chunk_ids.add(chunk_id)

    return chunks


def create_vector_store(
    chunks: list[dict[str, Any]],
) -> tuple[Any, SentenceTransformer]:
    """
    Embed chunks with all-MiniLM-L6-v2 and store them in ChromaDB
    with source metadata.
    """
    print(f"Loading embedding model: {EMBEDDING_MODEL_NAME}")
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    if os.path.isdir(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    client = chromadb.PersistentClient(path=CHROMA_PATH)

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    texts = [str(chunk["text"]) for chunk in chunks]

    print(f"Embedding {len(texts)} chunks...")
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        normalize_embeddings=True,
    ).tolist()

    collection.add(
        ids=[str(chunk["chunk_id"]) for chunk in chunks],
        documents=texts,
        embeddings=embeddings,
        metadatas=[
            {
                "document_name": str(chunk["document_name"]),
                "source_url": str(chunk["source_url"]),
                "chunk_position": int(chunk["chunk_position"]),
            }
            for chunk in chunks
        ],
    )

    return collection, model


def retrieve(
    query: str,
    collection: Any,
    model: SentenceTransformer,
    top_k: int = TOP_K,
) -> list[dict[str, Any]]:
    """Return top-k relevant chunks with source metadata and distance scores."""
    if not query.strip():
        raise ValueError("query must not be empty.")

    if top_k <= 0:
        raise ValueError("top_k must be greater than zero.")

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True,
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    retrieved: list[dict[str, Any]] = []

    for text, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        retrieved.append(
            {
                "text": text,
                "document_name": metadata["document_name"],
                "source_url": metadata["source_url"],
                "chunk_position": metadata["chunk_position"],
                "distance": float(distance),
            }
        )

    return retrieved


def print_retrieval_results(
    query: str,
    retrieved_chunks: list[dict[str, Any]],
) -> None:
    """Print retrieved chunks so relevance can be manually reviewed."""
    print("\n" + "=" * 100)
    print(f"QUERY: {query}")
    print("=" * 100)

    for rank, chunk in enumerate(retrieved_chunks, start=1):
        print(f"\nRESULT {rank}")
        print(f"Document: {chunk['document_name']}")
        print(f"Source URL: {chunk['source_url']}")
        print(f"Chunk position: {chunk['chunk_position']}")
        print(f"Distance: {chunk['distance']:.4f}")
        print("Text:")
        print(chunk["text"])
        print("-" * 100)


def main() -> None:
    """Build ChromaDB and test retrieval with evaluation queries."""
    chunks = load_chunks()
    print(f"Loaded {len(chunks)} chunks from: {CHUNKS_PATH}")

    collection, model = create_vector_store(chunks)
    print(f"Stored {collection.count()} chunks in ChromaDB at: {CHROMA_PATH}")

    for question in EVALUATION_QUERIES[:3]:
        results = retrieve(question, collection, model, top_k=TOP_K)
        print_retrieval_results(question, results)


if __name__ == "__main__":
    main()