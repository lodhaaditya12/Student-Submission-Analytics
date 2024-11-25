import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
from pinecone import Pinecone, ServerlessSpec
import pdfplumber

# Set your OpenAI and Pinecone API keys from environment variables
pinecone_api_key = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone client using the new API
pc = Pinecone(api_key=pinecone_api_key)

# Define the index name (create the index if it doesn't exist)
index_name = "student-submissions"

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric='cosine',
        spec=ServerlessSpec(cloud='aws', region='us-east-1')
    )

index = pc.Index(index_name)

# Path to the PDF file
pdf_file_path = "Aditya's submission on Renaissance.pdf"

if not os.path.exists(pdf_file_path):
    print(f"Error: The file '{pdf_file_path}' does not exist.")
    exit(1)

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Function to chunk text into smaller parts
def chunk_text(text, chunk_size=1000):
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return [chunk for chunk in chunks if chunk.strip()]

# Function to validate and fix metadata before upserting
def validate_text_metadata(vectors_to_upsert):
    for vector in vectors_to_upsert:
        metadata = vector['metadata']
        if isinstance(metadata['text'], list):
            # If the text field is a list, join it into a single string
            print(f"Warning: List detected in metadata, auto-correcting: {metadata['text']}")
            metadata['text'] = " ".join(map(str, metadata['text']))
            print("Corrected metadata text:", metadata['text'])
        elif not isinstance(metadata['text'], str):
            # If the text field isn't a string, raise an error
            print(f"Error: Unexpected data type in metadata. Expected string, got {type(metadata['text'])}")
            raise ValueError("Metadata field 'text' must be a string.")
    return vectors_to_upsert

# Extract text from the PDF file
pdf_text = extract_text_from_pdf(pdf_file_path)

# Chunk the extracted text into smaller parts
chunks = chunk_text(pdf_text)

# Prepare vectors for upsertion
vectors_to_upsert = []
for i, chunk in enumerate(chunks):
    if not isinstance(chunk, str):
        raise ValueError(f"Chunk {i} is not a string: {chunk}")
    # Generate embedding using OpenAI's embedding model (text-embedding-ada-002)
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=str(chunk)  # Ensure input is a string
    )

    embedding = response.data[0].embedding

    # Append vector with validated metadata
    vectors_to_upsert.append({
        "id": f"doc_{i}",
        "values": embedding,
        "metadata": {"text": str(chunk)}  # Ensure text is stored as a string
    })

# Validate all vectors before upserting them into Pinecone
validated_vectors = validate_text_metadata(vectors_to_upsert)

# Upsert validated vectors into Pinecone index
index.upsert(vectors=validated_vectors)

# Print success message and index stats
stats = index.describe_index_stats()
print(f"Successfully upserted {len(validated_vectors)} chunks.")
print("Index stats:", stats)