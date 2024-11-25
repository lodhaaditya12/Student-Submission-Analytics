System Design Overview
Components
FastAPI Application (ragbuilder.py):
Purpose: Provides an API endpoint to analyze student submissions using OpenAI's language model and Pinecone for vector storage and retrieval.
Key Functions:
rag_retrieve_and_analyze: Retrieves relevant documents from Pinecone and analyzes them using OpenAI's language model.
analyze_query: API endpoint to handle POST requests for analyzing queries.
2. PDF Text Extraction and Upsertion (upsert_to_pinecone.py):
Purpose: Extracts text from a PDF file, generates embeddings using OpenAI, and upserts them into a Pinecone index.
Key Functions:
extract_text_from_pdf: Extracts text from a given PDF file.
chunk_text: Splits the extracted text into smaller chunks for processing.
validate_text_metadata: Ensures metadata is correctly formatted before upsertion.
upsert: Inserts the processed text chunks as vectors into the Pinecone index.
Workflow
Text Extraction and Upsertion:
Extract text from a PDF document.
Chunk the text into manageable parts.
Generate embeddings for each chunk using OpenAI's embedding model.
Validate and upsert these embeddings into a Pinecone index.
Query Analysis:
Receive a query via the FastAPI endpoint.
Embed the query and retrieve relevant documents from Pinecone.
Use OpenAI's language model to analyze the retrieved documents.
Return the analysis as a structured JSON response.
Technologies Used
FastAPI: For building the web API.
OpenAI API: For generating text embeddings and performing text analysis.
Pinecone: For storing and retrieving vector embeddings.
pdfplumber: For extracting text from PDF files.
Pydantic: For data validation and serialization.
