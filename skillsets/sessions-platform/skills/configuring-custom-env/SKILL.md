---
name: configuring-custom-env
description: Use when adding, listing, or removing custom environment variables for Nori sessions, whether org-wide, personal to one person, or scoped to one custom agent.
---

<required>
- Use the `nori-sessions integrations` custom commands: `set-custom`, `list-custom`, `delete-custom`.
- Pick a name of uppercase letters, digits, and underscores that does not start with a digit (e.g. `MY_API_KEY`).
- If `set-custom` fails with `"field":"key"`, the name itself was rejected. Do not retry the same name; read `message`, then choose another name.
  - `"error":"invalid_key"`: the name breaks the format rule above.
  - `"error":"reserved_key"`: a built-in integration or the session machine already sets that name, or it would take over a tool for the whole session (for example `SLACK_APP_TOKEN`, `GITHUB_TOKEN`, `GH_TOKEN`, `AWS_ACCESS_KEY_ID`, `PATH`). Use the name the message suggests, or configure the owning integration instead.
- Pass secrets with `--value-file <path>`, never `--value`, so they stay out of the command line and shell history. Write the value to a file only you can read (`umask 077`), and delete the file afterwards. One trailing newline is dropped. Pass exactly one of `--value` or `--value-file`.
- Never ask the user to paste a secret into chat when the dashboard can take it instead.
</required>

# Scopes

| Scope | Flags | Reaches |
|---|---|---|
| Org (default) | none, or `--scope org` | Every session in the org |
| Personal | `--scope personal` | Only sessions that person started, and their personal automations |
| Agent | `--scope agent --agent <handle>` | Only sessions running that custom agent |

- Personal and agent scopes need the org's access-control feature. Without it, a scoped write fails with `scope must be 'org'`; say so and do not fall back to org scope for a personal secret.
- Only a signed-in person (the dashboard: Integrations → Custom environment variables) or a session with an approved `!admin` request can write personal or agent scope. A person's approval in the conversation does not count. From a session, have the person reply `!admin` and open the approval link it returns, then run `source "$HOME/.nori/env.d/broker-auth.sh"` before retrying. `!admin` works in web chat, Slack, and Discord; do not file a help request to ask whether it is available.
- Ask for `!admin` before generating a secret (for example running `ssh-keygen`) that you can only store in personal or agent scope, so you do not create and discard it.
- A personal variable written from a session belongs to the person that session works for.
- `list-custom` shows only org entries. Use `list-custom --all-scopes` to also see personal and agent entries you may view. Values are always masked.
- Delete with the same scope you saved: `delete-custom --key K --scope personal` (an admin adds `--owner <email>` to remove someone else's), or `--scope agent --agent <handle>`.

<system-reminder> A save or delete is pushed to running sessions immediately, as `$HOME/.nori/env.d/custom.sh`. A shell that was already open still has the old values; run `source "$HOME/.nori/env.d/custom.sh"` to pick up the change. </system-reminder>
