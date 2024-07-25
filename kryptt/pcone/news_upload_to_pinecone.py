import datetime
import os
import dotenv
from pymongo import MongoClient, UpdateOne
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
import asyncio

# Load environment variables
dotenv.load_dotenv()
print("Environment variables loaded.")

# MongoDB setup
ATLAS_USERNAME = os.getenv('ATLAS_USERNAME')
ATLAS_PASSWORD = os.getenv('ATLAS_PASSWORD')
MONGO_URI = f"mongodb+srv://{ATLAS_USERNAME}:{ATLAS_PASSWORD}@serverlessinstance1.2pjfhb1.mongodb.net/?retryWrites=true&w=majority&appName=ServerlessInstance1"
print("MongoDB URI constructed.")

# Pinecone setup
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_INDEX_NAME = "crypto-news"
print("Pinecone API key and index name set.")

# Initialize MongoDB client
mongo_client = MongoClient(MONGO_URI)
db = mongo_client['crypt']
collection = db['youtube_news']
print("MongoDB client initialized and connected to 'crypto_news' collection.")

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
print("Pinecone client initialized.")

# Initialize HuggingFace embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
print("HuggingFace embeddings initialized with model 'all-MiniLM-L6-v2'.")

def check_value(value):
    return value if value is not None else "Information not available"

def create_document(summary):
    print(f"Creating document for summary with title: {summary.get('title')}")
    return Document(
        page_content=check_value(summary.get('description')),
        metadata={
            "channel_title": check_value(summary.get('channel_title')),
            "video_url": check_value(summary.get('video_url')),
            "title": check_value(summary.get('title')),
            "published_date": check_value(summary.get('published_date')),
        }
    )

async def process_summaries():
    print("Fetching summaries without embeddings from MongoDB.")
    summaries = collection.find({
        "$or": [
            {"date_of_embedding": {"$exists": False}},
            {"date_of_embedding": None}
        ]
    })

    documents = [create_document(summary) for summary in summaries]
    print(f"Created {len(documents)} documents from summaries.")

    if documents:
        # Create or get the Pinecone index
        if PINECONE_INDEX_NAME not in pc.list_indexes():
            print(f"Creating Pinecone index: {PINECONE_INDEX_NAME}")
            try:
                pc.create_index(
                    name=PINECONE_INDEX_NAME,
                    dimension=384,  # Dimension for all-MiniLM-L6-v2
                    metric="cosine",
                    spec=ServerlessSpec(cloud="aws", region="us-east-1"),
                )
                print(f"Pinecone index {PINECONE_INDEX_NAME} created.")
            except Exception as e:
                print(f"Error creating Pinecone index: {e}")
        else:
            print(f"Pinecone index {PINECONE_INDEX_NAME} already exists.")

        # Upload documents to Pinecone
        print("Uploading documents to Pinecone.")
        vector_store = await asyncio.to_thread(
            PineconeVectorStore.from_documents,
            documents,
            embeddings,
            index_name=PINECONE_INDEX_NAME
        )
        print(f"Uploaded {len(documents)} documents to Pinecone.")

        # Update MongoDB to mark documents as embedded
        print("Updating MongoDB to mark documents as embedded.")
        update_operations = [
            UpdateOne(
                {"_id": doc.metadata.get("link")},
                {"$set": {"date_of_embedding": datetime.datetime.now()}}
            )
            for doc in documents
        ]
        await asyncio.to_thread(collection.bulk_write, update_operations)
        print("Updated MongoDB with embedding dates.")
    else:
        print("No new documents to process.")

async def main():
    print("Starting main process.")
    await process_summaries()
    print("Main process completed.")

if __name__ == "__main__":
    print("Script started.")
    asyncio.run(main())
    print("Script finished.")