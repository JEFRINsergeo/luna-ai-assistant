import os
import ollama
import google.generativeai as genai

MODEL = "llama3"

# Load Gemini key from environment
GEMINI_KEY = os.getenv("GEMINI_API_KEY")


if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)


def ask_luna(prompt):

    # ---------- TRY OFFLINE OLLAMA ----------
    try:
        response = ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"]

    except Exception:
        pass

    # ---------- FALLBACK TO GEMINI ----------
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(prompt)

        return response.text

    except Exception:
        return "⚠ Luna AI is unavailable right now."