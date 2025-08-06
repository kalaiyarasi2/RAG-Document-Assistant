# RAG-Document-Assistant

A **Retrieval-Augmented Generation (RAG) Document Assistant** web app built with Streamlit. Upload your own documents (PDF, DOCX, TXT, CSV, Excel, PPTX), ask questions in natural language, and get instant answers powered by advanced AI (Llama 3 via Groq API).

---

## Features

- Supports multiple document types: PDF, DOCX, TXT, CSV, XLSX, PPTX  
- Conversational QA interface to query your documents  
- AI-powered retrieval: embeddings + FAISS vector search  
- Privacy focused: documents remain local (except AI API calls)  
- Easy to use with no-code, web interface (Streamlit)  
- Modular design to customize or extend

---

## How It Works

1. Upload documents using the app interface.  
2. The app extracts text and creates embeddings for semantic search.  
3. Ask questions about your documents in natural language.  
4. Relevant document chunks are retrieved and passed to Llama 3 (Groq API) for answers.  
5. You can view extracted text, rebuild the index, and more.

---

## Installation

git clone https://github.com/kalaiyarasi2/rag-document-assistant.git
cd rag-document-assistant


2. Install dependencies:

pip install -r requirements.txt


3. Set your Groq API key (see **API Key Setup** below).

4. Run the app:

streamlit run app.py


1. Clone the repository:
---

## API Key Setup

- Obtain your Groq API key from the [Groq Console](https://console.groq.com/).  
- Set the key as an environment variable (recommended):

export GROQ_API_KEY=your_api_key_here


- Or enter it directly in the app when prompted.  
- Do **not** commit your API key to source control.

---

## Usage Examples

Try asking the assistant:

- "What is the main topic of the uploaded PDF?"  
- "Summarize section 3 of the document."  
- "List all key points from the Excel sheet."  
- "What does the presentation say about sales forecasts?"  
- "Are there any deadlines mentioned in these files?"

---

## Troubleshooting Tips

- **App does not start:** Make sure you installed all dependencies from `requirements.txt`.  
- **API errors:** Check your Groq API key is set correctly, and your account has usage quota.  
- **Documents not loading:** Verify supported file formats and file sizes.  
- **Indexing is slow:** Large or many documents may require more time; try smaller datasets first.  
- **Answers seem off:** Ensure documents have clear text and the question is relevant.

---

## Customization

- To add support for new document types or tweak text extraction, modify `backend.py`.  
- To change the embedding model or similarity search method, adjust the embeddings and vector index sections in `backend.py`.  
- To change UI layout or add features, edit `app.py`.  
- Feel free to integrate different LLM APIs by swapping the call in `backend.py`.

---

## File Structure

.
├── app.py # Streamlit frontend
├── backend.py # Document ingestion & retrieval logic
├── requirements.txt # Python dependencies
├── README.md # Project readme (this file)
├── .gitignore # Recommended gitignore rules
├── .env.example # Example environment file for API keys
└── ... # Additional scripts or folders


---

## .gitignore

Add a file named `.gitignore` with the following content to keep your repository clean:

Python cache and environment files
pycache/
*.pyc
.env
*.env

Streamlit-related
.streamlit/

OS generated files
.DS_Store
Thumbs.db

Virtual environment folders
venv/
env/


---

## .env.example

Provide this example file to guide users in setting environment variables without exposing secrets:

GROQ_API_KEY=your_api_key_here


Rename to `.env` and fill in your actual key when running locally.

---




