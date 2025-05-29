from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import Document
from langchain.chat_models import ChatOpenAI
from config.logging_config import setup_logging

import os
from dotenv import load_dotenv

# Set up logging
logger = setup_logging(__name__)

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.error("OPENAI_API_KEY not found in environment variables")
    raise ValueError("OPENAI_API_KEY not found in environment variables")

def get_faiss_retriever(chunks: list[Document]):
    """
    Store document chunks in FAISS and return a retriever using OpenAI Embeddings.

    Parameters:
    - chunks (list[Document]): List of text chunks

    Returns:
    - retriever: FAISS retriever object
    """
    try:
        logger.info(f"Creating FAISS retriever with {len(chunks)} chunks")
        
        if not chunks:
            logger.warning("No chunks provided for retriever creation")
            return None

        # Initialize OpenAI Embeddings
        logger.info("Initializing OpenAI Embeddings")
        embedding_model = OpenAIEmbeddings(api_key=api_key)

        # Create FAISS vector store
        logger.info("Creating FAISS vector store")
        vectorstore = FAISS.from_documents(chunks, embedding_model)
        logger.info(f"Created FAISS vector store with {len(chunks)} documents")

        
        # Return retriever
        logger.info("Creating retriever with k=5")
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
        logger.info("Successfully created retriever")
        
        return retriever

    except Exception as e:
        logger.error(f"Error creating FAISS retriever: {str(e)}", exc_info=True)
        return None
