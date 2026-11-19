---
name: configuring-codex
description: Use when setting up or verifying Codex provider credentials for Nori, including OpenAI API key handoff, Codex OAuth auth.json handoff, or skipping Codex credential persistence during onboarding.
---

<required>
CRITICAL Add the following steps to your Todo list using TodoWrite:

- Ask the user which credential they want to connect: a ChatGPT subscription through a device-code sign-in, or an OpenAI API key. The user can decline.
- For a ChatGPT subscription, prefer the device-code connect, which needs no secret file:
  1. Run `nori-sessions integrations codex connect-start`. It returns `verificationUri`, `userCode`, and `flowId`. Add `--scope personal` for the person's own account, or `--scope agent --agent HANDLE` for one custom agent, where the org has access control; from a session those two scopes also need an approved `!admin` request (ask the user to reply `!admin`, end your turn, then re-source `$HOME/.nori/env.d/broker-auth.sh`). The default is the org, which needs an admin (from a session, the same approved `!admin` request).
  2. Give the user `verificationUri` and `userCode`, ask them to sign in and enter the code, and end your turn.
  3. When they reply, run `nori-sessions integrations codex connect-status --flow-id <flowId>` until it reports `connected` or `failed`.
- For an API key or an existing `~/.codex/auth.json`: if the user is communicating through slack/discord/not the terminal, read and follow `{{skills_dir}}/receiving-secrets-from-chat/SKILL.md`, and explain how to get either (an API key from https://platform.openai.com/api-keys, or `auth.json` after `codex login`, including the macOS keychain steps). Then run `nori-sessions onboarding handoff-provider --provider codex --type api-key --api-key <key>` or `--type oauth-json --auth-json-file <path>`.
- If this is first-run onboarding, confirm that the skillset has uploaded successfully and `nori-sessions onboarding complete` has returned `{"onboarded":true}`.
- Verify with `nori-sessions onboarding status` (`.codex.configured` should be `true` unless the user skipped) or `nori-sessions integrations accounts list --all-scopes`. `nori-sessions integrations credential-health` lists credentials that expired and need reconnecting; reconnect a saved account in place with `connect-start --account-id <id>`.
</required>
