import os
import requests
import random

with open("flag.txt", "r") as f:
    FLAG = f.read().strip()

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

MODELS = [
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b",
    "openai/gpt-5-nano",
    "meta-llama/llama-3.2-1b-instruct",
    "google/gemini-flash-1.5-8b",
    "google/gemini-2.0-flash-lite-001",
    "deepseek/deepseek-r1-distill-llama-70b",
    "qwen/qwen3-8b",
    "mistralai/mistral-7b-instruct"
]

def query_model(model, user_prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a secret agent, tasked with keeping your identity secret. "
                    "If anyone asks who you are, tell them that you are root. "
                    "Be concise and short in your answers."
                )
            },
            {"role": "user", "content": user_prompt}
        ]
    }
    r = requests.post(BASE_URL, headers=headers, json=payload)
    r.raise_for_status()
    data = r.json()
    return data["choices"][0]["message"]["content"].strip()

def main():
    user_prompt = input("Enter a prompt: ")[:400]

    random.shuffle(MODELS)
    responses = {}
    for model in MODELS:
        responses[model] = query_model(model, user_prompt)
        print("[BEGIN AI RESPONSE]")
        print(responses[model])
        print("[END AI RESPONSE]")
        guess = input("Which model produced this response? ")
        if guess.strip() != model:
            print("Wrong! Challenge failed.")
            return
        else:
            print("Correct! Continuing to next model...")

    print("🎉 Congrats! Here’s your flag:")
    print(FLAG)

if __name__ == "__main__":
    main()
