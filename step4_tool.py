"""Step 4: Add a simple calculator tool.

Issue in this step:
- Tool works, but this script does not do full iterative planning loop.
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


messages = [
    {
        "role": "system",
        "content": (
            "If math is needed, output exactly: CALC: <expression>. "
            "Otherwise answer normally."
        ),
    },
    {"role": "user", "content": input("User: ")},
]

reply = chat(messages)
print("Agent:", reply)

if reply.startswith("CALC:"):
    expr = reply.replace("CALC:", "", 1).strip()
    result = calc(expr)
    messages.append({"role": "assistant", "content": reply})
    messages.append({"role": "user", "content": f"Tool result: {result}"})
    print("Agent:", chat(messages))

print("\n[Known issue] Tool added, but not yet combined with robust loop+memory workflow.")
