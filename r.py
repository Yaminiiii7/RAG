import os
os.environ["TAVILY_API_KEY"] = "ydc-sk-2e7e3ae953f062a6-E8Jh6xanmfSnSChhnijZZy3CDm3xEuFK-3c66c586"
os.environ["USER_AGENT"] = "rag-app"

import gradio as gr
import ollama
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
#from langchain_community.embeddings import OllamaEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_community.tools.tavily_search import TavilySearchResults
import time

# Step 1: Load data from a webpage
url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
loader = WebBaseLoader(url)

print(loader)
docs = loader.load()

print(docs[0])

# Step 2: Split the text into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

print(splits)