# How to run a further model (LLM G, ...)

LLM A to F are done (see README.md; A to E are Claude models, F is OpenAI GPT-6). Use this procedure only to add a model, for example one from another provider such as Google Gemini.

Do this once per model and per run (3 runs per model). Run n uses `prompts/prompt_order{n}.txt`.

1. Open a **new chat** with the model, with the version you want (for example a model of another provider). Set reasoning effort / extended thinking to **High** if the app lets you choose; otherwise leave the default and write it down.
   Use a temporary or incognito chat if the app has one, and turn off web search, memory, custom instructions and all tools. Do not attach any other file or project knowledge.
2. Copy the **whole text** of `prompts/prompt_order1.txt` into the chat and send it.
3. The model must reply with **only a JSON array** (21 objects). Copy the reply into a new file:
   `raw_responses/llm_g_run1.json`.
   If it adds text around the array, keep only the array; a ```json fence is accepted.
4. Start a **new chat** for run 2 (prompt_order2.txt) and run 3 (prompt_order3.txt). Never reuse a chat for two runs.
5. Write down, for each model: the exact model name shown by the app, the effort setting, and the date.

Use the next free label (LLM F, G, ...) and `raw_responses/llm_g_run1.json`, `llm_f_run2.json`, `llm_f_run3.json`.

## What to send back
Send the JSON files (or paste the replies) with the model name and run number, and Claude will validate and add them.
To add a run yourself instead:

```
cd scripts
python3 add_run.py --model "LLM G (model name)" --run 1 --json ../raw_responses/llm_g_run1.json
python3 analyze.py
```

`add_run.py` refuses a response if an entry is missing or duplicated, a rating is outside its range, or the same
model and run was already added.
