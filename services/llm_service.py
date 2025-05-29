from models.entity import StockDataRequest
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")

class LLMService:
    def __init__(self) -> None:
        self.llm_4_1_mini=ChatOpenAI(model="gpt-4.1-mini")
        self.param_extraction_llm = self.llm_4_1_mini.with_structured_output(StockDataRequest, method="function_calling")
    
    def __call__(self, *args: os.Any, **kwds: os.Any) -> os.Any:
        pass

    
