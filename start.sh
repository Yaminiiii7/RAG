#!/bin/sh
# Entrypoint for the all-in-one image: bring up Ollama, then start the app.
set -e

# 1. Start the Ollama server in the background (replaces the `ollama` service)
ollama serve &

# 2. Wait until the server is accepting requests (replaces the healthcheck)
echo "Waiting for Ollama to start..."
until ollama list >/dev/null 2>&1; do
  sleep 1
done
echo "Ollama is ready."

# Models are already baked into the image at build time, so no pull needed here.

# 3. Start the RAG app in the foreground (PID 1 -> container stays alive)
exec python rag.py
