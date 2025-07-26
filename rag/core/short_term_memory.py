# Global volatile memory storing last 5 interactions (query, answer, chunks)
# This will reset when the server restarts
MAX_MEMORY_SIZE = 5
short_term_memory = []

def add_interaction(query, answer, chunks):
    """
    Add a new interaction to the short-term memory.
    Keeps only the last MAX_MEMORY_SIZE items.
    """
    global short_term_memory
    short_term_memory.append({
        "query": query,
        "answer": answer,
        "chunks": chunks
    })
    # Keep only the last MAX_MEMORY_SIZE interactions
    short_term_memory = short_term_memory[-MAX_MEMORY_SIZE:]

def get_memory():
    """
    Retrieve the current short-term memory.
    Returns a list of dicts with keys: query, answer, chunks
    """
    return short_term_memory
