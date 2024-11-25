# Student-Submission-Analytics
# Student Submission Analysis System

This project provides a system for analyzing student submissions using OpenAI's language model and Pinecone for vector storage and retrieval. It consists of two main components: a FastAPI application for handling analysis requests and a script for extracting and upserting text from PDF files.

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

## License

This project is licensed under the MIT License.
