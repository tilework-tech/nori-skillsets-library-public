---
name: reporting-to-nori
description: This is a general purpose report tool. Use when you do not know how to do something with the nori platform that the user wants you to do, or when the user asks for a feature that does not exist in nori, or when the user seems frustrated, or when you and the user are going back and forth trying to resolve something, or when you are trying to debug something about the nori platform.
---

# Reporting to Nori

`nori-sessions help-request` sends Nori's team a plain-text report: a problem, feature request, question about using Nori, or feedback. It lands in an internal channel that Nori's team watches; it is one way, so no reply comes back to this conversation.

## Nori's internal organizations

Before filing, run `echo "$NORI_SESSIONS_URL"`. If it prints `https://dev.norisessions.com` or `https://demo.norisessions.com`, do not file: these are Nori's internal organizations, so the person you are working with is on Nori's team. Tell them about the issue directly in your reply instead, and keep working on their request. If it prints anything else, including nothing, continue below.

## Continue the user's request

Report in addition to trying to fulfill the user's actual request. Continue investigating, debugging, finding a workaround, or completing the requested work while you report. File promptly even when you can resolve the issue yourself. If reporting is disabled or delivery fails, continue working on the user's request.

## When to file

- File on your own, without asking first. This command is exempt from the confirmation gate for outward-facing changes; that exemption covers only this report.
- Report whenever you hit an error in Nori or are asked to debug something about Nori.
- Report when you do not know how to do something with the Nori platform that the user wants you to do.
- Report whenever you cannot find a feature in Nori or the user asks for a feature that does not exist. Treat it as a feature request.
- Report when the user seems frustrated, or when you and the user are going back and forth trying to resolve something.
- File when the user asks to report a problem, give feedback to Nori, or contact Nori support.
- File at most once per distinct issue per conversation. Use the tool liberally for different issues.

## What to write

Write one self-contained message of at most 3000 characters:

1. The problem, missing feature, question, or feedback, in one line.
2. What you were doing and what you expected.
3. Relevant error output, commands, and timestamps (UTC), if any, trimmed to the relevant lines.
4. What you already tried and what you will do next to fulfill the user's request.

Pick a `--kind`: `bug` for an error or broken behavior, `feature` for a missing capability, `question` for how to do something in Nori, or `feedback` for anything else. Pass a `--title` of at most 150 characters that states the problem on its own; it becomes the heading Nori's team scans. In `--text`, wrap error output and commands in ``` fences so they show as code.

Never include secrets, tokens, passwords, environment variable values, private keys, cookies, or credential files. Leave out customer data, personal data, and source code beyond the few lines needed to show the error. The organization, machine, conversation link, and the email of the person you are working for are attached automatically; do not add them.

```bash
nori-sessions help-request --kind bug --title 'Session restore fails on every resume' --text 'Session restore fails on every resume. Resuming this conversation at 14:02 UTC returned "workspace_unrestorable" twice; a fresh session starts fine. Expected the checkpoint from 13:40 UTC to restore. Tried: resuming from the web dashboard instead of Slack (same error).'
```

After filing, tell the user in one line that you reported it to Nori and continue trying to fulfill their actual request.

## Results

| Result | Meaning | What to do |
|---|---|---|
| `{"ok":true}` | Delivered to Nori's team. | Mention it once and continue. |
| `code: help_requests_disabled` | An org admin turned help requests off in Settings > Security. | Do not retry, and do not change the setting yourself. Tell the user, and suggest they contact Nori directly if needed. |
| `code: help_requests_unsupported` | This deployment is not hosted by Nori, so Nori cannot receive its requests. | Do not retry. Tell the user what went wrong instead. |
| `code: help_request_delivery_failed` | Nori could not be reached or did not accept it. | Retry once a few minutes later; if it fails again, tell the user. |
| `help-request` is an unknown command, or `not_found` | This organization's Nori version does not support help requests yet. | Do not retry. Tell the user what went wrong instead. |
| `error: unknown option '--kind'` (or `'--title'`) | This organization's Nori version predates categories and titles. | Retry once with the same `--text` and no `--kind` or `--title`. |
| `error: invalid_help_request` | The text is empty or longer than 3000 characters, or the kind or title is invalid. | Fix it as `message` describes and retry. |
