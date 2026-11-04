---
name: nori-sessions
description: Use when inspecting / changing global, fleet- and org-wide state — onboarding status, fleet setup and default skillset, integrations, triggers, webhooks, health, and checkpoints.
---

<system-note> Use the `sks` CLI for anything scoped to skillsets, not this nori-sessions cli. </system-note>

- `nori-sessions` (pre-installed at `~/.local/bin/`) talks to the Nori Sessions HTTP API and prints JSON for both success and failure. Use `--help` on any subcommand for syntax.
- Read the `tips` array when a response has one. Each tip names the exact command that fetches what the response left out (more pages, a broader scope or archive view, the detail behind a summary, the outcome of a pending change). A filtered or empty list does not prove a record does not exist.
- Command areas:
  - `health` - Nori Sessions reachability
  - `fleet` - inspect and update fleet setup (the org setup script)
  - `integrations` - provider and platform integrations, MCP servers, custom env vars (MCP/CLI connections take `--scope org|personal|agent`)
  - `onboarding` - first-run status, mark complete, hand off provider credentials
  - `triggers` and `webhook` - cron triggers and webhook triggers
  - `custom-agents` - named provider + model + skillset personas the org @-mentions in chat
  - `access` - who may use each custom agent (`restrict`, `grants add|remove`), the chat access policy, and the access audit log; needs the org's access-control feature (otherwise `not_found`), admin, and for changes from a session an approved `!admin` request
  - `checkpoint` - create or apply workspace checkpoint bundles
  - `transcripts` - list, summarize, and read conversations; `list` takes `--scope mine|authored|unread|all` or `--project <id>` (not both), plus `--archived` and `--cursor`
  - `memories` - search, save, revise, or delete reusable knowledge; read `{{skills_dir}}/using-session-memories/SKILL.md` for capture and retrieval guidance
- To link the user to this chat in the dashboard, run `nori-sessions transcripts resolve-session --self` and post `$NORI_SESSIONS_URL/chat/<transcriptId>` with both parts resolved.
- To shut yourself down when the user asks you to stop, end, or turn yourself off, run `nori-sessions sessions release --self --reason agent_requested`. In Slack, web chat, and the Nori CLI, Nori Sessions waits for your current reply to reach the user, then releases the machine and marks the conversation ended; in Discord the release happens immediately. Always pass `--reason`; a bare release tears the machine down mid-turn and drops your answer.

## Custom agents

A custom agent is a persona (handle + model provider + optional model + optional
skillset + optional description) that the org can @-mention in Slack (Nori
also provisions the backing Slack user group). Manage them with `nori-sessions
custom-agents`: `list`, `set`, `add`, `usergroup-conflict`, `adopt-usergroup`.

To create or update one agent, use `custom-agents add --handle <handle>
--provider <provider> [--model] [--skillset] [--size] [--description]`: it
reads the current set, merges that one agent, and writes the whole set back,
so the org's other agents are preserved.

<system-reminder> `custom-agents set` replaces the WHOLE set of custom agents.
Always `custom-agents list` first, edit that payload, and pass the full set
back (piping `list` into `set --stdin` round-trips cleanly). Omitting a handle
DELETES that agent, so never send a partial map or you will silently drop the
org's other custom agents. There is no per-agent delete. A custom agent still
assigned to a trigger cannot be removed (the API returns 409) — reassign the
trigger first. </system-reminder>

When a `custom-agents` response carries `tips` about Slack user groups, relay
them to the user as a Slack setting someone needs to change — the agent was
saved — not as a Nori failure or a missing agent permission.

<system-reminder> If a command fails, read the JSON error envelope before retrying. Authenticated commands need Nori Sessions auth from the session environment. </system-reminder>
