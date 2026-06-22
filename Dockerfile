FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["python", "rag.py"] 

# All-in-one image: Ollama + RAG app in a single container.
# Equivalent to the docker-compose stack (ollama + ollama-pull + rag-ai-app),
# but bundled together so it runs from one image with no orchestration.

#FROM python:3.11-slim

# System deps + install Ollama
#RUN apt-get update \
#    && apt-get install -y --no-install-recommends curl ca-certificates zstd \
#    && curl -fsSL https://ollama.com/install.sh | sh \
#    && apt-get clean \
#    && rm -rf /var/lib/apt/lists/*

#WORKDIR /app

# Python dependencies
#COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt

# Bake the models into the image at build time (replaces the ollama-pull service).
# Start the server temporarily, pull the models, then let the shell exit.
#RUN ollama serve & \
#    until ollama list >/dev/null 2>&1; do sleep 1; done; \
#    ollama pull llama3.2:3b && \
#    ollama pull nomic-embed-text

# Application code
#COPY . .

# App + Ollama run on the same host, so talk over localhost
#ENV OLLAMA_HOST=http://localhost:11434

#EXPOSE 7860 11434

#COPY start.sh /start.sh
#RUN chmod +x /start.sh

#CMD ["/start.sh"]
