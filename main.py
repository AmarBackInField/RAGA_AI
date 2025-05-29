from workflow.graph import build_rag_workflow
from config.logging_config import setup_logging

# Set up logging
logger = setup_logging(__name__)

def main():
    try:
        logger.info("Initializing RAG workflow")
        workflow = build_rag_workflow()

        
        state = {
            "mode": "yfinance",
            "input_data": "Get me the Apple stock data for the past 3 months with weekly intervals",
            "chunks": [],
            "retriever": None,
            "final_answer": ""
        }
     

        logger.info(f"Starting workflow with state: {state}")
        result = workflow.invoke(state)
        
        logger.info("Workflow completed successfully")
        print("\nFinal Answer:\n", result["final_answer"])
        
    except Exception as e:
        logger.error(f"Error in main workflow: {str(e)}", exc_info=True)
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()
