import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import ollama

MODEL = "llama3.2"

print("=" * 50)
print("       LOCAL OLLAMA CHATBOT")
print("=" * 50)
print("Model:", MODEL)
print("Type 'exit' to quit")
print("=" * 50)

messages = []

while True:
    user_input = input("\nYou: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    try:
        response = ollama.chat(
            model=MODEL,
            messages=messages
        )

        answer = response["message"]["content"]

        print("\nBot:", answer)

        messages.append({
            "role": "assistant",
            "content": answer
        })

    except Exception as e:
        print("\nError:", e)
        print("Make sure Ollama is running and the model is installed.")