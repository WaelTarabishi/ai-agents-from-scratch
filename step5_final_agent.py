"""Step 5 (final): Complete and correct minimal agent.

Features:
- Memory via `messages`
- Multi-step loop
- Calculator tool
- Stop condition via FINAL ANSWER
"""

import ast
import operator

from local_llm import chat

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


def run_agent(task: str, max_steps: int = 10):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful agent. "
                "If math is needed, write CALC: <expression>. "
                "When you are done, write FINAL ANSWER: <answer>."
            ),
        },
        {"role": "user", "content": task},
    ]

    for i in range(1, max_steps + 1):
        reply = chat(messages)
        print(f"Step {i}: {reply}")
        messages.append({"role": "assistant", "content": reply})

        if reply.startswith("CALC:"):
            expr = reply.replace("CALC:", "", 1).strip()
            try:
                result = calc(expr)
                messages.append({"role": "user", "content": f"Tool result: {result}"})
            except Exception as exc:
                messages.append({"role": "user", "content": f"Tool error: {exc}"})
            continue

        if "FINAL ANSWER" in reply:
            return reply

        messages.append({"role": "user", "content": "Continue until FINAL ANSWER."})

    return "Stopped: reached max steps without FINAL ANSWER."


if __name__ == "__main__":
    user_task = input("Task: ")
    final = run_agent(user_task)
    print("\nResult:", final)
