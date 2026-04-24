"""Load ChromaDB index and retrieve top-k chunks with MMR reranking."""

from __future__ import annotations

import os
from dataclasses import dataclass

import chromadb
from dotenv import load_dotenv
from llama_index.core import Settings, StorageContext, VectorStoreIndex
from llama_index.core.vector_stores.types import VectorStoreQueryMode
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

load_dotenv()

CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_db")
EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
TOP_K = int(os.getenv("TOP_K", "5"))
MMR_LAMBDA = float(os.getenv("MMR_LAMBDA", "0.5"))
COLLECTION = "rag_qa"


@dataclass
class Chunk:
    text: str
    source: str
    score: float


_retriever = None


def _get_retriever():
    global _retriever
    if _retriever is not None:
        return _retriever

    Settings.embed_model = HuggingFaceEmbedding(model_name=EMBED_MODEL)
    Settings.llm = None

    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_collection(COLLECTION)
    vector_store = ChromaVectorStore(chroma_collection=collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)

    _retriever = index.as_retriever(
        similarity_top_k=TOP_K,
        vector_store_query_mode=VectorStoreQueryMode.MMR,
        vector_store_kwargs={"mmr_threshold": MMR_LAMBDA},
    )
    return _retriever


def retrieve(question: str) -> list[Chunk]:
    nodes = _get_retriever().retrieve(question)
    return [
        Chunk(
            text=n.node.get_content(),
            source=n.node.metadata.get("file_name", "unknown"),
            score=float(n.score or 0.0),
        )
        for n in nodes
    ]
