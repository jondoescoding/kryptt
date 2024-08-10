# Vectorstore
from pinecone import Pinecone

# Local
from llm import LLM

# Python
import dotenv
import os

# Guard railing
from pydantic import BaseModel, Field

# Langchain
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore

# Load environment variables 
print("Loading environment variables...")
dotenv.load_dotenv()

# GLOBALS
print("Setting up global variables...")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PC = Pinecone(api_key=PINECONE_API_KEY)
INDEX = PC.Index("crypto-news")
EMBEDDINGS = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
VECTORSTORE = vectorstore_pinecone = PineconeVectorStore(index=INDEX, embedding=EMBEDDINGS)

# CLASSES
class ArticleResponse(BaseModel):
    # Single Entry
    title: str = Field(description="Based on the given context you this should be the title of the given article")
    url: list[str] = Field(description="Based on the given context you this should be LINKs/URLs to the given articles")
    summary: str = Field(description="Using ONLY the given context, this should be a summary from the details using the article document data in a bullet list")
    

### FUNCTIONS ###
def vectorstore_search(user_query: str):
    print(f"Searching vectorstore for query: {user_query}")
    "Accepts a prompt and a vectorstore. Using the information provided they query the vectorstore to find information on news articles."
    return VECTORSTORE.similarity_search(query=user_query, k=3)


def generate_response(user_query: str):
    print(f"Generating response for user query: {user_query}")
    # Passes the user's question to the Pinecone vectorstore to search for content which matches
    context = vectorstore_search(user_query)
    print(f"Context retrieved...: {context}")
    
    # Convert context to a dictionary format
    context_dict = {
    "articles": [
        {
            "title": doc.metadata.get("title", "No title"),
            "url": doc.metadata.get("link", "No URL"),
            "content": doc.page_content,
            "upload_date": doc.metadata.get("published_date", "No date given"),
            "country": doc.metadata.get("country", "No country given"),
            "keywords": doc.metadata.get("keywords", "No keywords given")
        } for doc in context
        ]
    }
    print(f"length of dict: {len(context_dict)}")
    print(f"Context converted to dict: {context_dict}")
    
    # Controls what the output of the LLM will be
    output_parser = PydanticOutputParser(pydantic_object=ArticleResponse)
    print("Output parser initialized.")
    
    # Define the prompt template
    template = """
    <role>You are an expert Financial Analyst Expert</role>
    <objective>Your goal is to answer question on news articles which are sourced from the crypto news channels. Use your expertise in the field to answer the question based on the given context.</objective>
    
    <question>{question}</question>

    <context>{context}</context>
    
    <format>{format_instructions}</format>
    """
    
    prompt_template = PromptTemplate(
        template=template, 
        input_variable=["context", "question"],
        partial_variables={"format_instructions": output_parser.get_format_instructions()}
    )
    print("Prompt template created.")
    
    retrieval_chain = prompt_template | LLM.gpt4o_mini | output_parser
    print("Retrieval chain set up.")
    
    # Generate the response
    try:
        response = retrieval_chain.invoke(
            {
                "context": context_dict,
                "question": user_query
            }
        )
        print(f"Response generated")
    
    except Exception as e:
        print(f"Error occurred: {e}")
        return f"Error: {e}" 
    
    # Map each summary to its corresponding link
    summaries = response.summary.split('\n')
    summary_with_links = ""
    for i, summary in enumerate(summaries):
        if summary:
            link = response.url[i] if i < len(response.url) else "No URL available"
            summary_with_links += f"{summary}\nLink: {link}\n\n"
    
    return f"""
    Title: {response.title}
    \nURL: {response.url}
    \nSummary: {response.summary}
    """