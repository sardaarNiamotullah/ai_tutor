from ..utils.search import get_relevant_chunks                 # For retrieving top-k relevant chunks from DB
from ..utils.data_embedder import model as embedding_model     # SentenceTransformer for embedding the query
from ..utils.evaluator import compute_cosine_similarity        # Function to evaluate relevance of chunks
import ollama                                                  # Used to interact with local Ollama LLM (e.g., llama3.2)


def handle_query(query, top_k=3):
    """
    Handles a user query by:
    1. Retrieving relevant document chunks from the vector DB
    2. Generating a grounded response using the LLM (Ollama)
    3. Evaluating chunk-query relevance via cosine similarity

    Args:
        query (str): The users question in English or Bangla.
        top_k (int): Number of chunks to retrieve from DB for grounding.

    Returns:
        dict: {
            "answer": final generated response,
            "chunks": retrieved chunks (text + embedding + distance),
            "evaluation": {
                "cosine_similarity_scores": list[float],
                "average_score": float
            }
        }
    """

    # --------------------------------------------------------------------
    # 🔍 Step 1: Retrieve top-k relevant document chunks from the DB
    # --------------------------------------------------------------------
    print(f"[QueryHandler] 🔍 Searching top {top_k} chunks for: {query}")
    chunks = get_relevant_chunks(query, top_k=top_k)

    # Combine all top-k chunk texts into a single string to form LLM context
    context = "\n".join([c["text"] for c in chunks])

    # --------------------------------------------------------------------
    # 🧠 Step 2: Build the prompt for the LLM (grounded in the chunk context)
    # --------------------------------------------------------------------
    prompt = f"""
    You are an expert assistant.
    Answer the following question *only* using the provided context.
    If the answer is not present in the context exactly as it is then at first try to guess it based on the context.
    Return your answer in the same language as the question.
    The answer should be very short and precise.

    Context:
    {context}

    Question: {query}

    Answer:
    """

    # --------------------------------------------------------------------
    # 🤖 Step 3: Generate the answer using Ollama (e.g., LLaMA3 model)
    # --------------------------------------------------------------------
    response = ollama.chat(
        model="llama3.2", 
        messages=[{"role": "user", "content": prompt}]
    )
    answer = response["message"]["content"].strip()

    # --------------------------------------------------------------------
    # 📏 Step 4: Evaluate how relevant the chunks are to the query
    # - Encode the query into a vector
    # - Compare with each retrieved chunk’s embedding using cosine similarity
    # --------------------------------------------------------------------
    query_embedding = embedding_model.encode([f"query: {query}"])[0]
    chunk_embeddings = [c["embedding"] for c in chunks]

    similarity_scores, avg_similarity = compute_cosine_similarity(
        query_embedding, chunk_embeddings
    )

    # --------------------------------------------------------------------
    # 📦 Step 5: Return the result: answer + raw chunks + evaluation metrics
    # --------------------------------------------------------------------
    return {
        "answer": answer,
        "chunks": chunks,  # You can choose to hide this in API layer
        "evaluation": {
            "cosine_similarity_scores": similarity_scores,
            "average_score": avg_similarity
        }
    }
