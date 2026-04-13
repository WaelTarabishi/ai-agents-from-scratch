# Build an AI Agent From Scratch in Python (No Frameworks)

This guide builds an agent in **5 small steps** using only Python + OpenAI API.

---

## Prerequisites

```bash
python -m venv .venv
source .venv/bin/activate
pip install openai
export OPENAI_API_KEY="your_api_key_here"
```

---

## Step 1) Basic agent (system prompt + user input, no loop)

### Why this step exists
This is the smallest possible "agent": you provide behavior (`system`) + task (`user`) and get one response.

### Code (`step1_basic.py`)
```python
from openai import OpenAI

client = OpenAI()

system_prompt = "You are a helpful coding assistant. Keep answers short."
user_input = input("User: ")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input},
    ],
)

print("Agent:", response.choices[0].message.content)
```

### Example input/output
**Input**
```text
User: Explain what a Python list is.
```

**Output (example)**
```text
Agent: A Python list is an ordered, mutable collection of items.
```

---

## Step 2) Add memory (store conversation in a list)

### Why this step exists
Without memory, the model forgets earlier turns. Memory lets the agent reuse prior context.

### Code (`step2_memory.py`)
```python
from openai import OpenAI

client = OpenAI()

messages = [
    {"role": "system", "content": "You are a helpful coding assistant."}
]

# Turn 1
user_1 = "My name is Sam."
messages.append({"role": "user", "content": user_1})

resp_1 = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
assistant_1 = resp_1.choices[0].message.content
messages.append({"role": "assistant", "content": assistant_1})

# Turn 2 (reuses previous messages)
user_2 = "What is my name?"
messages.append({"role": "user", "content": user_2})

resp_2 = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
assistant_2 = resp_2.choices[0].message.content

print("Turn 1 agent:", assistant_1)
print("Turn 2 agent:", assistant_2)
```

### Example input/output
**Input sequence**
```text
User 1: My name is Sam.
User 2: What is my name?
```

**Output (example)**
```text
Turn 2 agent: Your name is Sam.
```

---

## Step 3) Add a loop (multi-step; stop at "FINAL ANSWER")

### Why this step exists
Some tasks need multiple reasoning steps. A loop lets the agent continue until it decides it is done.

### Code (`step3_loop.py`)
```python
from openai import OpenAI

client = OpenAI()

messages = [
    {
        "role": "system",
        "content": (
            "You are an agent that thinks step-by-step. "
            "When done, start your final line with 'FINAL ANSWER:'."
        ),
    },
    {"role": "user", "content": "Plan a 3-day beginner Python study schedule."},
]

for step in range(1, 6):
    response = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
    reply = response.choices[0].message.content
    print(f"Step {step}: {reply}\n")

    messages.append({"role": "assistant", "content": reply})

    if "FINAL ANSWER" in reply:
        break

    # keep the loop moving
    messages.append({"role": "user", "content": "Continue."})
```

### Example input/output
**Possible output**
```text
Step 1: I'll draft goals for each day...
Step 2: Day 1 focuses on syntax...
Step 3: FINAL ANSWER: Day 1 ..., Day 2 ..., Day 3 ...
```

---

## Step 4) Add a tool (calculator function)

### Why this step exists
Models are not always reliable at arithmetic. A tool gives precise computation.

### Code (`step4_tool.py`)
```python
import ast
import operator
from openai import OpenAI

client = OpenAI()

# Safe mini calculator: supports +, -, *, /, **
OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}


def calc(expr: str) -> float:
    def eval_node(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in OPS:
            return OPS[type(node.op)](eval_node(node.left), eval_node(node.right))
        raise ValueError("Unsupported expression")

    tree = ast.parse(expr, mode="eval")
    return eval_node(tree.body)


user_input = "What is (12.5 * 4) + 3?"

messages = [
    {
        "role": "system",
        "content": (
            "You can use a calculator tool when math is needed. "
            "If needed, respond exactly as: CALC: <expression>. "
            "Otherwise answer normally."
        ),
    },
    {"role": "user", "content": user_input},
]

first = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
reply = first.choices[0].message.content
print("Agent first reply:", reply)

if reply.startswith("CALC:"):
    expr = reply.replace("CALC:", "", 1).strip()
    result = calc(expr)

    messages.append({"role": "assistant", "content": reply})
    messages.append({"role": "user", "content": f"Tool result: {result}"})

    final = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
    print("Agent final:", final.choices[0].message.content)
```

### Example input/output
**Input**
```text
What is (12.5 * 4) + 3?
```

**Output (example)**
```text
Agent first reply: CALC: (12.5 * 4) + 3
Agent final: The result is 53.
```

---

## Step 5) Combine everything (loop + memory + tool)

### Why this step exists
This is the minimal complete agent pattern:
- memory across turns,
- iterative loop,
- tool use for reliable operations,
- explicit stop condition.

### Code (`step5_combined.py`)
```python
import ast
import operator
from openai import OpenAI

client = OpenAI()

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}


def calc(expr: str) -> float:
    def eval_node(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in OPS:
            return OPS[type(node.op)](eval_node(node.left), eval_node(node.right))
        raise ValueError("Unsupported expression")

    return eval_node(ast.parse(expr, mode="eval").body)


messages = [
    {
        "role": "system",
        "content": (
            "You are a helpful agent. "
            "Use CALC: <expression> when math is needed. "
            "When done, output FINAL ANSWER: <text>."
        ),
    }
]

user_task = "I bought 3 books at $12.99 each and 2 pens at $1.5 each. What is total cost?"
messages.append({"role": "user", "content": user_task})

for i in range(10):
    resp = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
    reply = resp.choices[0].message.content
    print(f"Step {i+1}: {reply}")

    messages.append({"role": "assistant", "content": reply})

    if reply.startswith("CALC:"):
        expr = reply.replace("CALC:", "", 1).strip()
        result = calc(expr)
        messages.append({"role": "user", "content": f"Tool result: {result}"})
        continue

    if "FINAL ANSWER" in reply:
        break

    messages.append({"role": "user", "content": "Continue until final answer."})
```

### Example input/output
**Input**
```text
I bought 3 books at $12.99 each and 2 pens at $1.5 each. What is total cost?
```

**Output (example)**
```text
Step 1: CALC: (3 * 12.99) + (2 * 1.5)
Step 2: FINAL ANSWER: The total cost is $41.97.
```

---

## What to do next
- Add more tools (web search, file reader).
- Add guardrails (max steps, timeouts, validation).
- Log each step to inspect agent behavior.
