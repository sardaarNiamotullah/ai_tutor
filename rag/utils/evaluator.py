from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def compute_cosine_similarity(query_embedding, chunk_embeddings):
    """
    📐 Computes cosine similarity between the user's query embedding and
    the embeddings of retrieved document chunks.

    Cosine similarity measures how close the direction of two vectors are.
    The closer the angle, the more semantically similar the texts.

    Args:
        query_embedding (List[float]):
            A 1D vector (usually 384-d) representing the query's semantic meaning.

        chunk_embeddings (List[List[float]]):
            A list of vectors (same shape) representing document chunks.

    Returns:
        Tuple[
            List[float],  # Individual cosine similarity scores (one per chunk)
            float         # Average of all similarity scores
        ]
    """

    # -------------------------------------------------------------
    # ✅ Handle edge case: no chunk embeddings (e.g., empty DB)
    # -------------------------------------------------------------
    if not chunk_embeddings:
        return [], 0.0

    # -------------------------------------------------------------
    # 🔄 Step 1: Convert inputs to numpy arrays
    # - query_vec shape: (1, 384)
    # - chunk_vecs shape: (top_k, 384)
    # -------------------------------------------------------------
    query_vec = np.array(query_embedding).reshape(1, -1)
    chunk_vecs = np.array(chunk_embeddings)

    # -------------------------------------------------------------
    # 📏 Step 2: Compute cosine similarity between query and each chunk
    # - cosine_similarity returns a matrix of shape (1, top_k)
    # -------------------------------------------------------------
    similarity_scores = cosine_similarity(query_vec, chunk_vecs)[0]

    # -------------------------------------------------------------
    # 🧮 Step 3: Calculate average similarity (for high-level evaluation)
    # -------------------------------------------------------------
    avg_score = float(np.mean(similarity_scores))  # Ensure plain float for JSON serialization

    # -------------------------------------------------------------
    # 📦 Step 4: Return list of scores + average
    # -------------------------------------------------------------
    return similarity_scores.tolist(), avg_score
