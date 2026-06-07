from __future__ import annotations

import os
from typing import Any

import chromadb
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer

from config import (
    CHROMA_PATH,
    COLLECTION_NAME,
    EMBEDDING_MODEL_NAME,
    TOP_K,
)
from retriever import retrieve


MODEL_NAME = "llama-3.3-70b-versatile"


def load_vector_store() -> tuple[Any, SentenceTransformer]:
    """Load existing ChromaDB collection and embedding model."""
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_collection(name=COLLECTION_NAME)

    return collection, model


def format_context(chunks: list[dict[str, Any]]) -> str:
    """Format retrieved chunks for the LLM prompt."""
    context_parts = []

    for i, chunk in enumerate(chunks, start=1):
        context_parts.append(
            f"[Chunk {i}]\n"
            f"Document: {chunk['document_name']}\n"
            f"Source URL: {chunk['source_url']}\n"
            f"Text: {chunk['text']}"
        )

    return "\n\n".join(context_parts)


def get_sources(chunks: list[dict[str, Any]]) -> list[str]:
    """Return deduplicated source names and URLs from retrieved chunks."""
    sources = []

    for chunk in chunks:
        source = f"{chunk['document_name']} — {chunk['source_url']}"
        if source not in sources:
            sources.append(source)

    return sources


def generate_answer(question: str, chunks: list[dict[str, Any]]) -> str:
    """Generate a grounded answer using Groq."""
    load_dotenv()

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Missing GROQ_API_KEY. Add it to your .env file.")

    client = Groq(api_key=api_key)

    context = format_context(chunks)

    system_prompt = """
You are a grounded Broadway RAG assistant.

You must answer using ONLY the provided retrieved document context.

Rules:
- Do not use outside knowledge.
- Do not guess.
- Do not make assumptions.
- If the context does not contain enough information to answer the question, say exactly:
  "I don't have enough information on that."
- Keep the answer concise and directly tied to the retrieved context.
"""

    user_prompt = f"""
Retrieved context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt.strip()},
        ],
        temperature=0,
    )

    return response.choices[0].message.content.strip()


def ask(question: str) -> dict[str, Any]:
    """
    End-to-end RAG function:
    retrieve relevant chunks, generate grounded answer, and return sources.
    """
    if not question.strip():
        return {
            "answer": "Please enter a question.",
            "sources": [],
        }

    collection, model = load_vector_store()

    chunks = retrieve(
        query=question,
        collection=collection,
        model=model,
        top_k=TOP_K,
    )

    if not chunks:
        return {
            "answer": "I don't have enough information on that.",
            "sources": [],
        }

    answer = generate_answer(question, chunks)
    sources = get_sources(chunks)

    if answer == "I don't have enough information on that.":
        sources = []


if __name__ == "__main__":
    test_questions = [
        "Which Broadway show is a comedic reimagining of Titanic featuring Céline Dion songs?",
        "Where is The Play That Goes Wrong currently playing?",
        "What is the best pizza place in Manhattan?", # this is the off-domain question 
    ]

    for question in test_questions:
        result = ask(question)

        print("\n" + "=" * 80)
        print(f"Question: {question}")
        print("\nAnswer:")
        print(result["answer"])
        print("\nSources:")
        for source in result["sources"]:
            print(f"- {source}")