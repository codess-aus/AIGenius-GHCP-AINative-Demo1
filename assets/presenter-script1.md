# AI Genius Episode 1 - Presenter Script

**"Code with AI: GitHub Copilot for AI-Native Coding Workflows"**
1 hour · All skill levels · Livestream on YouTube

---

## Run of Show

| Time | Segment | Topic | Slide/Asset | Demo |
|------|---------|-------|-------------|------|
| 0:00 | Opening | What does AI-native actually mean? | Title slide / README | None |
| 0:05 | Live demo | Run the starter app, show it working | None | Terminal: `app.py` commands |
| 0:10 | Context | `copilot-instructions.md` + test suite | `.github/copilot-instructions.md` | Terminal: `pytest` |
| 0:15 | Exercise 01 | Write a well-formed issue together | Browser: Issues tab, template | None |
| 0:25 | Exercise 02 | Assign to Copilot, watch it work | None | Browser + Copilot App |
| 0:30 | Showcase | The GitHub Copilot app: what it is, when to use it, worktrees, canvases | Copilot App screenshare | Live: My Work view, a session, a canvas |
| 0:34 | Concept | Scaling up: from one issue to a fleet (`/fleet` and `/squad`) | Architecture / concept slide | Optional: live `/fleet` demo, time permitting |
| 0:38 | Exercise 03 | Review the generated PR | None | Browser: PR diff, session log |
| 0:48 | Exercise 04 | Iterate via PR comments | None | Browser: PR comments, merge |
| 0:55 | Stretch (optional) | Azure Table Storage + Azure OpenAI | Architecture diagram | Code walkthrough, no live Azure needed |
| 0:58 | Closing | 5 Golden Rules + call to action | None | None |

> **Timing note:** the core loop (Segments 1 to 7, including the Copilot App showcase and the Fleet/Squad concept segment) fits inside 55 minutes. The *talking points* in the Copilot App showcase and the Fleet/Squad segment are not optional, they're core content, only the optional live `/fleet` demo can be cut for time.

> **Livestream note:** there is no in-room audience. Everyone watching is in YouTube chat. Have a moderator (or a second monitor) watching chat throughout so questions can be answered live without breaking your flow on screen.

---

## Segment 1 - Opening (0:00 to 0:05)

*Screen: Title slide or repo README*

**SAY:**
> Welcome everyone, thanks for tuning in. My name is Michelle. I'm a Developer Engagement Lead at Microsoft.
>
> Today we're going to do something a little different. I'm not going to teach you GitHub Copilot features. I'm going to change how you think about writing code.
>
> When I say "AI-native", I don't mean bolting an AI assistant onto the pipeline you already have, and I don't mean using Copilot to autocomplete a line of code faster. AI-native is a different shape of workflow entirely.
>
> That changes what your job actually is. You're no longer the one typing every line. You're the one defining **what** to build, **why** it matters, and what "done" looks like. The agent handles **how**.
>
> By the end of this hour, you will have watched the full AI-native loop happen live: write issue, delegate to Copilot, review the PR, iterate. If you've got the repo forked, follow along in your own copy.

> 🔎 **Fun fact to drop here:** GitHub Copilot's coding agent runs your assigned issue inside an isolated GitHub Actions VM. It genuinely cannot touch production, cannot push directly to protected branches, and every action it takes is logged in a session you can audit afterwards.

> 💡 **Chat prompt:** ask the chat "How many of you have used GitHub Copilot for code completion? Type C in chat." Then: "How many have used Copilot to write an entire feature from a GitHub Issue? Type F in chat."

---

## Segment 2 - Live Demo: The Starter App (0:05 to 0:10)

*Screen: Terminal in the starter-app directory*

**SAY:**
> Let me show you what we're working with. This is a Python command-line task manager. It sounds simple, but it's a real codebase with priorities, tags, due dates, timestamps, and an automated test suite.
>
> This is the app we'll be extending today using Copilot. If you've forked the repo, feel free to run these same commands locally as I go, and let me know in chat if anything doesn't work for you so I can help troubleshoot.

**DO, type these commands live:**

```bash
cd starter-app

# Add a few tasks with different options
python app.py add "Deploy the API" --priority high --due 2025-12-31 --tag work
python app.py add "Buy coffee" --priority low --tag personal
python app.py add "Update README" --priority medium --tag work

# Show the full task list
python app.py list

# Show filters
python app.py stats
python app.py list --priority high
python app.py list --overdue
```

**SAY:**
> Notice that overdue tasks light up in red automatically, thanks to `rich` formatting. The app has filtering built in.
>
> Now, what if I want to store these tasks in Azure instead of a local file? And what if I want the app to automatically suggest a tag using AI when I add a task? That's what Copilot is going to build for us today.

---

## Segment 3 - Context: Instructions & Tests (0:10 to 0:15)

*Screen: VS Code or GitHub, `.github/copilot-instructions.md`*

**SAY:**
> Before Copilot writes a single line of code, it reads two things: your issue, and the copilot-instructions file.
>
> Think of `copilot-instructions.md` as the onboarding document you'd give a new developer. It tells Copilot what libraries to use, how to handle secrets, what the test approach is, and what "done" looks like for this repo.

**DO:**
1. Share your screen on `.github/copilot-instructions.md`
2. Point out these specific sections on screen, narrating clearly since viewers can't lean over your shoulder:
   - The task schema (the JSON example)
   - The Azure Table Storage section (SDK name, env var names)
   - The "Never hardcode credentials" rule
   - The testing approach (pytest, mocking Azure calls)

**SAY:**
> This file is the reason Copilot will reach for the right Azure SDK instead of a random library it found on the internet. Context is everything.
>
> Now let me show you the test suite.

**DO:**

```bash
# Open starter-app/tests/test_tasks.py, briefly scroll through the class structure
# Then run it live:
python -m pytest tests/ -v
```

Narrate what viewers are seeing on screen: all tests passing, in under a second.

**SAY:**
> When Copilot adds the Azure backend, it has to keep every one of these tests passing. That's the safety net. And it will write new tests for the new code too.

> 🔎 **Interesting fact:** keeping the dependency list minimal (`click`, `rich`, `pytest`) isn't just good practice for humans, it directly improves what an AI coding agent can do with your repo. Fewer dependencies means less ambiguity for the agent to reason about when deciding how to extend the code.

---

## Segment 4 - Exercise 01: Write the Issue (0:15 to 0:25)

*Screen: GitHub Issues tab, New Issue form*

**SAY:**
> Now I'm going to write an issue live on screen, and I'll talk through each section as I fill it in. If you've forked the repo, open your own Issues tab and write along with me, or write your own variation.
>
> The golden rule of AI-native development is this: **your issue IS your prompt.** If you write a vague issue, you get vague code. If you write a precise specification, you get precise code.

**DO, type or paste this issue:**

> **Title:** Migrate task storage to Azure Table Storage
>
> **Problem statement:**
> Tasks are stored in a local JSON file (`tasks.json`). This means data is lost when the machine changes and cannot be shared across devices. We need a cloud-backed storage option.
>
> **Desired behaviour:**
> - When `AZURE_STORAGE_CONNECTION_STRING` is set, tasks are stored in Azure Table Storage
> - When not set, the app falls back to the existing local JSON file
> - All existing CLI commands work identically, zero breaking changes
>
> **Acceptance criteria:**
> - [ ] A `storage.py` module with a `TaskStorage` protocol: `load() -> list[dict]` and `save(tasks) -> None`
> - [ ] `LocalStorage` implements `TaskStorage` using the existing JSON approach
> - [ ] `AzureTableStorage` implements `TaskStorage` using `azure-data-tables`
> - [ ] `app.py` calls `get_storage()` at startup to pick the right backend
> - [ ] `AZURE_STORAGE_CONNECTION_STRING` is loaded from `.env` using `python-dotenv`
> - [ ] Connection errors print a clear message and exit with code 1
> - [ ] `azure-data-tables` and `python-dotenv` added to `requirements.txt`
> - [ ] Tests mock Azure calls, no real API calls in tests
> - [ ] No connection strings or account keys in source code
>
> **Constraints:**
> Use `azure-data-tables` (not the older `azure-storage-table` SDK).
> Use `PartitionKey = "tasks"` and `RowKey = str(task["id"])`.
>
> **Submit the issue.**

**SAY:**
> Notice how specific I was. I named the module. I named the protocol. I named the method signatures. I named the environment variable.
>
> A human developer might fill in those gaps from experience. Copilot takes you literally. The more you specify, the closer the output is to what you actually want.
>
> Take 5 minutes if you're following along in your own fork, write the same issue or try Option B, C, or D from the exercises folder. I'll keep talking through the reasoning while you write, and I'll check chat for questions.

> 🔎 **Interesting fact:** this is essentially prompt engineering wearing a GitHub Issues costume. The same principles, specificity, examples, constraints, that make a good LLM prompt make a good AI-native issue.

> 👀 **WATCH FOR:** keep an eye on chat while people share their draft issues or ask questions. If someone posts an issue that's vague in the Acceptance Criteria section, gently prompt in chat: "What would 'done' look like for that requirement specifically?"

---

## Segment 5 - Exercise 02: Assign to Copilot (0:25 to 0:30)

*Screen: GitHub Issue, Assignees panel on the right*

**SAY:**
> Now for the part that still feels a bit like magic the first time you see it.
>
> Open the issue you just submitted. On the right side, find the Assignees panel. Depending on your repo's UI, you'll see either a dropdown listing available assignees, or a dedicated **Assign to Agent** button. Either way, we're assigning this issue to GitHub Copilot's coding agent. If you're following along, do the same on your own issue now.

**DO:**
1. Demonstrate on your own issue, on screen
2. In the Assignees panel, either select **Copilot** from the assignee dropdown, or click **Assign to Agent** if that's what your repo shows, both do the same thing
3. Show the confirmation comment that appears on the issue
4. Open the GitHub Copilot App on your desktop, go to My Work, find the active session
5. Keep this on the main screen share so everyone watching can see Copilot working in real time

**SAY:**
> While we wait, watch what it does first. It doesn't start coding immediately. It **explores**. It reads `copilot-instructions.md`. It reads `app.py`. It reads the existing tests.
>
> That's exactly what a good developer does, understand the codebase before touching it.
>
> One thing worth calling out here: this agent runs entirely in the cloud, on a GitHub Actions virtual machine. It is not running on my laptop. That means it keeps working even if I close this laptop and walk away.
>
> Today we're specifically using GitHub Copilot. Some of you may notice that same Assignees panel can list other AI agents as options too. That's not GitHub being agnostic about which agent does the work, it's the opposite. It's GitHub offering **choice**, while every one of those agents, Copilot included, runs inside the same governed control plane: the same repository permissions, the same branch protections, the same audit logging, the same security and compliance boundary. That control plane is GitHub's real advantage. You get to choose your agent, but you never leave GitHub's security, governance, privacy, and compliance model to do it.

> 👀 **WATCH FOR:**
> - Point out on screen when Copilot references `copilot-instructions.md`, this is the payoff for Segment 3
> - Point out when it reads the existing tests, it's learning the test patterns
> - If the PR isn't ready by 0:30, don't wait, move straight into Segment 5B, the wait time is exactly when a concept segment earns its keep
> - Keep glancing at chat, this is a natural point for questions since there's a bit of a wait

> 💡 **Chat prompt:** ask chat "What did you notice about how Copilot explored the codebase? What did it look at first?" and read out a couple of answers.

---

## Segment 5B - Showcase: The GitHub Copilot App (0:30 to 0:34)

*Screen: GitHub Copilot app, My Work view*

> **This segment is core content, not optional.** While Copilot works in the background on the issue we just assigned, this is the natural moment to showcase the app we already have open and explain why it matters.

**SAY:**
> We already opened the GitHub Copilot app to watch our session, but let's slow down for a minute because most of you haven't seen this before, and it's genuinely a different way of working with agents.
>
> The Copilot app is a standalone desktop application, it's not a browser tab and it's not an editor extension. It's a control center purpose-built for **agent-native development**. Instead of bouncing between a GitHub Issue tab, a PR tab, and a terminal to figure out what's happening, everything lives in one place.

**DO:**
1. Point to the **My Work** view on screen
2. Call out the active session for the issue we just assigned
3. If time allows, show the inbox of issues and PRs from connected repos

**SAY, what it is and when to use it:**
> The heart of the app is the **My Work** view. It shows your active sessions, one per agent working on a task, your inbox of issues and PRs, and any background automations, like Agent Merge carrying a PR through CI and review while you're not even looking at it.
>
> You reach for this app specifically when you're directing **more than one agent at a time**. If you're the kind of developer who assigns one issue and waits, VS Code or GitHub.com is fine. But the moment you're running two, five, ten sessions in parallel, this app is where you go to see all of them at a glance instead of hunting across browser tabs.
>
> It's also worth knowing this isn't just for developers. Because it's a desktop-first, visual interface rather than a terminal or an IDE, it's genuinely approachable for product managers, business analysts, anyone on your team who wants to direct an agent but finds the CLI or VS Code intimidating.

**SAY, why this instead of Codespaces, VS Code, or github.com:**
> Someone in chat is probably wondering, don't I already have Codespaces, VS Code, and github.com for this? Yes, and the Copilot app doesn't replace any of them, it fills a specific gap.
>
> Think of it this way: VS Code is where you write and review code with instant, in-editor AI assistance. GitHub.com is your hub for collaboration, code review, and PR management, always accessible from a browser. Codespaces gives you a full cloud dev environment when you need to run and debug code yourself. The Copilot app's strength is different: it's the control center for **directing and monitoring multiple agents in parallel**, something none of those three experiences were designed to visualize at a glance. You'll still use all of them together, VS Code to code, github.com to collaborate, and the Copilot app to orchestrate.

**SAY, worktrees:**
> Here's the part that makes parallel agents actually safe: every session in the Copilot app runs in its own **git worktree**, a real, isolated copy of your branch and working directory.
>
> That means if I have three agents working on three different issues in the same repo right now, they each get their own branch, their own environment, their own set of changes, and they cannot step on each other. No manual branch juggling, no `git stash` gymnastics, the app creates and cleans up worktrees automatically. You can even pick up a session on a different device later, because the worktree and the session state travel with it.

**SAY, canvases:**
> The last piece is **canvases**. Instead of a long chat thread where you're squinting to figure out what an agent actually did, a canvas is an interactive surface, a plan, a PR diff, terminal output, even a live browser session, that updates in real time as the agent works.
>
> You can edit, approve, or redirect the agent right there on the canvas, instead of typing another chat message and hoping it understood you. It turns "trust me, it's working" into something you can actually see and steer.

> 🔎 **Fun fact to drop here:** the Copilot app supports deep links, like `ghapp://session/new?repo=owner/repo&prompt=fix%20the%20flaky%20test`, so you can kick off a new agent session straight from a terminal alias or script, then watch it land in My Work.

> 👀 **WATCH FOR:** chat will likely ask "do I still need VS Code?" Reinforce: yes, absolutely, the Copilot app is an addition for orchestrating multiple agents, not a replacement for your editor.

> 💡 **Chat prompt:** ask chat "If you had three agents running right now, what three tasks would you hand them?"

---

## Segment 5C - Concept: Scaling Up, From One Issue to a Fleet (0:34 to 0:38)

*Screen: Concept slide or architecture diagram, terminal optional*

> **This segment is core content, not optional.** While Copilot works in the background on the issue we just assigned, this is the natural moment to zoom out and talk about what happens once you outgrow a single issue at a time.

**SAY:**
> So far we've done the smallest possible unit of AI-native work: one issue, one agent, one PR. That's the right place to start, but it doesn't scale to a real sprint, where you might have ten issues in flight.
>
> This is where `/fleet` and `/squad` come in. They're two different answers to the same question: "How do I go from one developer directing one agent, to a whole team directing many agents at once?"

**SAY, explain `/fleet`:**
> `/fleet` is a Copilot CLI command built for **parallel, stateless execution**. You give it one objective, and an orchestrator agent breaks that objective into independent sub-tasks, checks which ones are unblocked, and runs them in parallel.
>
> Think of it like this: if our single Copilot agent today is one developer picking up one issue, `/fleet` is like assigning ten related issues at once and having ten short-lived contractors work them simultaneously, then handing back the combined result.

**SAY, explain `/squad`:**
> `/squad` is a different shape of answer. It's not a single CLI command, it's an open source framework you install into your repo that creates a **persistent team of named agents**. Unlike Fleet's disposable sub-agents, Squad agents stick around across issues and sessions.
>
> If Fleet is contractors for a single sprint, Squad is closer to hiring permanent specialists onto your team, they build context over time, and they can even use Fleet internally when they need a burst of parallel throughput.

**SAY, connect it to cloud-native AI in the SDLC:**
> Here's why this matters beyond the novelty. These two patterns map almost exactly onto ideas you already use in cloud-native architecture.
>
> `/fleet` is **horizontal scaling for cognitive work**. A cloud-native app scales out stateless compute instances behind a load balancer to absorb load, `/fleet` scales out stateless sub-agents to absorb a backlog.
>
> `/squad` is closer to a **long-lived service mesh with persistent state**. Instead of ephemeral pods, you have specialized, addressable agents with their own memory and responsibilities, coordinating with each other.
>
> And the wave-based dependency scheduling inside `/fleet`, run what's unblocked, wait, run the next wave, is conceptually the same DAG scheduling you already know from CI/CD pipelines or a Kubernetes job graph.
>
> The takeaway: the single-issue loop we're doing today is the "hello world". `/fleet` and `/squad` are how that same loop scales to a real team's backlog without you personally babysitting every single agent session.

> 🔎 **Interesting fact:** neither `/fleet` nor `/squad` change the core safety model. Every sub-agent, whether disposable (Fleet) or persistent (Squad), still opens a PR, still cannot merge its own work, and still runs in an isolated sandbox with no production access, all governed by that same GitHub control plane.

**DO (optional live demo, time permitting only):**
```bash
# Example only, run this in the Copilot CLI if time allows
/fleet Break the remaining Exercise 05 issue into independent sub-tasks
       (Azure OpenAI client setup, tag suggestion function, tests) and
       work them in parallel
```
> If you don't have time to run this live, simply describe it from the slide: point out that the orchestrator will split the objective, dispatch the independent pieces at once, and reassemble the result as a single reviewable PR.

> 👀 **WATCH FOR:** chat will likely ask "does this mean I lose control?" Reinforce: no, every sub-agent's output still lands as a reviewable PR. More agents means more parallel proposals, not less review.

> 💡 **Chat prompt:** ask chat "In your team, is your bottleneck today writing enough good issues, or reviewing enough PRs? `/fleet` and `/squad` only help if you already know how to do Exercise 01 and Exercise 03 well."

---

## Segment 6 - Exercise 03: Review the PR (0:38 to 0:48)

*Screen: Pull Requests tab, draft PR opened by Copilot*

**SAY:**
> Copilot has opened a draft PR. This is where your most important skill in AI-native development comes into play: **critical review**.
>
> Copilot is very good at writing plausible code. Plausible is not the same as correct, secure, or exactly what you asked for. You are the quality gate. That's true whether it's one agent's PR, like this one, or a fleet of ten.
>
> Before we look at any code, let's read the session log in the PR description together. Copilot explains every decision it made. This is like reading a PR summary from a junior developer, you understand their reasoning before you judge their output.

**DO:**
1. Open the draft PR on screen
2. Read the session log aloud (at least the first paragraph)
3. Go to "Files changed" and walk through the checklist, narrating clearly for viewers:

| Check | What to look for |
|-------|-----------------|
| `storage.py` exists | Has a `TaskStorage` protocol with `load()` and `save()` |
| `app.py` calls `get_storage()` | Not the old JSON functions directly |
| No hardcoded secrets | Zero connection strings or API keys visible |
| `requirements.txt` updated | Includes `azure-data-tables` and `python-dotenv` |
| New tests exist | Tests mock Azure calls, no real API calls |

**SAY:**
> If you're following along on your own PR, find at least one thing to comment on. Not because Copilot did it wrong, maybe it didn't, but because the skill of writing precise PR feedback is itself what we're practicing.
>
> Good PR comments are **specific.** Not "this could be better." Instead: "The error message on line 42 says connection failed but doesn't tell the user what env var to set. Can you include the variable name in the message?"

**DO:**
1. Demonstrate leaving a comment on a specific line in Files changed
2. Give it about 5 minutes for anyone following along to review their own PR and leave a comment, meanwhile invite chat to paste an example comment they'd leave so you can read a few out

> 🔎 **Interesting fact:** this checklist habit is what separates AI-native teams that ship reliable software from teams that ship plausible-looking bugs. Plausible is not the same as correct, and only a human reviewer with domain context can tell the difference.

> 👀 **WATCH FOR:** if chat posts a vague comment like "improve this", reply in chat asking "What specifically? What would the improved version look like?" Call out anyone who spots a real security or logic issue.

---

## Segment 7 - Exercise 04: Iterate (0:48 to 0:55)

*Screen: PR, Copilot responding to comments*

**SAY:**
> Here's the mental model I want you to hold: Copilot is a junior developer who is incredibly fast, very literal, and absolutely does not take offence at feedback.
>
> You don't throw away the work and start again. You give precise feedback and let it improve.

**DO:**
1. Watch Copilot pick up your comment and update the branch, on screen
2. Once it pushes the update, re-review the specific section you commented on
3. Ask yourself, and narrate for viewers:
   - Did it address the feedback correctly?
   - Did it introduce any new issues in the process?
   - Is the PR ready to merge?
4. If you want another round, leave a second, more specific comment
5. When satisfied: change from Draft to Ready for Review, approve, merge

> 💡 **Good examples for a second-round comment:**
> - *"The validation rejects empty strings, but doesn't trim whitespace first. A name of spaces-only should also be rejected."*
> - *"The error says 'connection failed' but doesn't include the env var name so the user knows what to set."*
> - *"Can you extract the Azure entity mapping into its own function? It's mixed in with the save logic."*

**SAY:**
> Notice: **Copilot cannot merge.** The human is always the final gate. AI-native does not mean AI-autonomous. It means AI-collaborative. That's a deliberate design decision, not a limitation, and it holds true no matter how many agents you're running.
>
> How many rounds did it take? One? Three? Drop your round count in chat, the answer depends almost entirely on how precisely you wrote the original issue.

---

## Segment 8 - Stretch Goal: Azure + AI (0:55 to 0:58, optional filler)

*Screen: code walkthrough, no live Azure account required*

> **Use this segment only if Exercises 02 to 04 finished with time to spare. Otherwise, skip straight to Closing and point to Exercise 05 as homework.**

**SAY:**
> Let's look at what happens when the ask gets harder. There are two pre-written issues in the exercises folder: migrating storage to Azure Table Storage, which we just did, and adding Azure OpenAI powered smart tag suggestions.

**DO, show the architecture pattern:**

```
CLI (app.py)
    └── storage.py
            ├── LocalStorage (default)
            └── AzureTableStorage (env var activated)
```

**SAY:**
> The key design principle here is zero breaking changes. If `AZURE_STORAGE_CONNECTION_STRING` isn't set, it falls back to local JSON. Same for OpenAI, if the env vars aren't there, the app degrades gracefully.
>
> When you review this kind of PR, look extra hard for one thing: hardcoded credentials. That's the single most critical failure mode when delegating cloud integration work to an AI agent. Everything else is a nice-to-have compared to that.

> 🔎 **Fun fact:** asking Copilot to mock cloud calls in tests, using `unittest.mock`, rather than hitting real Azure resources, is both a testing best practice and a cost and safety control. Your CI pipeline never touches a real Azure bill or a real API key.

---

## Segment 9 - Closing (0:58 to 1:00)

*Screen: README, The 5 Golden Rules*

**SAY:**
> Let's land the plane. We just walked through the full AI-native development loop together, and we zoomed out to see how that loop scales from one agent to a fleet or a squad of them.
>
> We wrote the issue. We delegated to Copilot. We reviewed the PR. We iterated via comments. We merged. And we saw that scaling up to `/fleet` or `/squad` doesn't change any of those steps, it just multiplies them.
>
> That is the loop. And the better you get at each step, the faster and higher-quality your output becomes, at any scale.

**Read the 5 Golden Rules aloud:**

1. **Write better issues**, your issue IS your prompt. Be specific.
2. **Review like a senior dev**, AI generates fast, humans verify smart.
3. **Use `copilot-instructions.md`**, give Copilot standing context about your project.
4. **Iterate, don't regenerate**, guide via comments rather than starting from scratch.
5. **Stay in the loop**, check the session log, understand what Copilot did and why.

**SAY:**
> For those of you who want to go further: Exercise 05 in the exercises folder has a ready-to-use issue for adding Azure OpenAI smart tag suggestions. Your homework: fork this repo, write the issue, and run the loop yourself.
>
> You now have the skills to do that loop on any codebase, your work projects, your personal projects, anything, whether it's one issue or ten.
>
> Thanks for watching, and thanks for all the great questions in chat today. I'll stick around for a few more minutes to answer anything we didn't get to.

---

## Emergency / Fallback Notes

**If Copilot is slow to start:**
- Share `copilot-instructions.md` and exercise READMEs on screen while waiting, the preparation content fills 5 to 10 minutes naturally
- Invite chat to review the Exercise 05 pre-written issue and discuss in chat: "What would you change? What's unclear?"

**If the PR contains a bug worth showing:**
- Use it. A real bug caught in review is the best possible demo of why human review matters
- Say: *"This is the payoff. Copilot is fast, but not infallible. We caught this on review, that's our value in the loop."*

**If the Assignees panel looks different than expected (gear icon vs. dropdown vs. "Assign to Agent" button):**
- GitHub's assignment UI has changed over time and varies by repo settings. Don't worry about matching the script's exact wording, whatever variant appears, assign the issue to **Copilot**, that's the exercise.
- If a dropdown appears with multiple AI agents listed (Copilot, Claude, Codex), select **Copilot**. This is our episode, so we're staying focused on GitHub Copilot throughout.
- If a dedicated **Assign to Agent** button appears instead, click it, it performs the same assignment to Copilot.
- If chat asks why other agents are listed at all: this is GitHub offering choice of agent, all governed under one control plane, the same security, governance, privacy, and compliance boundary applies no matter which agent a team picks. It's a platform strength, not a sign of indecision.

**If chat asks about `copilot-instructions.md` being a security risk:**
- The file lives in `.github/`, it's part of the repo, just like the README. No secrets go in here, ever.
- Secrets live in environment variables or Azure Key Vault. That's why the instructions explicitly say so.

**If chat asks whether Copilot's coding agent can be a security risk in general:**
- The agent runs inside an isolated GitHub Actions VM per session, it has no persistent access beyond that run and cannot merge, push to protected branches, or touch production directly.
- The session log gives you a full audit trail of every decision and file it touched.
- This holds true for `/fleet` sub-agents and `/squad` agents too, more agents does not mean less isolation or less review.

**If chat asks whether the coding agent needs your laptop to stay open:**
- No. The agent runs entirely on GitHub's cloud infrastructure (a GitHub Actions VM), not locally. You can close your laptop and the session keeps running.
- This is a genuine architectural difference from Copilot autocomplete or Copilot Chat in your editor, which only runs while your editor session is active.

**If chat asks why other AI agents (Claude, Codex) appear as assignee options at all:**
- GitHub's platform is built to let organizations choose which agent works best for them, without ever leaving GitHub's security, governance, privacy, and compliance model.
- That's the differentiator: choice of agent, wrapped in one consistent, auditable control plane. It's not GitHub being neutral about which agent to use, it's GitHub owning the governance layer regardless of which agent an org selects.
- For today's session, we're focused on GitHub Copilot, so keep that selection consistent throughout the exercises.

**If viewers run out of time on Exercise 01:**
- It's fine, the Azure issue template in Exercise 05 is pre-written. They can copy-paste it after the stream.
- The learning is in the *reading and understanding* the acceptance criteria, not just in typing it.

**If running behind schedule overall:**
- Cut the live `/fleet` demo inside Segment 5C entirely, but still cover the talking points, that segment's explanation is core content and should not be dropped, only its optional demo.
- If you need to trim further, shorten Segment 5B (Copilot App showcase) by skipping the deep links fun fact and the live canvas walkthrough, but keep the what-it-is, when-to-use-it, and worktrees talking points, they're core content.
- Cut Segment 8 (Azure + AI stretch) entirely, it is designed as optional filler, not core content.
- Compress Segment 3 (Context) by skipping the live `pytest` run and just stating the test count and pass rate on screen.

**Livestream-specific fallbacks:**
- If chat is quiet, seed it yourself: "If you're watching, drop a comment with your priority level default, high, medium, or low."
- If there's stream lag or a technical hiccup, narrate what's happening rather than going silent, viewers can't see your screen freeze the way an in-room audience would notice a stall.
- If a moderator is present, agree beforehand on a signal (a specific emoji or phrase) they'll use in your own chat window to flag an urgent question versus a general comment.
