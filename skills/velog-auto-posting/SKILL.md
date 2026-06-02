---
name: velog-auto-posting
description: Prepare, verify, draft, and optionally stage or publish Korean Velog posts for any user-requested topic. Use when Codex needs to turn notes, source files, links, code, study material, research, reviews, tutorials, retrospectives, or algorithm solutions into a polished Velog markdown draft, save a local backup, and use Playwright/browser automation to enter the post in Velog when requested.
---

# Velog Auto Posting

## Quick Start

1. Identify what the user wants posted: topic, audience, tone, source material, deadline, and whether they want only a local draft, Velog staging, or publishing.
2. Inspect all user-provided local files, notes, code, images, links, or pasted material before making claims.
3. Research or verify current/external facts when needed. Prefer official or primary sources for factual, technical, legal, medical, financial, or time-sensitive claims.
4. Draft in Korean by default unless the user asks for another language.
5. Use `assets/velog-post-template.md` as a flexible scaffold, not a rigid form.
6. Save a local markdown backup before touching Velog.
7. Use Playwright only when the user asks to stage, edit, or publish on Velog. Save as draft unless the user explicitly asks to publish.

## Workflow

### 1. Clarify Scope Without Stalling

- Infer reasonable defaults from the user's request and available files.
- Ask a concise question only when a missing choice would materially change the post, such as publish vs draft, target Velog account, or whether sensitive/private content may be included.
- If the user gives a broad topic, propose a focused angle and continue unless the topic is too ambiguous to research safely.
- Treat the user's own files or notes as the highest-priority source for personal study logs, project write-ups, and retrospectives.

### 2. Gather Reliable Context

- Read local source material first: code, notes, screenshots, PDFs, Markdown, documents, or repository files.
- For web facts, collect enough sources to support the post's factual claims. Use official docs for product/API details and primary pages for problem statements, specs, releases, prices, policies, or schedules.
- For opinion, review, or study-log posts, research 2-3 public posts only to learn readable structure and common reader expectations. Do not copy wording.
- Keep source links in the draft when they help readers verify or go deeper.
- Paraphrase long source material instead of copying it wholesale.

### 3. Choose The Post Shape

Pick the structure that fits the request:

- **Technical tutorial**: intro, goal, prerequisites, concept, step-by-step implementation, full code, errors/troubleshooting, wrap-up.
- **Study note**: why this topic mattered, core concept, examples, mistakes/confusions, final summary, next steps.
- **Project/dev log**: background, problem, decisions, implementation, results, lessons learned.
- **Review/comparison**: criteria, options, comparison table, pros/cons, recommendation, caveats.
- **Algorithm/BOJ**: problem link, paraphrased description, input/output, sample I/O, approach, original code, weak points, improved solution, complexity, lessons.
- **Research/summary**: question, key takeaways, evidence, source notes, practical implications, limitations.

Do not force every section into every post. A Velog post should feel deliberate, not like a filled form.

### 4. Drafting Standards

- Write in a reflective, readable Korean blog tone unless the user requests a different voice.
- Make the title specific and searchable.
- Start with a short hook that says why the topic matters or what the reader will get.
- Use headings that help scanning.
- Explain jargon, libraries, helper functions, and data structures in plain language when they are central.
- Include runnable code blocks when code is part of the post. Add short comments only where a beginner would otherwise pause.
- When comparing solutions or approaches, explain the tradeoff, not only which one is "better."
- Keep claims proportionate to the evidence. Mark uncertain points as interpretation.
- Avoid publishing private tokens, credentials, private URLs, personal data, or unreviewed company/client details.

### 5. Technical And Algorithm Posts

When the post is based on source code:

- Read the target code before explaining the approach.
- Separate "what the code tries to do" from "whether it is correct."
- Validate with provided examples or small self-made cases when practical.
- Include one cleaner, safer, or more idiomatic alternative when useful.
- Explain time and space complexity when practical:
  - define symbols like `n`, `m`, or `k` in the current problem
  - name the repeated work that dominates runtime
  - describe worst-case behavior when useful
  - explain growth in beginner-friendly language
  - for `O(log n)`, explain that the search range is cut roughly in half each step
- For BOJ or similar problems, use the official problem page for the problem link, limits, input/output, and sample I/O. Paraphrase the statement.

### 6. Local Backup Rules

- Always save the prepared markdown before web staging.
- Put the backup near the user's source material when a clear project/folder exists.
- Use a descriptive filename:
  - `velog-<topic-slug>-draft.md` for general posts
  - `boj-<problem_id>-velog-draft.md` for BOJ posts
  - `<date>-<topic-slug>-velog-draft.md` when chronological organization matters
- Do not overwrite an existing draft unless the user clearly wants an update. Create a versioned filename such as `...-v2.md` if needed.

### 7. Velog Staging Rules

- Use Playwright/browser automation only when the user asks for web staging, editing, or publishing.
- Prefer opening Velog, creating a new post, and pasting the completed local markdown into the editor.
- If Korean text is corrupted while typing into a CodeMirror-style editor, copy the markdown to the clipboard and paste it in one operation.
- Fill title, tags, series, thumbnail, and URL slug when the user provides them or when safe defaults are obvious.
- Save as draft by default.
- Publish only when the user explicitly says to publish.
- After web work, report what was staged or published and mention the local backup path.

## Resources

- `assets/velog-post-template.md`
  Use as a flexible markdown scaffold for general Velog posts.
- `references/openai-principles.md`
  Use only when refining this skill or checking the agent-design rationale.

## Output Checklist

- The post matches the user's requested topic, audience, and tone.
- Important claims are grounded in user-provided material or verified sources.
- Source links are included when useful.
- Long source text is paraphrased rather than copied.
- The structure fits the post type.
- Code, commands, or examples are runnable or clearly marked as illustrative.
- Non-obvious tools, functions, or terms are explained plainly.
- Technical posts include complexity or tradeoff analysis when relevant.
- Sensitive/private details are excluded or minimized.
- A local markdown backup exists.
- If Velog was touched, the post was saved as a draft unless explicit publishing was requested.
