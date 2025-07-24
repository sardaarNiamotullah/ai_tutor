from .vector_search import semantic_search
import ollama


def generate_answer(query, top_k=3):
    # Step 1: Search top relevant chunks
    relevant_chunks = semantic_search(query, top_k=top_k)
    context = "\n".join([c["text"] for c in relevant_chunks])

    # Step 2: Build prompt
    prompt = f"""
    You are an expert assistant.

    Answer the following question *only* using the provided context.
    If the answer is not present in the context, respond with "I don't know".

    Return your answer in a single short sentence, in the same language as the question (Bangla or English).

    Context:
    {context}

    Question: {query}

    Answer:
    """

    # Step 3: Query Ollama
    response = ollama.chat(
        model="llama3.2", messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"].strip()
