from pydantic import BaseModel, Field
from typing import Optional

# used for yfinance mode
class StockDataRequest(BaseModel):
    ticker: str
    period: Optional[str] = Field("6mo", description="Period like 1d, 5d, 1mo, 3mo, 6mo, etc.")
    interval: Optional[str] = Field("1d", description="Interval such as 1d, 1wk, or 1mo")
