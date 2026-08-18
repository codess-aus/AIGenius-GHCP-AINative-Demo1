# Exercise 03 -- Review the Draft PR

## Goal

Review Copilot's pull request with the critical eye of a senior developer.

## Your Most Important Skill

In an AI-native workflow, **critical review** is your highest-value activity. Copilot is very good at generating plausible code. But plausible is not the same as correct, secure, or aligned with your actual intent.

You are the quality gate. The AI generates fast. You verify smart.

---

## Your Task

### Step 1 -- Open the Draft PR

1. Go to the **Pull Requests** tab in your repo.
2. Open the draft PR that Copilot created from your issue.

### Step 2 -- Read the Session Log

Before looking at the code diff, read the session log Copilot included in the PR description. This explains:

- How it interpreted your issue
- What decisions it made and why
- What it chose not to do

### Step 3 -- Review the Diff

Go through the **Files changed** tab carefully. Use the checklist below as your review guide.

---

## PR Review Checklist

Use this checklist on every Copilot-generated PR:

**Correctness**
- [ ] Does the code match the acceptance criteria in the issue?
- [ ] Are edge cases handled? (empty input, invalid values, missing data)
- [ ] Does the logic make sense end-to-end?

**Code Quality**
- [ ] Is the code readable and consistent with the rest of the codebase?
- [ ] Are functions small and focused?
- [ ] Are there type hints and docstrings on new functions?

**Security**
- [ ] No hardcoded credentials, API keys, or secrets
- [ ] User input is validated before use
- [ ] No obvious injection or parsing vulnerabilities

**Dependencies**
- [ ] Are new dependencies justified and declared in `requirements.txt`?
- [ ] Are imported libraries actually used?

**Tests**
- [ ] Do existing tests still pass?
- [ ] Are there new tests for the new behaviour?

---

## Your Task (Continued)

4. Work through the checklist above.
5. Leave **at least one comment** on the PR requesting a change or asking a clarifying question.

Good comments are specific. Instead of:
> "This could be better"

Try:
> "Can you add input validation to the task name field? It should reject empty strings and names longer than 200 characters."

---

## Reflection Questions

- Did Copilot miss anything from the acceptance criteria?
- Were there any decisions in the session log you disagreed with?
- How did writing a detailed issue affect the quality of the PR?

---

## Next Step

Once you've left a review comment, move on to [Exercise 04 -- Iterate via PR Comments](../04-iterate/README.md).
