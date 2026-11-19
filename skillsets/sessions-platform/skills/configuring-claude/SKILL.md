---
name: configuring-claude
description: Use when setting up or verifying Claude provider credentials for Nori, including API key handoff, Claude Code OAuth credential handoff, or skipping Claude credential persistence during onboarding.
---

<required>
CRITICAL Add the following steps to your Todo list using TodoWrite:

- Get the credentials from the user. The user can decline to provide them.
  - If the user is communicating through slack/discord/not the terminal, read and follow `{{skills_dir}}/receiving-secrets-from-chat/SKILL.md`. Receive either an API key or `~/.claude/.credentials.json`, and explain how to obtain either, including the macOS keychain steps.
  - Otherwise, instruct the user to get the key from /login or from platform.claude.com.
- If this is first-run onboarding, confirm that the skillset has uploaded successfully and `nori-sessions onboarding complete` has returned `{"onboarded":true}`.
- Hand off the credential with `nori-sessions onboarding handoff-provider --provider claude --type api-key --api-key <key>` or `--type oauth-json --credentials-file <path>`. If the user declines, don't do anything.
- Verify by running `nori-sessions onboarding status`. `.claude.configured` should be `true` unless the user skipped.
</required>
