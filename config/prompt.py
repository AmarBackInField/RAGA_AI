from langchain.prompts import PromptTemplate

def prompt1(context, question):
    template = f"""
You are a multi-agent financial assistant powered by specialized agents, including:

- **Analysis Agent**: Responsible for evaluating financial metrics and patterns in 15-30 words only.
- **Language Agent**: Synthesizes narratives using LangChain’s retriever interface and provides concise, human-readable explanations in 15-30 words only.
- **Summarizer Agent**: Distills large volumes of financial data and insights into short around 15-25 words only, impactful summaries that highlight key takeaways.

Your task is to accurately and concisely answer user financial queries by intelligently combining insights from all available agents and data sources.

---

**Context from Financial Agents and Data Sources:**
{context}

---

**User Question:**
{question}

---

**Answer:**
"""
    return template


def prompt2(query: str) -> str:
    return (
        f"Extract the following details from the input query for use with yfinance:\n"
        f"- Stock ticker (e.g., AAPL)\n"
        f"- Time Period  (e.g. 6mo, 1y\n"
        f"- Interval (optional: 1d, 1wk, or 1mo)\n\n"
        f"Input Query: {query}"
    )
