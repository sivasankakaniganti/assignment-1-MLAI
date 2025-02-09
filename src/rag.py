import fitz
import re
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_text_from_pdf(pdf_paths):
    text = ''
    for path in pdf_paths:
        doc = fitz.open(path)
        text += "\n".join([page.get_text("text") for page in doc])
    return text

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks


def get_embeddings(chunks):
    return np.array(embed_model.encode(chunks, normalize_embeddings=True))

def build_faiss_index(embeddings):
    d = embeddings.shape[1]  # Dimension of embeddings
    index = faiss.IndexFlatL2(d)
    index.add(embeddings)
    return index

def retrieve_chunks(query, index, chunks, top_k=3):
    query_embedding = embed_model.encode([query], normalize_embeddings=True)
    distances, indices = index.search(np.array(query_embedding), top_k)
    
    retrieved_texts = [chunks[i] for i in indices[0]]
    return retrieved_texts