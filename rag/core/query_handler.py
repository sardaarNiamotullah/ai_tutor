from ..utils.search import get_relevant_chunks
import ollama

def handle_query(query, top_k=3):
    print(f"[QueryHandler] 🔍 Searching top {top_k} chunks for: {query}")
    chunks = get_relevant_chunks(query, top_k)
    context = "\n".join([c["text"] for c in chunks])

    prompt = f"""
    You are an expert assistant.
    Answer the following question *only* using the provided context.
    If the answer is not present in the context, respond with \"I don't know\".
    Return your answer in the same language as the question.

    Context:
    {context}

    Question: {query}

    Answer:
    """

    response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
    answer = response["message"]["content"].strip()

    print(f"[QueryHandler] 🧠 Answer: {answer}")
    return answer, chunks