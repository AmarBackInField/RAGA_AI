from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# def scrape_web_chunks(query: str, chunk_size: int = 1000, chunk_overlap: int = 200):
#     """
#     Search the web and return content chunks from top 5 search results.

#     Parameters:
#     - query (str): The search query
#     - chunk_size (int): Number of characters per chunk
#     - chunk_overlap (int): Number of overlapping characters between chunks

#     Returns:
#     - List[Document]: Chunks of crawled web content
#     """
#     try:
#         logger.info(f"Starting web search for query: {query}")
        
#         # Step 1: Get top 5 URLs from DuckDuckGo
#         results = []
#         with DDGS() as ddgs:
#             for r in ddgs.text(query, max_results=5):
#                 results.append(r["href"])
#                 logger.info(f"Found URL: {r['href']}")
#                 if len(results) == 5:
#                     break
        
#         if not results:
#             logger.warning("No search results found")
#             return []
        
#         # Step 2: Scrape HTML content from the URLs
#         documents = []
#         for url in results:
#             try:
#                 logger.info(f"Scraping content from: {url}")
#                 response = requests.get(url, timeout=10)
#                 response.raise_for_status()  # Raise an exception for bad status codes
                
#                 soup = BeautifulSoup(response.text, "html.parser")
                
#                 # Remove script and style elements
#                 for script in soup(["script", "style"]):
#                     script.decompose()
                
#                 # Get text and clean it
#                 text = soup.get_text(separator="\n", strip=True)
#                 text = " ".join(text.split())  # Normalize whitespace
                
#                 if not text.strip():
#                     logger.warning(f"No text content found in {url}")
#                     continue
                    
#                 logger.info(f"Successfully extracted {len(text)} characters from {url}")
#                 documents.append(Document(page_content=text, metadata={"source": url}))
#             except requests.RequestException as e:
#                 logger.error(f"Failed to fetch {url}: {str(e)}")
#             except Exception as e:
#                 logger.error(f"Error processing {url}: {str(e)}")
        
#         if not documents:
#             logger.warning("No documents were successfully scraped")
#             return []
        
#         # Step 3: Split content into chunks
#         logger.info(f"Splitting {len(documents)} documents into chunks")
#         splitter = RecursiveCharacterTextSplitter(
#             chunk_size=chunk_size,
#             chunk_overlap=chunk_overlap,
#             length_function=len,
#             is_separator_regex=False
#         )
        
#         chunks = splitter.split_documents(documents)
#         logger.info(f"Created {len(chunks)} chunks from {len(documents)} documents")
        
#         if not chunks:
#             logger.warning("No chunks were created after splitting")
#             return []
            
#         return chunks

#     except Exception as e:
#         logger.error(f"Error during web scraping: {str(e)}", exc_info=True)
#         return []
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def scrape_web_chunks(query: str, chunk_size: int = 1000, chunk_overlap: int = 200):
    """
    Search the web and return content chunks from top 5 search results using multithreading.

    Parameters:
    - query (str): The search query
    - chunk_size (int): Number of characters per chunk
    - chunk_overlap (int): Number of overlapping characters between chunks

    Returns:
    - List[Document]: Chunks of crawled web content
    """
    try:
        logger.info(f"Starting web search for query: {query}")
        
        # Step 1: Get top 5 URLs from DuckDuckGo
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=5):
                results.append(r["href"])
                logger.info(f"Found URL: {r['href']}")
                if len(results) == 5:
                    break

        if not results:
            logger.warning("No search results found")
            return []

        # Step 2: Define scraping function
        def scrape_url(url):
            try:
                logger.info(f"Scraping content from: {url}")
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                for script in soup(["script", "style"]):
                    script.decompose()
                text = soup.get_text(separator="\n", strip=True)
                text = " ".join(text.split())
                if not text.strip():
                    logger.warning(f"No text content found in {url}")
                    return None
                logger.info(f"Successfully extracted {len(text)} characters from {url}")
                return Document(page_content=text, metadata={"source": url})
            except requests.RequestException as e:
                logger.error(f"Failed to fetch {url}: {str(e)}")
            except Exception as e:
                logger.error(f"Error processing {url}: {str(e)}")
            return None

        # Step 3: Use multithreading to scrape URLs
        documents = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {executor.submit(scrape_url, url): url for url in results}
            for future in as_completed(future_to_url):
                doc = future.result()
                if doc:
                    documents.append(doc)

        if not documents:
            logger.warning("No documents were successfully scraped")
            return []

        # Step 4: Split content into chunks
        logger.info(f"Splitting {len(documents)} documents into chunks")
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False
        )
        chunks = splitter.split_documents(documents)
        logger.info(f"Created {len(chunks)} chunks from {len(documents)} documents")
        
        return chunks if chunks else []

    except Exception as e:
        logger.error(f"Error during web scraping: {str(e)}", exc_info=True)
        return []
