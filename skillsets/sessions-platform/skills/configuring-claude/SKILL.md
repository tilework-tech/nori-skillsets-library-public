---
name: configuring-claude
description: Use when setting up or verifying Claude provider credentials for Nori, including API key handoff, Claude Code OAuth credential handoff, or skipping Claude credential persistence during onboarding.
---

<required>
CRITICAL Add the following steps to your Todo list using TodoWrite:

- Ask the user which credential they want to connect: a Claude subscription through a browser sign-in, or an API key. The user can decline.
- For a subscription, prefer the browser connect, which needs no secret file:
  1. Run `nori-sessions integrations claude connect-start`. It returns `authorizeUrl` and `state`. Add `--scope personal` for the person's own account, or `--scope agent --agent HANDLE` for one custom agent, where the org has access control; from a session those two scopes also need an approved `!admin` request (ask the user to reply `!admin`, end your turn, then re-source `$HOME/.nori/env.d/broker-auth.sh`). The default is the org, which needs an admin (from a session, the same approved `!admin` request).
  2. Give the user `authorizeUrl`, ask them to approve and reply with the code the page shows, and end your turn.
  3. Within 10 minutes, run `nori-sessions integrations claude connect-finish --state <state> --code <code>`.
  - `integrations claude setup-token-start` / `setup-token-finish` is the same flow for a long-lived setup token.
- For an API key or an existing `~/.claude/.credentials.json`: if the user is communicating through slack/discord/not the terminal, read and follow `{{skills_dir}}/receiving-secrets-from-chat/SKILL.md`, and explain how to get either (an API key from platform.claude.com, or the credentials file after `claude /login`, including the macOS keychain steps). Then run `nori-sessions onboarding handoff-provider --provider claude --type api-key --api-key <key>` or `--type oauth-json --credentials-file <path>`.
- If this is first-run onboarding, confirm that the skillset has uploaded successfully and `nori-sessions onboarding complete` has returned `{"onboarded":true}`.
- Verify with `nori-sessions onboarding status` (`.claude.configured` should be `true` unless the user skipped) or `nori-sessions integrations accounts list --all-scopes`. `nori-sessions integrations credential-health` lists credentials that expired and need reconnecting; reconnect a saved account in place with `connect-start --account-id <id>`.
</required>
