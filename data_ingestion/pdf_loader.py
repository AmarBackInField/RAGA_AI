from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_pdf_chunks(file_path: str, chunk_size: int = 1000, chunk_overlap: int = 200):
    """
    Load a PDF file and return text chunks using LangChain's PyPDFLoader.

    Parameters:
    - file_path (str): Path to the PDF file
    - chunk_size (int): Size of each text chunk
    - chunk_overlap (int): Overlap between chunks

    Returns:
    - List[Document]: List of document chunks
    """
    try:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        chunks = splitter.split_documents(documents)
        return chunks

    except Exception as e:
        print(f"Error loading or splitting PDF: {e}")
        return []
