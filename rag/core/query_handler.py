from ..core.short_term_memory import add_interaction, get_memory         # For managing short-term memory
from ..utils.search import get_relevant_chunks                           # For retrieving relevant chunks from the knowledge base
from ..utils.data_embedder import model as embedding_model               # SentenceTransformer model used for embeddings
from ..utils.evaluator import compute_cosine_similarity                  # Utility to compute cosine similarity between embeddings
import ollama                                                            # LLM interface (Ollama backend)

def handle_query(query, top_k=3):
    """
    Handle a user query by retrieving relevant document chunks,
    combining them with recent conversation history, generating a response using an LLM,
    storing the interaction in short-term memory, and evaluating relevance with cosine similarity.

    Args:
        query (str): The users question.
        top_k (int): Number of top document chunks to retrieve based on similarity.

    Returns:
        dict: Contains the LLM-generated answer, the retrieved chunks,
              and an evaluation report with cosine similarity scores.
    """


    # STEP 1: Retrieve short-term memory (recent Q&A interactions)
    memory = get_memory()

    # STEP 2: Retrieve top-K relevant chunks from the vector DB (long-term memory)
    chunks = get_relevant_chunks(query, top_k)

    # STEP 3: Prepare the document context from retrieved chunks
    context = "\n".join([c["text"] for c in chunks])

    # STEP 4: Reconstruct conversation history as a formatted string for the prompt
    conversation_history = ""
    for interaction in memory:
        conversation_history += f"Q: {interaction['query']}\nA: {interaction['answer']}\n\n"

    # STEP 5: Construct the LLM prompt combining history, context, and current query
    prompt = f"""
    You are a Tutor who teach school going kids.
    Answer the following question *only* using the provided context.
    If the answer is not present in the context exactly as it is then at first try to guess it based on the context.
    Return your answer in the same language as the question.
    The answer should be very short and precise.

    Conversation history:
    {conversation_history}

    Context:
    {context}

    Current question:
    {query}

    Answer:
    """

    # STEP 6: Call the LLM with the generated prompt using Ollama API
    response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
    answer = response["message"]["content"].strip()

    # STEP 7: Store the new interaction in short-term memory (volatile)
    add_interaction(query, answer, chunks)

    # STEP 8: Embed the user query for evaluation
    query_embedding = embedding_model.encode([f"query: {query}"])[0]

    # STEP 9: Extract embeddings of retrieved chunks for evaluation
    chunk_embeddings = [c["embedding"] for c in chunks]

    # STEP 10: Compute cosine similarity between query and each retrieved chunk
    similarity_scores, avg_similarity = compute_cosine_similarity(query_embedding, chunk_embeddings)

    # STEP 11: Return the full result with answer, retrieved chunks, and evaluation scores
    return {
        "answer": answer,
        "chunks": chunks,
        "evaluation": {
            "cosine_similarity_scores": similarity_scores,
            "average_score": avg_similarity
        }
    }
