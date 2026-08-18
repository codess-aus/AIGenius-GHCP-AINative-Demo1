# Exercise 04 -- Iterate via PR Comments

## Goal

Refine Copilot's work through PR comments rather than starting from scratch.

## The Mental Model

Think of Copilot as a junior developer who is incredibly fast, very literal, and needs clear direction. You are not discarding their work and rewriting it yourself -- you are giving feedback and letting them improve it.

This is collaborative iteration. You don't start over. You refine.

---

## Your Task

### Step 1 -- Review Your Comment from Exercise 03

Go back to the draft PR you reviewed in Exercise 03. Find the comment you left requesting a change.

### Step 2 -- Watch Copilot Respond

Copilot will pick up your comment and update the branch. Watch it:

- Interpret your feedback
- Make the requested changes
- Push the updated code to the same PR

### Step 3 -- Re-review

Once Copilot has responded, review the updated diff:

- Did it address your feedback correctly?
- Did it introduce any new issues?
- Is the PR ready to merge?

### Step 4 -- Leave Another Round of Feedback (Optional)

If the changes need further refinement, leave another comment. Be even more specific this time.

Examples of effective iteration comments:

> "The validation you added rejects empty strings, but it does not trim whitespace first. A task name of '   ' (spaces only) should also be rejected."

> "Can you move the CSV export logic into its own function? The current implementation mixes I/O and formatting in a way that will be hard to test."

> "The error message on line 42 says 'invalid input' but doesn't tell the user what valid input looks like. Can you improve it?"

### Step 5 -- Approve and Merge

When you are satisfied with the PR:

1. Change the PR from **Draft** to **Ready for Review**.
2. Leave a final review approval.
3. Merge the PR.

Remember: **Copilot cannot merge.** The human is always the final gate. This is intentional. AI-native does not mean AI-autonomous. It means AI-collaborative.

---

## Reflection Questions

- How many rounds of iteration did it take to get a result you were happy with?
- How did the precision of your comments affect the quality of Copilot's updates?
- What would you do differently in the original issue to reduce the number of iterations needed?

---

## Congratulations

You have completed the full AI-native development loop:

```
Write Issue  ─►  Assign to Copilot  ─►  Review PR  ─►  Iterate  ─►  Merge
```

You operated as the tech lead. You defined what to build and why. Copilot handled the implementation. You verified the result and guided it to completion.

That is AI-native development.

---

## What Next?

- Explore the [GitHub Copilot documentation](https://docs.github.com/en/copilot)
- Try the [Copilot CLI](https://docs.github.com/en/copilot/using-github-copilot/using-github-copilot-in-the-command-line): `gh copilot suggest "undo my last commit but keep the changes"`
- Write a `copilot-instructions.md` for one of your own projects
