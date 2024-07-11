# MongoDB
from pymongo.errors import PyMongoError
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Imports for the environmental variables
from dotenv import load_dotenv
import os

# Importing logger from loguru
from loguru import logger

# Environmental Variables
load_dotenv('.env')

# MongoDB
atlas_user = os.environ['ATLAS_USER']
atlas_pass = os.environ['ATLAS_PASS']

URI = f"mongodb+srv://{atlas_user}:{atlas_pass}@serverlessinstance1.2pjfhb1.mongodb.net/?retryWrites=true&w=majority&appName=ServerlessInstance1"

# Create a new client and connect to the server
client = MongoClient(URI, server_api=ServerApi('1'))
    
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    logger.info("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {e}")

# Setting up the database
db = client['crypt']

def upload_to_mongodb(collection_name: str, data: list):
    """
    Uploads a list of article data to a specified MongoDB collection, avoiding duplicates based on article_id.

    Args:
        collection_name (str): The name of the MongoDB collection to upload to.
        article_data (list): A list of dictionaries, each containing article data with an 'article_id' field.

    Returns:
        None
    """
    mongodb_collection = db[collection_name]

    existing_ids = set(mongodb_collection.distinct("data_id"))
    
    logger.debug(f"Inserting data into {collection_name}...")
    data_to_insert = [data_point for data_point in data if data_point["data_id"] not in existing_ids]
    
    if data_to_insert:
        try:
            mongodb_collection.insert_many(data_to_insert)
            logger.info(f"Inserted {len(data_to_insert)} data points.")
        except PyMongoError as e:
            logger.error(f"PyMongo error: {e}")
        except Exception as e:
            logger.error(f"General error: {e}")
    else:
        logger.info("No new data points to insert.")