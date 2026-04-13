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
6. Determine the time complexity of the original and improved solutions with explicit Big-O notation, using worst-case analysis by default.
7. Expand the complexity section for beginners:
   - define what symbols like `n`, `m`, or `k` mean in the current problem
   - identify which loop, search, or repeated operation is doing the real work
   - say what input shape creates the worst case when it is practical to describe
   - explain growth in plain language, such as what happens when the input size roughly doubles
   - when `O(log n)` or binary search is used, explain that the search range is cut roughly in half each step
8. Rewrite blog code blocks with short explanatory comments when helpful, even if the original submission had no comments.
9. Draft the post with the template at `assets/velog-post-template.md`.
10. If the user asks for publishing help, use Playwright to stage the draft in Velog and save it as a draft rather than publishing immediately.

## Workflow

### 1. Build context from the code first

- Read the solution file before making claims about the approach.
- Preserve the user's original code in the post if the write-up is retrospective.
- Separate "what the code is trying to do" from "whether it is fully correct."
- If the blog would be clearer with comments, it is okay to re-present the same logic with short inline comments as long as the behavior stays the same.

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

Inside those sections, prefer adding two kinds of teaching detail when they matter:

- a plain-language explanation of any non-obvious library, helper, or data structure
- a beginner-friendly expansion of the Big-O section, not just the formula

### 5. Drafting rules

- Write in Korean unless the user asks otherwise.
- Keep the tone reflective and study-log oriented, not textbook-dry.
- Explain both the user's path and the cleaner path.
- Prefer concise sections and readable code blocks.
- When showing code in the final post, prefer a blog-friendly version with short comments that explain the role of variables, loops, branches, and important helper calls.
- Do not add noisy comments to every line. Focus on the lines a beginner is likely to stop at and ask about.
- If a helper like `bisect_left`, `heapq.heappop`, `deque.popleft`, `Counter`, or `set` is central to the solution, explain what it does in the current problem instead of naming the tool only.
- When a helper's return value is the key idea, say exactly what it returns and why that matters. Example: "`bisect_left(b, x)` returns the leftmost index where `x` could be inserted, and that index is exactly the number of values in `b` that are smaller than `x`."
- Always include time complexity in Big-O notation for the original and improved solutions when practical.
- Do not only state `O(...)`. Also explain why, based on the number of passes, loops, recursive calls, or dominant operations in the code.
- Treat Big-O as worst-case time complexity unless the post explicitly compares best, average, and worst cases.
- In the Big-O section, explicitly define each symbol in the problem context. Example: "`n` is the length of A, `m` is the length of B."
- After the formal Big-O label, add a plain-language explanation for beginners:
  - what work repeats
  - what part dominates the runtime
  - which input shape or branch makes the worst case happen
  - how the runtime changes as input size grows
- For `O(log n)` explanations, describe the "half each step" intuition.
- For `O(n log n)` explanations, separate the `O(n)` part from the `O(log n)` part when useful, such as "there are `n` items, and each search cuts the remaining range in half."
- If one solution is faster than another, explain what repeated work was removed or reduced, not only that the Big-O label improved.
- For `O(1)` solutions, say explicitly that the code uses only a fixed number of arithmetic or branching operations and does not scale with input size.
- If several solutions appear, list the complexity for each solution separately so readers can compare them.
- Keep these details inside the existing "Time complexity" section. Do not add a new top-level section only for worst-case analysis.
- Prefer one concrete worst-case example over a long theory paragraph. Example: "If every item must be compared with every other item, the nested loops can run about `n * m` checks, so the worst case is `O(nm)`."

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
- The complexity section defines the meaning of symbols like `n`, `m`, or `k` in the current problem.
- The complexity section states the worst-case behavior or gives a small worst-case input shape when practical.
- The complexity section includes a beginner-friendly explanation of how the runtime grows with input size.
- Non-obvious helpers or data structures are explained in plain language, not only named.
- Code blocks include short comments where a beginner would otherwise get stuck.
- A local backup file exists.
- If Velog was touched, the draft was saved.
