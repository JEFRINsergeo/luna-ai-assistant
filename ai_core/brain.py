import ollama
from memory import save_chat, get_history, get_profile, save_profile
from internet import search_web


def ask_ai(user_input):

    history = get_history()
    profile = get_profile()

    # Internet search trigger
    if user_input.startswith("search:"):
        query = user_input.replace("search:", "").strip()
        web_results = search_web(query)
        user_input = f"Use this internet information to answer clearly:\n{web_results}"

    profile_text = "User Profile:\n"
    for k, v in profile.items():
        profile_text += f"{k}: {v}\n"

    messages = [
        {
            "role": "system",
            "content": f"You are a friendly AI companion who helps the user learn, build projects, and solve doubts.\n{profile_text}"
        }
    ]

    for u, a in history:
        messages.append({"role": "user", "content": u})
        messages.append({"role": "assistant", "content": a})

    messages.append({"role": "user", "content": user_input})

    response = ollama.chat(
        model="llama3",
        messages=messages
    )

    reply = response["message"]["content"]

    save_chat(user_input, reply)

    # Profile learning
    text = user_input.lower()

    if "my name is" in text:
        name = user_input.split("my name is")[-1].strip()
        save_profile("name", name)

    if "i am a" in text:
        role = user_input.split("i am a")[-1].strip()
        save_profile("role", role)

    return reply