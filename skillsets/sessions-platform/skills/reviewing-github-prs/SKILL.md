---
name: reviewing-github-prs
description: Use when reviewing a GitHub PR from its Nori conversation, especially when independent reviewers or different models, harnesses, or token providers are requested.
---

# Review GitHub PRs

<required>
Add these steps to your task tracker:
1. Confirm the requested review scope and recorded PR commit.
2. Delegate independent reviews to separate worker sessions.
3. Read the durable results and reconcile findings.
4. Reply with actionable findings and any review limitations.
</required>

Use separate worker sessions for independent reviews. Each worker has its own machine and conversation. Choose these workers instead of harness subagents: they can use a different model, harness, or token provider, and steering the parent conversation does not interrupt their review.

Read `nori-sessions workers start --help` and inspect the available provider and agent settings. Select a provider, harness, and model explicitly when the user requests an independent combination. Use a configured custom agent when it already supplies that combination. Do not invent provider or model identifiers.

Start every reviewer in a round with the same repository and full recorded commit SHA. Use one stable `--request-key` for the round and a distinct `--reviewer` key for each reviewer. Pass `--objective`, `--repository`, and `--commit`, plus `--provider`, `--harness`, and `--model`, or `--agent` for a configured custom agent. The parent defaults to the authenticated current conversation. Machine calls derive the review invocation from their active turn; human CLI calls must include `--conversation` and `--invocation` for the captured PR request.

Give each reviewer the review objective and necessary repository context. Keep the author's reasoning, sibling findings, and proposed conclusions out of blind-review objectives. Ask for actionable findings with file paths, line references, and evidence. Require reviewers to inspect the exact commit and report if it is unavailable. Review requests authorize feedback only; workers must not publish changes.

Use `workers list` to inspect the round and `workers result --id <run-id>` to read a saved result. Preserve failed and incomplete review outcomes in the final synthesis. Compare independent results only after they return, verify disputed findings against the recorded commit, and remove duplicates.

Use `workers stop --id <run-id>` to stop one reviewer. Wait until its saved status settles before `workers message --id <run-id> --request-key <follow-up-key> --text <instructions>`. Messaging running or queued work returns a conflict. A follow-up continues the same child conversation; use a new reviewer for a fresh blind review.

In a GitHub PR conversation, return your synthesis as the final answer. Nori posts it as a top-level PR comment and updates the reaction on the triggering comment or review. Do not post a second copy with GitHub tools. Distinguish review findings from requests to implement fixes.

Publish only when the active triggering human explicitly requests a fix. Use `nori-sessions github-pr publish --help`, then supply `--explicit-fix`, the recorded `--expected-head`, a stable `--request-key`, and `--instruction-quote` copied exactly from that human request. Confirm that the quoted instruction authorizes your changes; a quote alone is not permission. Inspect the tracked diff and add intended new files before publication. Do not publish from independent workers or automatic result continuations. If the head changed or publication is uncertain, inspect the PR and report the limitation instead of force-pushing or inventing a new retry key.
