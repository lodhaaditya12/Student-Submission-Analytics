# Student Submission Analysis System
Video Link: https://www.loom.com/share/62f85a9038a949df91be2aa09618a44f?sid=67c14caf-eeda-452f-bb54-f7d5fc6103a2 


This project provides a system for analyzing student submissions using OpenAI's language model and Pinecone for vector storage and retrieval. It consists of two main components: a FastAPI application for handling analysis requests and a script for extracting and upserting text from PDF files.

## System Design Overview

### Components

FastAPI Application (ragbuilder.py):
Purpose: Provides an API endpoint to analyze student submissions using OpenAI's language model and Pinecone for vector storage and retrieval.

### Key Functions:
1. rag_retrieve_and_analyze: Retrieves relevant documents from Pinecone and analyzes them using OpenAI's language model.
analyze_query: API endpoint to handle POST requests for analyzing queries.
2. PDF Text Extraction and Upsertion (upsert_to_pinecone.py):
Purpose: Extracts text from a PDF file, generates embeddings using OpenAI, and upserts them into a Pinecone index.
### Key Functions:
extract_text_from_pdf: Extracts text from a given PDF file.
chunk_text: Splits the extracted text into smaller chunks for processing.
validate_text_metadata: Ensures metadata is correctly formatted before upsertion.
upsert: Inserts the processed text chunks as vectors into the Pinecone index.

### Workflow
Text Extraction and Upsertion:
Extract text from a PDF document.
Chunk the text into manageable parts.
Generate embeddings for each chunk using OpenAI's embedding model.
Validate and upsert these embeddings into a Pinecone index.

### Query Analysis:
Receive a query via the FastAPI endpoint.
Embed the query and retrieve relevant documents from Pinecone.
Use OpenAI's language model to analyze the retrieved documents.
Return the analysis as a structured JSON response.

### Technologies Used
FastAPI: For building the web API.
OpenAI API: For generating text embeddings and performing text analysis.
Pinecone: For storing and retrieving vector embeddings.
pdfplumber: For extracting text from PDF files.
Pydantic: For data validation and serialization.




## Components

### 1. FastAPI Application (`ragbuilder.py`)

- **Endpoint**: `/analyze`
- **Method**: POST
- **Request Body**: JSON object with a `query` field.
- **Response**: JSON object containing the analysis of the query.

#### Key Features

- Embeds queries and retrieves relevant documents from Pinecone.
- Analyzes retrieved documents using OpenAI's language model.
- Returns a detailed analysis including readability, grammar, and complexity.

### 2. PDF Text Extraction and Upsertion (`upsert_to_pinecone.py`)

- Extracts text from a specified PDF file.
- Chunks the text into smaller parts for processing.
- Generates embeddings using OpenAI's embedding model.
- Upserts the embeddings into a Pinecone index.

## Setup

### Prerequisites

- Python 3.7+
- OpenAI API key
- Pinecone API key

### Installation

1. Clone the repository.
2. Install the required packages:
   ```bash
   pip install fastapi openai pinecone-client pdfplumber pydantic
   ```
3. Set your OpenAI and Pinecone API keys as environment variables:
   ```bash
   export OPENAI_API_KEY='your-openai-api-key'
   export PINECONE_API_KEY='your-pinecone-api-key'
   ```

### Running the FastAPI Application

1. Navigate to the directory containing `ragbuilder.py`.
2. Start the FastAPI server:
   ```bash
   uvicorn ragbuilder:app --reload
   ```

### Running the PDF Text Extraction and Upsertion Script

1. Ensure the PDF file path is correctly set in `upsert_to_pinecone.py`.
2. Run the script:
   ```bash
   python upsert_to_pinecone.py
   ```

## Usage

- Use the `/analyze` endpoint to submit queries for analysis.
- Ensure the PDF text extraction script is run to populate the Pinecone index with data.

