import streamlit as st
from workflow.graph import build_rag_workflow
from config.logging_config import setup_logging
from helper.lingual_model import speech_to_text,text_to_speech
import os
from dotenv import load_dotenv

# Set up logging
logger = setup_logging(__name__)

# Load environment variables
load_dotenv()

# Initialize session state
if 'workflow' not in st.session_state:
    logger.info("Initializing workflow in session state")
    st.session_state.workflow = build_rag_workflow()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'current_mode' not in st.session_state:
    st.session_state.current_mode = "web"

def process_query(mode: str, input_data: str, question: str = None):
    """Process a query through the RAG workflow"""
    try:
        logger.info(f"Processing query in {mode} mode with input: {input_data}")
        
        state = {
            "mode": mode,
            "input_data": input_data,
            "chunks": [],
            "retriever": None,
            "final_answer": ""
        }
        
        # If a specific question is provided, update the state
        if question:
            state["question"] = question
            
        result = st.session_state.workflow.invoke(state)
        
        # Add to chat history
        st.session_state.chat_history.append({
            "mode": mode,
            "input": input_data,
            "question": question or "Summarize the content",
            "answer": result["final_answer"]
        })
        
        return result["final_answer"]
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}", exc_info=True)
        return f"Error: {str(e)}"

def main():
    st.set_page_config(
        page_title="RAG AI Assistant",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 RAG AI Assistant")
    
    # Sidebar for mode selection and settings
    with st.sidebar:
        st.header("Settings")
        
        # Mode selection
        mode = st.radio(
            "Select Mode",
            ["web", "pdf", "yfinance"],
            index=["web", "pdf", "yfinance"].index(st.session_state.current_mode)
        )
        st.session_state.current_mode = mode
        
        # Display chat history
        st.header("Chat History")
        for i, chat in enumerate(st.session_state.chat_history):
            with st.expander(f"Chat {i+1} - {chat['mode']}"):
                st.write(f"Input: {chat['input']}")
                st.write(f"Question: {chat['question']}")
                st.write(f"Answer: {chat['answer']}")
        
        # Clear chat history button
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Input area based on mode
        if mode == "web":
            st.subheader("Web Search")
            input_data = st.text_input(
                "Enter your search query",
                placeholder="e.g., Latest news about Tesla stock"
            )
        elif mode == "pdf":
            st.subheader("PDF Analysis")
            uploaded_file = st.file_uploader("Upload a PDF file", type=['pdf'])
            if uploaded_file:
                # Save the uploaded file temporarily
                temp_path = f"temp_{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getvalue())
                input_data = temp_path
            else:
                input_data = None
        else:  # yfinance mode
            st.subheader("Stock Analysis")
            input_data = st.text_input(
                "Enter your query it will automatically extract Historical Data",
                placeholder="E.g. Get me the Apple stock data for the past 3 months with weekly intervals"
            ).upper()
        
        # Optional question input
        question = st.text_input(
            "Optional: Enter a specific question:",
            placeholder="e.g., What are the key points?"
        )
        
        # Handle buttons
        process_clicked = st.button("Process", type="primary")
        mic_clicked = st.button("Mic")

        # Initialize input_data via mic if Mic button is clicked
        if mic_clicked:
            input_data = speech_to_text()

        # Common processing logic
        if process_clicked or mic_clicked:
            if input_data:
                with st.spinner("Processing..."):
                    answer = process_query(mode, input_data, question if question else None)
                    # Display the answer
                    st.markdown("### Answer")
                    st.write(answer)
                    text_to_speech(answer)

                    # Clean up temporary PDF file if in PDF mode
                    if mode == "pdf" and os.path.exists(input_data):
                        os.remove(input_data)
            else:
                st.warning("Please provide input data")



    
    with col2:
        # Display current mode information
        st.subheader("Current Mode Information")
        if mode == "web":
            st.info("""
            **Web Search Mode**
            - Searches the web for relevant information
            - Uses DuckDuckGo for search results
            - Processes and summarizes web content
            """)
        elif mode == "pdf":
            st.info("""
            **PDF Analysis Mode**
            - Upload and analyze PDF documents
            - Extracts and processes text content
            - Provides summaries and answers questions
            """)
        else:  # yfinance
            st.info("""
            **Stock Analysis Mode**
            - Analyze stock data from Yahoo Finance
            - Enter stock ticker symbols (e.g., AAPL, TSLA)
            - Get summaries and insights about stocks
            """)
        
        # Display system status
        st.subheader("System Status")
        st.success("✅ RAG System Active")
        st.info(f"Current Mode: {mode.upper()}")
        st.info(f"Chat History: {len(st.session_state.chat_history)} entries")

if __name__ == "__main__":
    main() 