import os
from dotenv import load_dotenv
load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY

os.environ["USER_AGENT"] = "rag-app"

import gradio as gr
import ollama
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_community.tools.tavily_search import TavilySearchResults
import time

# Step 1: Load data from a webpage
url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
loader = WebBaseLoader(url)
docs = loader.load()

# Step 2: Split the text into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

# Step 3: Create embeddings and store in ChromaDB

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

client = ollama.Client(host=OLLAMA_HOST)

embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
    base_url=OLLAMA_HOST
)
embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_HOST)
vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)


# Step 4: Define a function to call Llama 3 with context
def ollama_llm(question, context):
    formatted_prompt = f"Question: {question}\n\nContext: {context}"
    response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': formatted_prompt}])
    return response['message']['content']

# Step 5: Set up the RAG system
retriever = vectorstore.as_retriever()
def rag_chain(question):
    retrieved_docs = retriever.invoke(question)
    formatted_context = "\n\n".join(doc.page_content for doc in retrieved_docs)
    return ollama_llm(question, formatted_context)

# Step 6: Create a Gradio interface
def get_answer(question):
    return rag_chain(question)

iface = gr.Interface(
    fn=get_answer,
    inputs=gr.Textbox(lines=2, placeholder="Enter your question here..."),
    outputs="text",
    title="RAG with Llama 3:",
    description="Ask questions."
)

# Step 7: Launch the Gradio app
iface.launch(server_name="0.0.0.0", server_port=7860)