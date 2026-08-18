# AI Genius Episode 1: Workshop Repo

![TitlePage](https://github.com/codess-aus/AIGenius-GHCP-AINative/blob/4d72afc7038a1cf0f45bc48c38ae517547b30628/assets/AI-Genius-Ep1.png)


## "Code with AI: GitHub Copilot for AI-Native Coding Workflows"

Welcome! This is the hands-on workshop repo for **AI Genius Episode 1**. You'll work through the full AI-native development loop: writing issues, delegating to Copilot, reviewing generated code, and iterating via PR comments.

---

## What You Will Learn

- What "AI Native" actually means for developers
- How to write issues that give Copilot the context it needs
- How to assign work to Copilot and observe it in action
- How to review Copilot-generated PRs like a senior developer
- How to iterate via PR comments instead of starting from scratch
- Best practices for collaborating with AI throughout the coding process

---

## The AI-Native Workflow Loop

```
IDEA
  └─► GitHub Issue  (describe the work)
        └─► Assign to Copilot  (Copilot agent picks it up)
              └─► Code is generated in a secure sandbox
                    └─► Draft PR is opened  (with session log)
                          └─► Human reviews and iterates via PR comments
                                └─► Merge and ship
```

You are the **tech lead** in this workflow. Copilot handles the *how*. You define the *what* and *why*.

---

## Setup Instructions

### Prerequisites

- A GitHub account with access to GitHub Copilot
- [GitHub Copilot App](https://github.com/features/copilot) installed (desktop)
- Python 3.10+ installed locally (for the starter app)
- Git installed

### Get Started

1. **Fork this repo** to your own GitHub account (top-right corner of this page).

2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/AIGenius-GHCP-AINative.git
   cd AIGenius-GHCP-AINative
   ```

3. **Run the starter app**:
   ```bash
   cd starter-app
   pip install -r requirements.txt
   python app.py add "Deploy the API" --priority high --due 2025-12-31 --tag work
   python app.py add "Buy coffee" --priority low --tag personal
   python app.py list
   python app.py stats
   ```

4. **Open the GitHub Copilot App** and connect it to your forked repo.

5. Work through the exercises in order, starting with [`exercises/01-write-an-issue`](./exercises/01-write-an-issue/README.md).

---
## Repo Structure

```
📁 AIGenius-GHCP-AINative/
  ├── README.md                        # Episode intro + setup instructions
  ├── .github/
  │   ├── copilot-instructions.md      # Copilot context: conventions, Azure patterns, secrets
  │   └── ISSUE_TEMPLATE/
  │       └── feature-request.md       # Issue template for AI-native workflow
  ├── exercises/
  │   ├── 01-write-an-issue/           # Task: write a well-formed issue (cloud/AI options)
  │   ├── 02-assign-to-copilot/        # Task: assign + observe
  │   ├── 03-review-a-pr/              # Task: review and comment on a PR
  │   ├── 04-iterate/                  # Task: iterate via PR comments
  │   └── 05-azure-and-ai/             # Stretch: pre-written issues for Azure + OpenAI features
  └── starter-app/                     # Python CLI task manager to extend
      ├── app.py                       # CLI: add, list, complete, edit, delete, stats
      ├── requirements.txt             # click, rich, pytest
      └── tests/
          ├── conftest.py              # Shared fixtures (isolated task file)
          └── test_tasks.py            # 41 tests covering all commands + edge cases
```

---

## The 5 Golden Rules of AI-Native Coding

1. **Write better issues** -- your issue IS your prompt. Be specific.
2. **Review like a senior dev** -- AI generates fast, humans verify smart.
3. **Use `copilot-instructions.md`** -- give Copilot standing context about your project.
4. **Iterate, don't regenerate** -- guide via comments rather than starting from scratch.
5. **Stay in the loop** -- check the session log, understand what Copilot did and why.

---

## Speaker

**Michelle Sandford** -- Developer Engagement Lead, Australia and NZ

Michelle is a Developer Engagement Leader at Microsoft who writes code, builds with GitHub and Azure AI, and learns out loud.
