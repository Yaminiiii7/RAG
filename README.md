# RAG with Llama 3

A local **Retrieval-Augmented Generation (RAG)** application that answers questions about a web page using [Ollama](https://ollama.com/), [LangChain](https://www.langchain.com/), [ChromaDB](https://www.trychroma.com/), and a [Gradio](https://www.gradio.app/) web UI — all running fully locally, no external LLM API required.

The app loads a Wikipedia article, splits it into chunks, embeds them into a vector store, and uses the `llama3.2:3b` model to answer questions grounded in the retrieved content.

## How it works

```
Web page ──► Split into chunks ──► Embed (nomic-embed-text) ──► ChromaDB
                                                                    │
Question ──────────────────────────────► Retrieve relevant chunks ─┘
                                                                    │
                                          llama3.2:3b + context ──► Answer (Gradio UI)
```

1. **Load** – [`WebBaseLoader`] fetches the source page (default: the *Artificial intelligence* Wikipedia article).
2. **Split** – `RecursiveCharacterTextSplitter` breaks the text into 1000-character chunks with 200-character overlap.
3. **Embed & store** – chunks are embedded with `nomic-embed-text` and stored in an in-memory ChromaDB vector store.
4. **Retrieve** – at query time, the most relevant chunks are pulled from the store.
5. **Generate** – `llama3.2:3b` answers the question using the retrieved chunks as context.
6. **Serve** – a Gradio interface exposes the app on port `7860`.

## Tech stack

| Component        | Used for                                  |
| ---------------- | ----------------------------------------- |
| Ollama           | Running `llama3.2:3b` + `nomic-embed-text` locally |
| LangChain        | Document loading, splitting, retrieval    |
| ChromaDB         | Vector store for embeddings               |
| Gradio           | Web UI                                     |
| Docker Compose   | One-command orchestration of Ollama + app |

## Project structure

| File | Purpose |
| ---- | ------- |
| [rag.py](rag.py) | Main RAG application and Gradio UI |
| [ollamacheck.py](ollamacheck.py) | Quick smoke test that Ollama + `llama3.2:3b` respond |
| [requirements.txt](requirements.txt) | Python dependencies |
| [Dockerfile](Dockerfile) | Image for the RAG app |
| [docker-compose.yml](docker-compose.yml) | Runs Ollama, pulls models, and starts the app |
| [.github/workflows/aws.yml](.github/workflows/aws.yml) | CI: build & push image to Amazon ECR on push to `main` |

## Getting started

### Option 1 — Docker Compose (recommended)

This spins up Ollama, automatically pulls the required models, and starts the app.

```bash
docker compose up --build
```

Then open **http://localhost:7860**.

### Option 2 — Run locally

**Prerequisites:** [Ollama installed](https://ollama.com/download) and running.

1. Pull the models:

   ```bash
   ollama pull llama3.2:3b
   ollama pull nomic-embed-text
   ```

2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file (see [Configuration](#configuration)).

4. Run the app:

   ```bash
   python rag.py
   ```

   Then open **http://localhost:7860**.

## Configuration

Create a `.env` file in the project root:

```env
TAVILY_API_KEY=your_tavily_api_key      # optional, for web search
OLLAMA_HOST=http://localhost:11434      # defaults to localhost; set to http://ollama:11434 in Docker
```

## Usage

Type a question into the Gradio textbox (e.g. *"What is artificial intelligence?"*) and the app returns an answer grounded in the loaded article.

To point the app at a different source, change the `url` in [rag.py](rag.py#L22).

## Deployment

The included [GitHub Actions workflow](.github/workflows/aws.yml) builds the Docker image and pushes it to **Amazon ECR** on every push to `main`. To use it, configure these GitHub Actions secrets:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

and set the `AWS_REGION` / `ECR_REPOSITORY` env values in the workflow.

## Credits

Based on the [GeeksforGeeks RAG using Llama 3 tutorial](https://www.geeksforgeeks.org/artificial-intelligence/rag-using-llama3/).
