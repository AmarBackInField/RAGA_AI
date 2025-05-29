# 🤖 RAG AI Assistant

A powerful Retrieval-Augmented Generation (RAG) AI Assistant that can process and analyze information from multiple sources including web searches, PDF documents, and stock market data. The assistant features a user-friendly web interface with speech capabilities for both input and output.

## Demo

![Screenshot 2025-05-29 110700](https://github.com/user-attachments/assets/f4dd90fc-2086-40f7-b613-9b2216b67eda)

![Screenshot 2025-05-29 105900](https://github.com/user-attachments/assets/c5aa7466-aa1e-4d43-94ed-f5e174f63a66)

![Screenshot 2025-05-29 105944](https://github.com/user-attachments/assets/d2dfbbc9-7eac-4bed-8c2e-77d85bbdeabc)



## 🌟 Features

- **Multiple Data Sources**
  - Web Search: Get real-time information from the internet
  - PDF Analysis: Upload and analyze PDF documents
  - Stock Analysis: Get insights from Yahoo Finance data

- **Interactive Interface**
  - Modern Streamlit web interface
  - Speech input/output capabilities
  - Chat history tracking
  - Multiple Threading Enables

- **Advanced AI Capabilities**
  - RAG (Retrieval-Augmented Generation) system
  - Contextual understanding and analysis
  - Natural language processing
  - Customizable responses

## Archietecture

![image](https://github.com/user-attachments/assets/1450a96b-9174-4c3d-956c-18ad8fcedde9)


## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- FFmpeg (for audio processing)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/RagaAI.git
cd RagaAI
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

### Running the Application

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

## 💻 Usage

### Web Search Mode
- Enter your search query in the text input
- The assistant will search the web and provide relevant information
- Optionally, ask specific questions about the search results

### PDF Analysis Mode
- Upload a PDF document using the file uploader
- The assistant will process and analyze the content
- Ask questions about the document content

### Stock Analysis Mode
- Enter a stock ticker symbol (e.g., AAPL, TSLA)
- Get analysis and insights about the stock
- View historical data and trends

### Speech Features
- Click the "Mic" button to use speech input
- The assistant will respond with both text and speech output
- Adjust speech rate and volume in the settings

## 📁 Project Structure

```
RagaAI/
├── agents/          # AI agent implementations
├── config/          # Configuration files
├── data_ingestion/  # Data processing modules
├── helper/          # Utility functions
├── models/          # AI model definitions
├── rag/            # RAG system components
├── services/       # External service integrations
├── workflow/       # Workflow definitions
├── app.py          # Main Streamlit application
├── main.py         # CLI entry point
└── requirements.txt # Project dependencies
```



### Testing
Run tests using pytest:
```bash
pytest
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
