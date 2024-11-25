from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI

import os

# Set your OpenAI API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=openai_api_key)
from pinecone import Pinecone, ServerlessSpec

# Initialize FastAPI app
app = FastAPI()

# Initialize Pinecone using the new API and environment variables for security
pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY")
)

# Check if the index exists, otherwise create it
index_name = "student-submissions"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric='cosine',
        spec=ServerlessSpec(cloud='aws', region='us-east-1')
    )

index = pc.Index(index_name)

# Fallback implementation for OpenAI embeddings if LangChain's OpenAIEmbeddings is unavailable
class OpenAIEmbeddings:
    def __init__(self, api_key):
        self.api_key = api_key

    def embed_query(self, query):
        response = client.embeddings.create(model="text-embedding-ada-002",
        input=query)
        return response.data[0].embedding

# Initialize embeddings manually if LangChain's implementation is unavailable
embeddings = OpenAIEmbeddings(api_key=openai_api_key)

# Define the request body model
class QueryRequest(BaseModel):
    query: str  # Example: "Analyze Aditya's submission on Renaissance"

# Define the response model
class AnalysisResponse(BaseModel):
    analysis: str

def rag_retrieve_and_analyze(query: str) -> str:
    try:
        # Embed the query to get the vector representation
        query_vector = embeddings.embed_query(query)

        # Query Pinecone to retrieve relevant documents (dummy implementation for now)
        results = index.query(
            vector=query_vector,
            top_k=5,
            include_metadata=True,
        )['matches']

        retrieved_texts = []
        for result in results:
            metadata = result.get('metadata', {})
            text = metadata.get('text')

            if isinstance(text, str):
                retrieved_texts.append(text)
            elif isinstance(text, list):
                joined_text = " ".join(map(str, text))
                retrieved_texts.append(joined_text)
            else:
                raise ValueError("Each result must have a 'text' field in metadata that is either a string or a list of strings.")

        combined_texts = "\n\n".join(retrieved_texts)

        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Analyze the following student submissions:\n\n{combined_texts}\n\nProvide a detailed writing analysis."},
            {"role": "user", "content": (
                f"Analyze this text for readability, grammar, and complexity: {combined_texts}. "
                "Please return the result as a valid JSON object with the following keys: "
                "'readability_score' (a float), 'grade_level' (a string), 'lexical_diversity' (a float), "
                "'avg_sentence_length' (a float), 'grammar_issues' (a list of strings), "
                "'syntax_variety' (a string), and 'tense_consistency' (a boolean)."
            )}
        ]

        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=500,
        temperature=0.7)

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error during RAG retrieval or analysis: {e}")
        raise

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_query(request: QueryRequest):
    try:
        query = request.query

        analysis_result = rag_retrieve_and_analyze(query)

        return AnalysisResponse(analysis=analysis_result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))