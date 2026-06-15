import ollama

response = ollama.chat(
    model='llama3.2:3b',
    messages=[
        {'role': 'user', 'content': 'Explain RAG in simple terms'}
    ]
)

print(response['message']['content'])