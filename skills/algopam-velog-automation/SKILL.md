---
name: algopam-velog-automation
description: Turn local algorithm-study solutions, especially BOJ Python files in weekly folders, into researched Korean Velog drafts and optionally stage them in the Velog editor. Use when Codex needs to inspect a solved BOJ problem from code, paraphrase the official problem statement and sample I/O, explain the user's original approach, suggest cleaner alternatives, research public algorithm recap post structure, or automate draft entry with Playwright.
---

# Algopam Velog Automation

## Quick Start

1. Read the target solution file and identify the problem number and title from comments or behavior.
2. Open the official problem page and collect the statement structure, limits, input/output format, and sample I/O.
3. Paraphrase the problem statement instead of copying long source text verbatim. Always keep the original problem link.
4. Read 2-3 public algorithm recap or study-log posts to capture a readable section order and tone.
5. Explain the user's first solution, validate it against examples, and look for at least one counterexample or improvement opportunity.
6. Determine the time complexity of the original and improved solutions with explicit Big-O notation and prepare a short reason for each complexity.
7. Draft the post with the template at `assets/velog-post-template.md`.
8. If the user asks for publishing help, use Playwright to stage the draft in Velog and save it as a draft rather than publishing immediately.

## Workflow

### 1. Build context from the code first

- Read the solution file before making claims about the approach.
- Preserve the user's original code in the post if the write-up is retrospective.
- Separate "what the code is trying to do" from "whether it is fully correct."

### 2. Use official sources for the problem shape

- Prefer the official BOJ problem page for the problem statement, constraints, and examples.
- Include `problem link`, `input format`, `output format`, and `sample input/output` sections in the post.
- Do not paste long problem statements verbatim. Summarize or paraphrase the original wording and point readers to the source link.

### 3. Research structure, not wording

- Read a small set of public algorithm recap posts from platforms such as Velog, Tistory, or Naver Blog.
- Extract the section flow that makes those posts readable.
- Do not imitate specific phrasing; only borrow the structural pattern.

### 4. Default post structure

Use this order unless the problem clearly needs a different flow:

- Intro and problem link
- Problem description
- Input format
- Output format
- Sample input/output
- Core idea or approach
- User's original solution
- What the original solution was trying to do
- Weak points, counterexample, or debugging notes
- One or more improved solutions
- Time complexity
- Retrospective or lessons learned

### 5. Drafting rules

- Write in Korean unless the user asks otherwise.
- Keep the tone reflective and study-log oriented, not textbook-dry.
- Explain both the user's path and the cleaner path.
- Prefer concise sections and readable code blocks.
- Always include time complexity in Big-O notation for the original and improved solutions when practical.
- Do not only state `O(...)`. Also explain why, based on the number of passes, loops, recursive calls, or dominant operations in the code.
- For `O(1)` solutions, say explicitly that the code uses only a fixed number of arithmetic or branching operations and does not scale with input size.
- If several solutions appear, list the complexity for each solution separately so readers can compare them.

### 6. Velog staging rules

- Use Playwright only when the user wants the draft staged on the web.
- Keep a local markdown backup next to the source solution, for example `boj-5612-velog-draft.md`.
- If the editor is CodeMirror-based and Korean text gets corrupted while typing, copy the local markdown to the clipboard and paste it into the editor.
- Save as draft unless the user explicitly asks to publish.

## Resources

- `references/openai-principles.md`
  Use for the official OpenAI prompting and agent-design principles that shaped this workflow.
- `assets/velog-post-template.md`
  Use as the default markdown skeleton for BOJ write-ups.

## Output Checklist

- The post includes the official problem link.
- The problem description is paraphrased, not copied wholesale.
- Input format, output format, and sample I/O are present.
- The user's original approach is explained fairly.
- At least one improved solution or refactor is presented.
- Time complexity is shown in Big-O notation and the reason for that complexity is explained.
- A local backup file exists.
- If Velog was touched, the draft was saved.
