# OpenAI Official Notes For This Skill

This reference records the design principles behind the Velog automation workflow. Load it only when refining the skill itself.

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

Velog posting often needs several tool-backed steps:

- inspect user-provided files before drafting
- verify current or external facts before making claims
- create a durable local markdown artifact
- use browser automation only when the user asks for web-side staging or publishing

### 2. Keep prompts structured

The skill separates source gathering, drafting, local backup, and Velog staging so another Codex instance can follow the workflow without guessing the order.

### 3. Reuse flexible templates

The markdown skeleton in `assets/velog-post-template.md` is intentionally general. It gives the post shape without forcing every topic into the same rigid section list.

### 4. Preserve safety and review

The default web action is saving a draft. Publishing requires explicit user intent because Velog posts are public and may include personal, project, or time-sensitive claims.

## How These Principles Change The Output

- Posts are grounded in user materials and verified sources, not generated from memory alone.
- The local markdown backup remains the source of truth even if Velog editing is requested.
- The agent adapts the structure to the content type: tutorial, study log, dev log, review, algorithm write-up, or research summary.
- The workflow protects private details and avoids copying long source text verbatim.
