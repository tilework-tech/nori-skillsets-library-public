---
name: nori-sessions
description: Use when inspecting / changing global, fleet- and org-wide state — onboarding status, fleet setup and default skillset, integrations, triggers, webhooks, health, and checkpoints.
---

<system-note> Use the `sks` CLI to install, switch, or edit skillsets. `nori-sessions skillsets` only browses them. </system-note>

- `nori-sessions` (pre-installed at `~/.local/bin/`) talks to the Nori HTTP API and prints JSON for both success and failure. Use `--help` on any subcommand for syntax.
- The CLI covers the whole API. It does not hide commands you may lack permission for; Nori refuses those with a 401/403 error, so read the error instead of assuming a command is missing.
- Read the `tips` array when a response has one. Each tip names the exact command that fetches what the response left out (more pages, a broader scope or archive view, the detail behind a summary, the outcome of a pending change). A filtered or empty list does not prove a record does not exist.
- Command areas:
  - `health`, `version`, `auth whoami` - Nori reachability (`health live|ready`), the running server version, and the identity this CLI calls as
  - `sessions` - list, start, release, resume, and hand off session machines; the web capacity queue (`queue`, `idle`, `end-idle`); per-session history, contributors, transcript, preview URL, and file `attach`/`download`
  - `fleet` - inspect and update fleet setup (the org setup script and admin settings such as `set-setup --github-user-attribution` and `--github-signed-commits`), machine sizes (`fleet sizes list|set`), the start queue, sandbox provider, and the org agent (`get-agent|set-agent`)
  - `config` - the org default provider and model and which providers are offered (`get-provider|set-provider`, `get-models|set-model`, `get-enabled-providers|set-enabled-providers`; setters need admin), and the org's feature flags (`features`). The dashboard equivalent is "Set as org default" on Integrations > Token providers. `fleet set-agent` changes the agent's name and style, not its model
  - `billing` - plan, machine capacity, and renewal (`summary`), seats and usage, and the billing portal; admin only, and only owners change the plan
  - `integrations` - provider and platform integrations, MCP servers, custom env vars (MCP/CLI connections and custom env vars take `--scope org|personal|agent`), credential health, and provider connect flows
    - `integrations github-user status` - whether the person you work for connected their GitHub account, with the `connectUrl` they open to connect it; connecting and disconnecting happen only in their browser (`github-user disconnect` is refused unless a person is signed in)
  - `slack-proxy` - call a Slack Web API method or download a shared file with this conversation's Slack grant (`--slack-token`, else `NORI_SLACK_CONTEXT_TOKEN` from `~/.nori/env.d/slack.sh`), limited to the channels the grant covers
  - `vault` - read provider credentials session machines pull (`codex-token`)
  - `credentials` - only when your turn brief says conversational scoping is on: `credentials list` shows the credential names this machine holds and can request, with who can approve each; `credentials request <name>... --reason "<why>"` asks for them by name (Nori maps names to credentials and posts the approval card itself). Any org member who can give a name may approve it, in the conversation or not (`anyApprover`: any member or admin); Nori does not message approvers, so when one is not in the conversation, ask the user to send them the link; `credentials status <request-id>` and `credentials requests` show how requests stand. Requesting never waits: tell the user what you asked for and why, then end your turn; you are woken as people decide. You may make several requests in one conversation. A project coordinator with people in its conversation asks like any chat; automation runs and subworkers cannot request (the command exits 3: report what is missing instead). An approved credential stays with the conversation, on every machine it runs on, until the org's credential grant lifetime (from approval; the brief says how long) ends or someone revokes it; it then shows as requestable again, so request it again if you still need it. Otherwise the machine already holds every credential it may use
  - `onboarding` and `levelup` - first-run status, mark complete or skip, hand off provider credentials; the post-onboarding level-up flow
  - `triggers` and `webhook` - cron triggers and webhook triggers; `triggers create --deliver-to coordinator` wakes a project's coordinator on a schedule (see the `planning-project-heartbeats` skill)
  - `projects` - list, create, and read projects; delegate, message, stop, resume, and retry their work (`delegate|message|stop|resume|retry`, `work`, `held-work`); read and edit the project docs.md, which needs no approval (`docs get|save|history`); inspect a bounded excerpt (`docs preview --project <id> [--revision N]`); attach automations and chats (`triggers`, `chats`)
  - `workers` - independent PR reviews on separate machines (`start|list|get|result|message|stop`), owned by the current conversation; use the reviewing-github-prs skill for fixed-commit and blind-review guidance
  - `github-pr` - publish an explicitly requested fix to the current GitHub PR with its captured-head guard; run `github-pr publish --help` for required instruction evidence and supported file changes
  - `channels` - channel mode: bind a channel to a custom agent or a project coordinator (admin; differs from `projects channels`)
  - `custom-agents` and `agents` - named provider + model + skillset personas the org @-mentions in chat; which agents you can start a chat with and which harnesses the org supports
  - `access` - who may use each custom agent (`restrict`, `grants add|remove`), the access policy (`policy set` with `--admins-can-prompt-all-chats`, `--member-chat-visibility own|own-and-projects`, `--member-agent-transcript-reach own-conversation|as-person`), and the access audit log; needs admin, the org's access-control feature for everything except `policy` (otherwise `not_found`; with it off, only the member settings can be set), and for changes from a session an approved `!admin` request
  - `skillsets`, `skill-improvement`, `skillset-changes` - browse skillsets and the skills a session would install; read transcripts for a skill-improvement review (admin scope only) and submit, approve, or reject proposed org skillset changes (approval is an admin's decision)
  - `scripts` - setup scripts and their versions
  - `checkpoint` - create or apply workspace checkpoint bundles
  - `transcripts` - list, summarize, and read conversations; `list` takes `--scope mine|authored|unread|all` or `--project <id>` (not both), plus `--archived` and `--cursor`; also pin, follow, rename, archive, and resume them; prompt another conversation, cancel its running turn, and manage its queued messages (`prompt|cancel`, `queue list|edit|remove`; see Acting in other chats)
  - `multiplex` - live conversations side by side; `multiplex watch` reads the live feed for a bounded time (`--max-events`, `--timeout-ms`)
  - `stats` and `logs` - session statistics; `logs query --query <LogsQL> [--start --end --limit]` reads this org's service logs; see the `fixing-unspecified-platform-problems` skill for how to triage them
  - `memories` - search, save, revise, or delete reusable knowledge; read `{{skills_dir}}/using-session-memories/SKILL.md` for capture and retrieval guidance
  - `notifications` - list and dismiss Nori notifications
  - `help-request` - send Nori's team a help request; see the `reporting-to-nori` skill
  - `users`, `invites`, `admin-escalation` - org members, invite links, and `!admin` requests (admin)
  - `preferences`, `push`, `views` - the signed-in person's dashboard preferences, browser push subscriptions, and custom web UI views
  - `assets` - durable, shareable web pages and tools: `create`, `publish <id> --dir <dist> --note`, `versions`, `rollback --to`, `share --user|--org-role`, `unshare`, `transfer`, `delete|restore`, `store get|list|put|update|cas|delete <id> <collection> [<key>]` (the asset's data; `cas --expected-v 0` claims exactly once), `usage` (org admins); only where the org's `assets` feature is on (otherwise every command is `not_found`)
  - `factory` - the org's saved Factory assessment of how it ships software (`factory get`); `save` is reserved for the factory-discovery automation run
  - `suggestions` - the personal suggestions shown under the web composer; `save` is reserved for each person's own suggestions research run
  - `one-connect` - personal and shared app connections through One, where the org has it (`status`, `authorize`, `disconnect`, `catalog`; `share-apps` needs admin)
  - `tours`, `set-pieces`, `scripted-onboarding`, `onboarding-v3` - internal to Nori's onboarding flows; use them only when an onboarding skill tells you to
  - `e2e` - Nori-internal end-to-end testing utilities; refused unless the deployment enables them
- To link the user to this chat in the dashboard, run `nori-sessions transcripts resolve-session --self` and post `$NORI_SESSIONS_URL/chat/<transcriptId>` with both parts resolved.
- To shut yourself down when the user asks you to stop, end, or turn yourself off, run `nori-sessions sessions release --self --reason agent_requested`. In Slack, web chat, and the Nori CLI, Nori waits for your current reply to reach the user, then releases the machine and marks the conversation ended; in Discord the release happens immediately. Always pass `--reason`; a bare release tears the machine down mid-turn and drops your answer.

## Acting in other chats

You can start, prompt, and steer other chats as the person you work for (the
latest person to write to you, else whoever started your session). They are shown as sent "via a session agent"
(`Agent`), and you get no more access than that person and your session
credential both allow.

- Start a chat: `sessions acquire` (a new chat; resume and purpose sessions
  need a person), or `sessions queue --draft-id <id> --prompt <text>` when the
  fleet is full.
- Prompt a chat: `transcripts prompt --id <id> --prompt <text>`. It answers
  `started`, `queued`, or `waiting_for_machine`. While a turn runs it is
  refused with `turn_in_flight`; add `--queue` to run after that turn. The
  command does not wait for the reply; read it with `transcripts get --id <id>`.
- Stop a turn: `transcripts cancel --id <id>` (`no_turn` when nothing runs).
- Queued messages: `transcripts queue list --id <id>`, then
  `queue edit|remove --id <id> --message-id <clientMessageId>`. You may change
  only messages a session agent queued, never ones the person typed
  (`not_sender`). Queues need the org's message-queue feature
  (`queue_unavailable` otherwise).

Limits, each refused with its `code`:

- You cannot act on your own conversation (`own_conversation`).
- In a chat another session agent started, you cannot start or act in other
  chats (`nested_agent_chat`); ask the person to do it.
- One machine may start at most 10 chats (`agent_chat_rate_limited`) and send
  at most 30 prompts (`agent_prompt_rate_limited`) per rolling hour. Refused
  requests do not count. Wait rather than retrying in a loop.

## Project docs links

Project docs and references share the project’s `docs.md`; do not create a
separate references store. Run `nori-sessions projects docs get --project <id>`
and use its returned revision when linking the content you read:
`$NORI_SESSIONS_URL/projects/<id>?details=docs&revision=<revision>`. A revision
returned by `projects docs save` may also be linked. Resolve the dashboard URL
and quote the complete URL in shell commands so `&` is preserved.
`projects docs preview --project <id> [--revision N]` returns a bounded JSON
excerpt; use `docs get` when the task requires reading the full document.

A revision link opens that immutable revision, with a docs preview in web chat
and a compact Slack excerpt when the audience is authorized. Use
`?details=docs` without `revision` only for an intentionally mutable latest-docs
link. Keep `/projects/<id>` for the generic project card.

## Custom agents

A custom agent is a persona (handle + model provider + optional model + optional
skillset + optional description) that the org can @-mention in Slack (Nori
also provisions the backing Slack user group). Manage them with `nori-sessions
custom-agents`: `list`, `set`, `add`, `sync`, `usergroup-conflict`,
`adopt-usergroup`.

To create or update one agent, use `custom-agents add --handle <handle>
--provider <provider> [--model] [--skillset] [--size] [--thinking]
[--description]`: it reads the current set, merges that one agent, and writes
the whole set back, so the org's other agents are preserved.

`--thinking <level>` (alias `--effort`) pins the reasoning level the agent's
conversations start at; blank clears it to the org default. The allowed
levels depend on the agent's harness and model, and Nori rejects others
with the list. Never encode a level in the model id (`model#medium`): pass
the bare model and `--thinking medium`.

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

When the reason is `permission_denied`, also offer to change the setting
together in the session browser:

1. Ask whether the user is a Slack workspace admin and is at a desktop. Slack
   admin settings do not work from the mobile app. If they are not an admin,
   give them the tips' steps to forward to one and stop.
2. Follow `{{skills_dir}}/using-a-web-browser/SKILL.md`. Open the
   account-types URL from the tips, send the live view link, and ask the user
   to sign in to Slack there. End your turn.
3. When they reply, find "Create and edit user groups" and show the user the
   change: set it to Everyone. This changes their whole Slack workspace, so
   save only after they approve it. Offer "Disable user groups" set to
   Everyone as a separate, optional change; it only lets Nori retire removed
   agents' groups. Change nothing else.
4. Run `nori-sessions custom-agents sync` and report each agent's @-handle.
   If the response still carries tips, relay them. If sync returns 403, say
   that an org admin can retry from the Agents page, or that Nori
   retries on its own within the hour.
5. Ask the user to sign out of Slack in the live view, or sign out for them
   once they agree.

Until the setting changes, agents work as `@<bot> +<handle>`. Nori also
retries the sync every hour, so a fix made outside the session is picked up
without a re-save.

## Machine sizes

`nori-sessions fleet sizes list` shows the sizes members may pick, the
`default` setting (`auto` or a pinned size), `effectiveDefault` (the size the
warm pool runs right now), and `recentClaims` (how recent sized starts voted).
`fleet sizes set --enabled small,medium --default <auto|size>` changes them
(admin; both commands answer `not_found` when the org lacks machine sizes).

The warm pool holds only one size. A custom agent, automation, or project
saved with any other size starts on a fresh machine that boots cold (minutes,
mostly the org setup script) and is destroyed on release. So pinning a
`--default` different from the sizes custom agents and automations save makes
every one of those starts cold.

<system-reminder> Prefer `--default auto`: the warm pool then follows the size
most recent sized starts ask for. Before changing a default or an agent's or
automation's `--size`, run `fleet sizes list`, compare against the sizes saved
on custom agents and automations, and tell the user which starts will go cold.
Do not pin a default that differs from those sizes unless the user asks for it
after hearing that. </system-reminder>

<system-reminder> If a command fails, read the JSON error envelope before retrying. Authenticated commands need Nori auth from the session environment. </system-reminder>
