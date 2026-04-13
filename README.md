# AI Agent From Scratch in Python (Local LLM, No Frameworks)

This repo now contains real code files (not only a README).

## Requirements
- Python 3.10+
- [Ollama](https://ollama.com/) running locally
- A local model pulled in Ollama (example: `llama3.1:8b`)

## Installation
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Start local LLM
```bash
ollama serve
ollama pull llama3.1:8b
```

> If you use a different model, edit `MODEL` in `local_llm.py`.

## Project Structure
- `local_llm.py` — tiny client for local Ollama chat API
- `step1_basic.py` — system + user (single call)
- `step2_memory.py` — adds conversation memory list
- `step3_loop.py` — adds multi-step loop with `FINAL ANSWER` stop
- `step4_tool.py` — adds calculator tool selection pattern
- `step5_final_agent.py` — final complete version (loop + memory + tool)

## Run Each Step
```bash
python step1_basic.py
python step2_memory.py
python step3_loop.py
python step4_tool.py
python step5_final_agent.py
```

## Why Steps Exist + Known Issues
1. **Step 1**: Minimal baseline.  
   - Issue: no memory, no multi-step behavior.
2. **Step 2**: Reuse prior conversation (`messages` list).  
   - Issue: still no autonomous reasoning loop.
3. **Step 3**: Add iterative loop and explicit stop condition.  
   - Issue: no tool, so calculations can be unreliable.
4. **Step 4**: Add calculator tool (`CALC: ...`).  
   - Issue: not yet full combined planning workflow.
5. **Step 5**: Complete and correct minimal agent combining all pieces.

## Quick Example for Final Step
Input:
```text
I bought 3 books at 12.99 and 2 pens at 1.5 each. What's total?
```

Expected behavior:
- Agent emits `CALC: (3*12.99) + (2*1.5)`
- Python tool computes result
- Agent returns `FINAL ANSWER: ...`
