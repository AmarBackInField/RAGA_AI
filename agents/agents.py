from langgraph.graph import StateGraph, END
from langchain.schema import Document
from typing import List, Literal, TypedDict, Union
from config.prompt import prompt1,prompt2
from data_ingestion.api import load_stock_data
from data_ingestion.pdf_loader import load_pdf_chunks
from data_ingestion.web_scrapper import scrape_web_chunks
from models.entity import StockDataRequest
from rag.rag import get_faiss_retriever
from langchain_openai import ChatOpenAI
from config.logging_config import setup_logging
import os
from dotenv import load_dotenv
load_dotenv()

# Set up logging
logger = setup_logging(__name__)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.error("OPENAI_API_KEY not found in environment variables")
    raise ValueError("OPENAI_API_KEY not found in environment variables")
llm = ChatOpenAI(model="gpt-4.1-mini", api_key=api_key, temperature=0.1)

# Define state
class RAGState(TypedDict):
    mode: Literal["pdf", "web", "yfinance"]
    input_data: str  # file_path, query, or ticker symbol
    chunks: List[Document]
    retriever: object
    final_answer: str


# STEP 1: Load Data
def load_data(state: RAGState) -> RAGState:
    logger.info(f"Loading data in {state['mode']} mode with input: {state['input_data']}")
    try:
        if state["mode"] == "pdf":
            logger.info(f"Loading PDF from: {state['input_data']}")
            chunks = load_pdf_chunks(state["input_data"])
        elif state["mode"] == "web":
            logger.info(f"Scraping web for query: {state['input_data']}")
            chunks = scrape_web_chunks(state["input_data"])
        elif state["mode"] == "yfinance":
            llm_params=llm.with_structured_output(StockDataRequest)
            prompt=prompt2(state["input_data"])
            response=llm_params.invoke(prompt)
            logger.info(f"Loading stock data for ticker: {response}")
            
            df = load_stock_data(response.ticker, response.period, response.interval)
            if df is None:
                logger.error(f"Failed to load stock data for {state['input_data']}")
                return {**state, "chunks": [], "final_answer": "Failed to load stock data"}
            text = df.to_csv(index=False)
            chunks = [Document(page_content=text)]
        else:
            logger.error(f"Invalid mode: {state['mode']}")
            raise ValueError("Invalid mode")

        logger.info(f"Successfully loaded {len(chunks)} chunks")
        return {**state, "chunks": chunks}
    except Exception as e:
        logger.error(f"Error in load_data: {str(e)}", exc_info=True)
        return {**state, "chunks": [], "final_answer": f"Error loading data: {str(e)}"}


# STEP 2: Generate Retriever
def create_retriever(state: RAGState) -> RAGState:
    logger.info("Creating retriever from chunks")
    try:
        if not state["chunks"]:
            logger.warning("No chunks available for retriever creation")
            return {**state, "retriever": None, "final_answer": "No content available to create retriever"}
        
        retriever = get_faiss_retriever(state["chunks"])
        if retriever is None:
            logger.error("Failed to create retriever")
            return {**state, "retriever": None, "final_answer": "Failed to create retriever"}
        
        logger.info("Successfully created retriever")
        return {**state, "retriever": retriever}
    except Exception as e:
        logger.error(f"Error in create_retriever: {str(e)}", exc_info=True)
        return {**state, "retriever": None, "final_answer": f"Error creating retriever: {str(e)}"}


# STEP 3: Run LLM Query
def analysis_agent(state: RAGState) -> RAGState:
    logger.info("Querying LLM with retrieved documents")
    try:
        if not state["retriever"]:
            logger.error("No retriever available for query")
            return {**state, "final_answer": "No retriever available for query"}

        question = state["input_data"] # could be dynamic
        print(question)
        logger.info(f"Retrieving relevant documents for question: {question}")
        docs = state["retriever"].get_relevant_documents(question)
        
        if not docs:
            logger.warning("No relevant documents retrieved")
            return {**state, "final_answer": "No relevant documents found"}
        
        logger.info(f"Retrieved {len(docs)} relevant documents")
        context = "\n\n".join([doc.page_content for doc in docs])
        prompt = prompt1(context=context, question=question)
        
        logger.info("Generating response from LLM")
        answer = llm.invoke(prompt).content
        logger.info("Successfully generated response")
        
        return {**state, "final_answer": answer}
    except Exception as e:
        logger.error(f"Error in query_llm: {str(e)}", exc_info=True)
        return {**state, "final_answer": f"Error generating response: {str(e)}"}

