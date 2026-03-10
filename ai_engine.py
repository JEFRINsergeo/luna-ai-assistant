import os
import ollama
import google.generativeai as genai

MODEL = "llama3"

GEMINI_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)


def ask_luna(prompt):

    # Try Ollama (local only)
    try:
        response = ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"]

    except Exception as e:
        print("Ollama failed:", e)

    # Try Gemini
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Gemini error: {e}"