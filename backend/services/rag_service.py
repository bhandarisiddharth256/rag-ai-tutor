from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

index = None
stored_chunks = []


def chunk_text(text, chunk_size=100, overlap=20):
    words = text.split()
    chunks = []

    if not words:
        return []

    step = chunk_size - overlap

    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)

    return chunks


def store_embeddings(chunks):
    global index, stored_chunks

    if not chunks:
        print("No chunks to store")
        return

    embeddings = model.encode(chunks, normalize_embeddings=True)
    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]
    print("Storing chunks:", len(chunks))
    if index is None:
        index = faiss.IndexFlatIP(dimension)
  
    index.add(embeddings)
    stored_chunks.extend(chunks)


def search(query, k=5):
    global index, stored_chunks

    if index is None or len(stored_chunks) == 0:
        return ["No data available"]

    query_embedding = model.encode([query], normalize_embeddings=True)
    query_embedding = np.array(query_embedding).astype("float32")

    D, I = index.search(query_embedding, k)

    print("Scores:", D)
    print("Indexes:", I)

    results = []

    for idx in I[0]:
        if 0 <= idx < len(stored_chunks):
            results.append(stored_chunks[idx])

    # ✅ ALWAYS RETURN LIST
    return results if results else ["No relevant context found"]
