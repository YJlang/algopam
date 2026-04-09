# OpenAI Official Notes For This Skill

This skill follows a small set of official OpenAI documentation principles so the workflow stays reusable and agent-friendly.

## Sources

- Responses API migration guide  
  https://developers.openai.com/api/docs/guides/migrate-to-responses
- Prompting overview  
  https://developers.openai.com/api/docs/guides/prompting
- Prompt engineering guide  
  https://developers.openai.com/api/docs/guides/prompt-engineering
- Models guide  
  https://developers.openai.com/api/docs/models

## Principles Adopted Here

### 1. Prefer agentic, tool-using workflows

The official Responses API guidance positions Responses as the recommended API for new projects and emphasizes built-in tools, multi-turn state, and agent-style loops. For this skill, that translates to:

- use tools to gather current facts instead of guessing
- keep problem research, code reading, and posting as distinct steps
- preserve working state while iterating on the same draft

### 2. Keep prompts structured

The prompt engineering guide recommends using clear logical boundaries and organizing developer messages into sections such as identity, instructions, examples, and context. This is why the repo-level `AGENTS.md` is organized in that order.

### 3. Reuse prompts and templates

The prompting guide recommends reusable prompts, variables, and versioned prompt assets. For this workflow, the reusable markdown skeleton in `assets/velog-post-template.md` acts as the stable prompt/output scaffold for repeated BOJ write-ups.

### 4. Use the right model and tools for coding work

The models guide recommends modern GPT-5 family models for complex reasoning and coding. In practice, this skill assumes a coding-capable agent should:

- inspect source files before explaining them
- validate claims with examples or counterexamples
- use browser automation only when the user wants web-side staging
- explain non-obvious helpers and libraries in plain language, not by label alone
- turn abstract complexity labels into beginner-friendly explanations tied to the current problem

## How These Principles Change The Write-Up

- The post is grounded in the actual source file, not a guessed solution.
- The problem section is sourced from the official page, but paraphrased for copyright safety.
- The draft has a consistent structure so it can be reused across many BOJ problems.
- The agent keeps a local markdown artifact even when it also writes to Velog.
- Code blocks can be re-presented with short explanatory comments when that improves readability for beginners.
- Big-O sections should define the symbols in the current problem, explain the repeated work, and describe growth in plain language instead of stopping at `O(...)`.
