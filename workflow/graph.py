from langgraph.graph import StateGraph, END
from config.logging_config import setup_logging
from agents.agents import RAGState,load_data,create_retriever,analysis_agent


# Set up logging
logger = setup_logging(__name__)





# Define LangGraph flow
def build_rag_workflow():
    logger.info("Building RAG workflow")
    try:
        graph = StateGraph(RAGState)

        graph.add_node("load_data", load_data)
        graph.add_node("generate_retriever", create_retriever)
        graph.add_node("analysis_agent", analysis_agent)

        graph.set_entry_point("load_data")
        graph.add_edge("load_data", "generate_retriever")
        graph.add_edge("generate_retriever", "analysis_agent")
        graph.add_edge("analysis_agent", END)

        app = graph.compile()
        logger.info("Successfully built RAG workflow")
        return app
    except Exception as e:
        logger.error(f"Error building RAG workflow: {str(e)}", exc_info=True)
        raise
