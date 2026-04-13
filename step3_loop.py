"""Step 3: Add a reasoning loop that stops on FINAL ANSWER.

Issue in this step:
- No tool support; math/facts can be wrong.
"""

from local_llm import chat

messages = [
    {
        "role": "system",
        "content": (
            "Work step by step. "
            "When done, write: FINAL ANSWER: <answer>."
        ),
    },
    {"role": "user", "content": input("Task: ")},
]

for step in range(1, 9):
    reply = chat(messages)
    print(f"Step {step}: {reply}\n")
    messages.append({"role": "assistant", "content": reply})

    if "FINAL ANSWER" in reply:
        break

    messages.append({"role": "user", "content": "Continue."})

print("[Known issue] Loop works, but there is no calculator/tool yet.")
