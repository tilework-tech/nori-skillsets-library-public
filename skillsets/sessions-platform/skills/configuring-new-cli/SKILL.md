---
name: configuring-new-cli
description: Use when adding a new CLI tool, runtime, or integration that should be available in every future session.
---

<required>
CRITICAL Add the following steps to your Todo list using TodoWrite:

- If the tool is Salesforce, stop: never connect it from a session with a CLI, MCP server, or token. Salesforce freezes users and revokes their tokens when API traffic comes from anonymizing-proxy IPs, and session machines egress from such IPs. Sessions use the managed relay instead: follow `using-salesforce`, and have an org admin connect Salesforce on the Integrations page if it is not connected.
- Check for a managed preset first: `nori-sessions integrations cli presets`. If one matches the tool (e.g. Snowflake, AWS), it already installs the CLI and handles login in every session; you only need to obtain the env vars it lists. Read each env var's `instructions` for how to get the value.
- Before anyone signs in, tell the user that persisting the credential means every session in the org acts as that account, including sessions started from Slack, triggers, and webhooks. Recommend a dedicated, least-privilege account (and a sandbox where the service has one) rather than a personal or admin account. If they only need access now, stop here and follow `authenticating-a-service-for-one-session` instead.
- Install the tool in this session and walk the user through any auth flow. Do the terminal work yourself; the user should only need to sign in through a browser.
  - If the user needs to run commands on this machine, give them the shell URL: $NORI_SESSION_URL/shell/
  - If an OAuth flow uses a localhost callback, the user will hit a page-not-found error at the end of the browser redirect. Have them copy the full localhost URL from their address bar and paste it back to you so you can curl it on this machine to complete the callback.
  - Use the alias, profile, or connection name the preset's install script expects.
- Use the tool for a real task the user cares about, or run a clear confirmatory test. Get explicit user confirmation that it works as intended.
- Only after confirmation, make it permanent:
  - If a preset matched, first check `nori-sessions integrations mcp list` (it includes CLI integrations) for an existing row with the same `provider`. Two rows for one provider silently override each other, so ask the user before replacing one with `nori-sessions integrations mcp delete --name HANDLE`.
  - Then connect it, computing both values inline so the install script is copied exactly and the secret never appears in your output. For example, with `PRESET` set to the preset's `id`:
    ```bash
    nori-sessions integrations cli connect --name "$PRESET" --provider "$PRESET" \
      --install-script "$(nori-sessions integrations cli presets | jq -r --arg id "$PRESET" '.presets[] | select(.id==$id) | .installScript // empty')" \
      --env-vars "$(CREDENTIAL_COMMAND | jq -c '{ENV_VAR_NAME: .credential}')"
    ```
    Replace `CREDENTIAL_COMMAND` with the CLI command that prints the credential as JSON, and build one key per env var the preset lists. Use the preset's `provider` if it differs from its `id`. If the preset's `installScript` is null, omit `--install-script` entirely.
    This connects it org-wide. If access control is on and the user wants it only for themselves or one custom agent, add `--scope personal` or `--scope agent --agent HANDLE` and drop `--install-script` (scoped integrations cannot carry one, so the tool must already be installed by the setup script). From a session, scoped connects need an approved `!admin` request; ask the user to reply `!admin`, then re-source `$HOME/.nori/env.d/broker-auth.sh` before retrying.
  - Otherwise, add durable install steps to the org setup script. Edit it as a file — never pass the script inline. Pull the current script with `nori-sessions fleet get-setup --org-script-out /tmp/org-setup.sh`, edit `/tmp/org-setup.sh`, then push it with `nori-sessions fleet set-setup --org-script-file /tmp/org-setup.sh`.
  - Put API keys or secrets in custom env vars (`nori-sessions integrations set-custom`).
  - If agents need instructions about the tool, add a section to `~/org/sessions/AGENTS.md` or a new skill at `~/org/sessions/skills/<tool-name>/SKILL.md`.
  - If you edited files in `~/org/sessions/`, follow the `maintaining-org-skillset` skill to test and upload.
- Tell the user that new sessions get the integration automatically, while already-running sessions need a restart (their install script only runs at provisioning), and how to revoke the credential at the service.
</required>
