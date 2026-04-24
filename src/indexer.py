"""Build ChromaDB index from documents in CORPUS_PATH.

Run once to (re)build index:
    python -m src.indexer

Idempotent: drops collection `rag_qa` and rebuilds from scratch.
"""

from __future__ import annotations

import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from llama_index.core import Settings, SimpleDirectoryReader, StorageContext, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

load_dotenv()

CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_db")
CORPUS_PATH = os.getenv("CORPUS_PATH", "./docs")
EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
COLLECTION = "rag_qa"


def build_index() -> int:
    corpus = Path(CORPUS_PATH)
    if not corpus.exists() or not any(corpus.iterdir()):
        raise SystemExit(f"Empty corpus at {corpus}. Add .md/.txt files before indexing.")

    Settings.embed_model = HuggingFaceEmbedding(model_name=EMBED_MODEL)
    Settings.node_parser = SentenceSplitter(chunk_size=512, chunk_overlap=50)
    Settings.llm = None  # we call Claude directly in generator.py

    client = chromadb.PersistentClient(path=CHROMA_PATH)
    try:
        client.delete_collection(COLLECTION)
    except Exception:
        pass
    collection = client.create_collection(COLLECTION)

    vector_store = ChromaVectorStore(chroma_collection=collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    documents = SimpleDirectoryReader(str(corpus), recursive=True).load_data()
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
    index.storage_context.persist(persist_dir=CHROMA_PATH)

    return collection.count()


if __name__ == "__main__":
    n = build_index()
    print(f"Indexed {n} chunks into {COLLECTION} at {CHROMA_PATH}")
