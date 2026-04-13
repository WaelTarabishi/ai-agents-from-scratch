"""Step 2: Add memory using a messages list.

Issue in this step:
- Still no autonomous loop.
- Still no tools for reliable calculation.
"""

from local_llm import chat

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
]

while True:
    user_text = input("User (or 'quit'): ").strip()
    if user_text.lower() == "quit":
        break

    messages.append({"role": "user", "content": user_text})
    answer = chat(messages)
    messages.append({"role": "assistant", "content": answer})

    print("Agent:", answer)

print("\n[Known issue] Memory exists, but no step loop or tool use yet.")
