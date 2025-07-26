# AI_Tutor

AI_Tutor is a Retrieval-Augmented Generation (RAG) system designed to answer user queries in both English and Bangla by retrieving relevant information from a knowledge base built on document chunks. It supports semantic search over PDF content, particularly focusing on the *HSC26 Bangla 1st Paper* book, and generates contextually accurate responses.

## Features

* **Multilingual Query Support:** Accepts and processes queries in English and Bangla.
* **Semantic Retrieval:** Retrieves relevant chunks of text from a vectorized document corpus using embedding-based similarity search.
* **Knowledge Base:** Builds and maintains a vector database of pre-processed, cleaned, and chunked PDF documents.
* **Memory Management:**
   * *Short-Term Memory:* Maintains recent user chat inputs for conversational context.
   * *Long-Term Memory:* Stores document embeddings persistently in a vector database.
* **Answer Generation:** Uses retrieved chunks to generate accurate answers.
* **Evaluation Metrics:** Supports cosine similarity scores evaluation for retrieval relevance.
* **REST API:** Lightweight API for interaction with the RAG system.



## 🚀 Getting Started

## System Prerequisites

Before running this application on your local machine, ensure the following tools are installed with the specified versions:

| Tool | Version | Purpose |
|------|----------------|---------|
| Python | 3.13+ | Core application runtime |
| pip | 25+ | Python package management |
| Django | 5+ | Backend framework |
| Ollama | 0.9+ | Local LLM runtime and model management |
| llama | 3.2 | Language model (installed via Ollama) |
| PostgreSQL | 14+ | Primary database |
| pgvector | 0.8+ | Vector similarity extension |


## !Caution

Before proceeding with the application setup, you must configure the database for long-term memory storage. **This step is critical** - skipping the database configuration will cause the application to crash on startup, as it attempts to embed PDF documents and store vector data in the pgvector database immediately upon initialization.

<hr/>

## Vector Database Setup: Long-Term Memory
```bash
# Connect to PostgreSQL and create the application database:
# Connect to PostgreSQL as your user
psql <your_user_name> -d postgres
```

```sql
-- Create the application database
CREATE DATABASE yourdatabasename;

-- Connect to the newly created database
\c yourdatabasename;

-- Enable Vector Extension
-- Install the pgvector extension for vector similarity operations:
CREATE EXTENSION IF NOT EXISTS vector;

-- Upon successful completion, you should see the message: `CREATE EXTENSION`
-- Verify that the extension has been installed correctly:
\dx
```

Your database is now ready with:
- ✅ Application database created
- ✅ pgvector extension enabled
- ✅ Vector similarity search capabilities available


## LLM Setup
Dowload and intall Ollama at your local environment from [here](https://ollama.com/)

```bash
# Check ollama is currectly installed on your systmem or not
ollama --version

# Pull the language model llama3.2
# This may take some depending on your internet speed
ollama pull llama3.2    

# Now run the LLM model
ollama run llama3.2
```

### Now it's time to install the applicaiton
## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/sardaarNiamotullah/ai_tutor
   cd ai_tutor
   ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    # If this do not work then try with this
    python3 -m venv env
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt # or pip3 install -r requirements.txt
    python3 -m venv env   
    ```

4. Apply migrations:

    ```bash
    python manage.py makemigrations      
    python manage.py migrate
    ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Project Structure

```
├── config/                         # Project settings and configurations
│   ├── settings.py                 # Django settings
│   ├── urls.py                     # URL routing
│
├── rag/                            # Core app for query handling
│   ├── models.py                   # Database models
│   ├── views.py                    # API views
│   ├── urls.py                     # App-specific URL patterns
│   │                     
│   ├── apps.py                     # Rag app configuration, Runs on StartUP
│   │                               # Change your PDF book name here to work with another book.
│   │ 
│   ├── core/                       # Core logic for query handling - RAG
│   │   ├── query_handler.py        # Query processing logic
│   │   ├── short_term_memory.py    # Short conversation memory
│   │
│   ├── pipeline/                   # Data ingestion pipeline
│   │   ├── ingest_pipeline.py      # PDF ingestion and processing
│   │
│   ├── utils/                      # Utility scripts
│   │   ├── search.py               # Vector similarity search functionality
│   │   ├── pdf_reader.py           # PDF text extraction utilities
│   │   ├── pdf_cleaner.py          # PDF content cleaning and preprocessing
│   │   ├── evaluator.py            # RAG system performance evaluation
│   │   ├── data_chunker.py         # Chunking PDF data
│   │   ├── data_embedder.py        # Embedding data
│
├── manage.py                       # Django management script
```


# API Testing and Usage

## Testing the RAG Query Endpoint

### Basic Query Testing

1. **Open Postman** or your preferred API testing tool

2. **Configure the request:**
   - **Method:** `POST`
   - **URL:** `http://127.0.0.1:8000/api/rag/query/`
   - **Headers:** `Content-Type: application/json`

3. **Request Body:**
   ```json
   {
     "query": "অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?"
   }
   ```

4. **Expected Response:**
   ```json
   {
     "answer": "শুম্ভুনাথ"
   }
   ```

### Enabling Evaluation Metrics

To view detailed evaluation metrics alongside the answer, you need to enable the evaluation response in the API.

1. **Navigate to:** `rag/views.py`

2. **Uncomment the evaluation fields** in the response:
   ```python
   return Response({
       "answer": result["answer"],               # LLM-generated answer
       # "chunks": result["chunks"],             # Retrieved document chunks (optional)
       # "evaluation": result["evaluation"]      # Cosine similarity scores
   })
   ```

3. **Enhanced Response Format:**
   ```json
   {
     "answer": "শুম্ভুনাথ",
     "evaluation": {
       "cosine_similarity_scores": [
         0.7398948669433594,
         0.7260565757751465,
         0.7255054116249084
       ],
       "average_score": 0.7304856181144714
     }
   }
   ```

### Response Fields Explanation

- **`answer`**: The generated response from the LLM
- **`chunks`**: Retrieved document segments used for context (useful for debugging)
- **`evaluation`**: Performance metrics including:
  - `cosine_similarity_scores`: Individual relevance scores for retrieved chunks
  - `average_score`: Overall relevance metric for the query-document matching

### Usage Notes

- The evaluation metrics help assess the quality of document retrieval and answer relevance
- Cosine similarity scores range from 0 to 1, with higher values indicating better semantic similarity
- Enable chunk visibility for transparency in the RAG process and debugging purposes




# Working with English Book

## Configuration Setup

### Switching to English Document

To configure the application to work with an English book instead of the default Bengali book:

1. **Navigate to the configuration file:**
   ```
   rag/apps.py
   ```

2. **Replace the existing line:**
   ```python
   # Change this line
   ingest_pdf_data("HSC26-Bangla1st-Paper.pdf")
   
   # To this line
   ingest_pdf_data("englishboi.pdf")
   ```

3. **Restart the server:**
   ```bash
   python manage.py runserver
   ```

## Sample Queries for English Book

**Query:** "What happened to the well of Zamzam over time?"  
**Answer:** "It disappeared beneath the sand."

**Query:** "How did Allah protect Abraham from the fire?"  
**Answer:** "Allah said \"O fire, be coolness and peace for Abraham.\""

**Query:** "Why was Hashim's son named 'Shaybah'?"  
**Answer:** "Because some of his hair was white, so it means \"greyhaired\"."


# Question & Answer Section

## PDF Text Extraction

**Q: What method or library did you use to extract text from the PDF, and did you encounter any formatting challenges during the process?**

**A:** I used PyMuPDF (fitz) for text extraction, as it is currently one of the most reliable and efficient libraries for parsing content from PDFs. I also experimented with pdfplumber to compare the results.

Yes, I encountered significant formatting challenges with the extracted content. PDF structure often lacks consistent formatting, which makes it difficult to extract clean and structured text. I explored various libraries and techniques to address these issues programmatically. While some tools offered partial solutions, none could fully resolve the formatting inconsistencies across different PDFs. A substantial amount of manual effort and custom logic was required to clean and standardize the extracted text.

## Text Chunking Strategy

**Q: What chunking strategy did you choose (e.g. paragraph-based, sentence-based, character limit)? Why do you think it works well for semantic retrieval?**

**A:** I used a character-limit-based chunking strategy with overlap (e.g., 1000 characters with 200-character overlap). This method ensures consistent chunk size, which is important for generating stable embeddings, while the overlap helps preserve context across chunks. It works well for semantic retrieval because it reduces the chance of splitting meaningful sentences or ideas, resulting in more accurate and relevant matches.

## Embedding Model Selection

**Q: What embedding model did you use? Why did you choose it? How does it capture the meaning of the text?**

**A:** I used the `paraphrase-multilingual-MiniLM-L12-v2` model from the SentenceTransformers library. I also experimented with other models like `paraphrase-multilingual-mpnet-base-v2` and `sagorsarker/bangla-sentence-embedding`. However, I found the MiniLM model more suitable for my project due to its balanced trade-off between performance and speed, and its strong multilingual support, especially for both English and Bangla.

This model captures the meaning of text by generating dense vector representations that preserve semantic similarity—texts with similar meanings are mapped to nearby points in the embedding space. This makes it highly effective for downstream tasks like semantic search and retrieval.

## Similarity Comparison and Storage

**Q: How are you comparing the query with your stored chunks? Why did you choose this similarity method and storage setup?**

**A:** I compare the query embedding with stored chunk embeddings using cosine similarity because it effectively measures the angular distance between vectors, focusing on semantic similarity regardless of magnitude. This makes it well-suited for text embeddings. For storage, I use the pgvector extension in PostgreSQL, which is open-source, highly optimized, and allows fast vector operations directly in the database, enabling efficient and scalable semantic search.

## Query Context and Relevance

**Q: How do you ensure that the question and the document chunks are compared meaningfully? What would happen if the query is vague or missing context?**

**A:** Firstly, if the system returns a relevant and accurate answer for the query, I can infer that the document chunks are being compared meaningfully. Additionally, I use cosine similarity scores to quantitatively measure the closeness between the query and chunk embeddings, ensuring semantic alignment.

If the query is vague or lacks sufficient context, the retrieval process may return less relevant or overly broad chunks because the embeddings generated won't capture a specific intent. This can lead to less precise answers or ambiguity in the response. To mitigate this, it's important to encourage more precise queries or implement query expansion techniques to enrich context before retrieval.

## Results Quality and Improvements

**Q: Do the results seem relevant? If not, what might improve them (e.g. better chunking, better embedding model, larger document)?**

**A:** For English queries related to English documents, the results are consistently relevant, often achieving nearly 100% accuracy in retrieving the correct chunks. However, for Bengali books and queries, the search frequently fails to fetch the most relevant top three chunks. To improve performance in Bengali, a more specialized and higher-quality embedding model tailored to the Bengali language is likely needed.

---

## Performance Summary

- **English Content**: ~100% accuracy in chunk retrieval
- **Bengali Content**: Lower accuracy, requires language-specific optimization
- **Embedding Model**: `paraphrase-multilingual-MiniLM-L12-v2`
- **Storage**: PostgreSQL with pgvector extension
- **Similarity Metric**: Cosine similarity