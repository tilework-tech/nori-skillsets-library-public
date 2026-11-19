---
name: configuring-codex
description: Use when setting up or verifying Codex provider credentials for Nori, including OpenAI API key handoff, Codex OAuth auth.json handoff, or skipping Codex credential persistence during onboarding.
---

<required>
CRITICAL Add the following steps to your Todo list using TodoWrite:

- Get the credentials from the user. The user can decline to provide them.
  - If the user is communicating through slack/discord/not the terminal, read and follow `{{skills_dir}}/receiving-secrets-from-chat/SKILL.md`. Receive either an API key or `~/.codex/auth.json`, and explain how to obtain either, including the macOS keychain steps.
  - Otherwise, instruct the user to get the key from /login or from https://platform.openai.com/api-keys.
- If this is first-run onboarding, confirm that the skillset has uploaded successfully and `nori-sessions onboarding complete` has returned `{"onboarded":true}`.
- Hand off the credential with `nori-sessions onboarding handoff-provider --provider codex --type api-key --api-key <key>` or `--type oauth-json --auth-json-file <path>`. If the user declines, don't do anything.
- Verify by running `nori-sessions onboarding status`. `.codex.configured` should be `true` unless the user skipped.
</required>
