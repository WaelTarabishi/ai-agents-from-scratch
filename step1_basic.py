"""Step 1: Basic agent (system + user only, single call).

Issue in this step:
- No memory. Agent forgets earlier conversation.
- No loop. Cannot do multi-step work.
"""

from local_llm import chat

messages = [
    {"role": "system", "content": "You are a helpful assistant. Keep replies short."},
    {"role": "user", "content": input("User: ")},
]

answer = chat(messages)
print("Agent:", answer)

print("\n[Known issue] This version has no memory and no multi-step loop.")
