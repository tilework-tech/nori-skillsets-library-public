---
name: configuring-triggered-runs
description: Use for any scheduled or proactive work (triggered session automations) - nightly jobs, one-time reminders, any cron timing, scheduled maintenance, or waking a session from a webhook. Examples - polling for new PRs, weekly docs cleanup, nightly end-to-end tests of the day's biggest merge, or triaging errors the moment a Sentry, Grafana, or Alertmanager webhook fires.
---

# Triggered session automations

A trigger starts an automation: each run claims a fresh session machine, sends the prompt to an agent with no human present, then releases the machine. The dashboard calls these Automations. They are stored in Nori, so no skillset upload is needed. Never use `/schedule`, `/loop`, `ScheduleWakeup`, or `CronCreate`; they die with this session.

<required>
CRITICAL Add these steps to your todo list:

- List existing triggers first (`nori-sessions triggers --help` for syntax).
- Decide **when**, **who**, and **where** (below).
- Write the prompt as the task only. Nori already tells the agent no human is present and to finish without asking questions, and wraps webhook payloads as untrusted data. Do not repeat any of that.
- Cron or reminder: confirm the IANA timezone with the user, then offer a dry run (`nori-sessions triggers test`). Webhook: tell the user they can test it from Automations > Run now.
- Save. If the response has `status: "pending_admin_approval"` or `pendingChange`, give the user the `approvalUrl` and stop; it is not active. Otherwise read the trigger back and verify it.
- Report when, who, where, approval status, and any assumptions.
</required>

## When

- **Cron**: the default for recurring work and polling (new PRs, nightly tests, weekly cleanup).
- **Reminder**: one time, at a set moment.
- **Webhook**: proactive sessions. An external system (Sentry, Grafana, Alertmanager, CI) POSTs and the agent reacts in seconds, with the payload appended to the prompt.
- Any trigger's prompt may call another trigger's webhook URL, e.g. a nightly poll that fires a triage trigger per finding.

Use IANA zones (`America/New_York`), never abbreviations or offsets. Cron is wall-clock time and follows daylight saving. With no zone given, propose one (e.g. from the requester's Slack profile) and confirm. A trigger with no stored zone is legacy and fires in UTC; say so.

## Who

Pick exactly one:
- Org defaults: pass nothing.
- A custom agent: `--custom-agent-id <profileId>` (list custom agents for the id). Later edits to the agent apply automatically.
- Manual: `--agent-provider`, `--model` (needs `--agent-provider`), `--skillset`.

Automations run with org-wide credentials (plus the custom agent's) by default, not the requester's. If the job must read the requester's own personal integrations (their inbox, calendar, personal MCP servers), add `--personal true`:
- Cron or reminder only, standalone only (no `--slack-channel-id` / `--slack-thread-ts`; have the prompt post with the Slack CLI instead), not with `--run-as-admin true`, and not in a project (`--personal true` skips the session's default project). Refused when the org has access control off.
- It runs as its author. Only the author can change it, test it, turn personal off, or chain an internal-event automation off it; anyone else can only pause it, and only the author sees its last-run output. If the author leaves the org, runs fail rather than fall back to org credentials.

When your turn brief says conversational scoping is on, each run gets the org's and its custom agent's credentials, read at run time, plus the credentials attached with `--credential <name>` (repeatable; `update --no-credentials` detaches all). Runs never request more.
- You can attach only credentials a person gave this conversation (`nori-sessions credentials list` shows them as held). A person can see what they could attach with `triggers attachable-credentials`.
- Attaching anyone's personal credential needs the personal shape above: cron or reminder, standalone, no thread, not `--run-as-admin true`, not in a project. Only its author can test-fire it, and while it carries another person's credential, others can only pause it or change what is attached.
- If an attached credential is gone when the automation fires (owner left, lost access, deleted it), the run fails at once with a message naming it.

## Where

- **Standalone** (no `--slack-channel-id`): for background jobs. Nothing is posted unless the prompt names an exact destination (`#eng-updates`), and the bot must be in that channel (no DMs). Required for `--run-as-admin true` and `--personal true`.
- **Slack thread** (`--slack-channel-id <id>`): for having the agent bring you collaborative work. Each run opens a thread, Nori posts the prompt and final reply, and people reply to keep working with the agent. Don't also tell the agent to post, or it appears twice.
- **Project coordinator** (`--deliver-to coordinator`): for keeping a project moving. Each run wakes the project's coordinator conversation (restoring it if it is not running) and gives it the prompt as one AUTOMATION turn; the coordinator plans, delegates, and answers where it already talks. Cron or reminder in a project only, at most hourly, with no Slack, agent, size, admin, or personal settings. Follow the `planning-project-heartbeats` skill to turn a vague goal into the right heartbeat or reminder.

`--slack-thread-header` sets the channel post in thread mode:
- `standard` (default, recommended): a short header (name, schedule, agent). Everything else stays in the thread, keeping walls of text out of channel history.
- `agent`: nothing is posted while the agent works; its final reply becomes the channel post and starts the thread. All of the reply lands in the channel, so ask for a brief reply in the prompt. If the run fails or replies with nothing, nothing is posted (the run still shows in the automation's history).

### Running in an existing thread

A run can work under an existing message in the trigger's own `--slack-channel-id` instead of opening a new thread. No new channel post is made; Nori adds one short "Automation X is working in this thread" reply.
- Every run: `--slack-thread-ts <ts>` on create/update (blank clears; not allowed with `--slack-thread-header agent`).
- One run: `nori-sessions webhook fire --trigger-id <id> --slack-thread-ts <ts>` (needs the trigger's webhook secret: pass `--webhook-secret <secret>` from `triggers list`, or be signed in and it is looked up), or append `?slackThreadTs=<ts>` to the webhook URL and send the secret in the `X-Nori-Webhook-Secret` header. `triggers test` takes the same flag; it needs read access to the automation (if `triggers list` shows it to you, you can target a thread with it). Put the target in the query string, never the payload; put the secret in the header, never the URL. `--slack-channel-id`/`slackChannelId` is optional and must equal the trigger's channel.
- A reply's ts resolves to its thread root. The bot must be in the channel.
- The webhook URL alone can only start new threads. Steering a run into an existing thread needs the webhook secret (webhook fires) or read access to the automation (test fires, the same people who can see the secret); otherwise the fire is refused with 403 `target_unauthorized` and nothing is posted. Keep the URL and the secret private all the same.
- If anything already holds the thread (a live or recovering session, queued work, messages being handled, another automation), the run fails fast as `thread_busy` (webhook/test answer 409). It never waits or interrupts. After `!done` or idle cleanup the thread is free.
- A thread with history resumes its conversation; if the trigger sets its own agent, model, or skillset, those are switched in, and a different provider starts fresh from a thread digest. A thread without history gets a new session. Replies in the thread keep talking to that session.

## Notes

- An admin's creates and updates take effect at once. Non-admin creates and updates wait for admin approval (the automation shows "Change awaiting approval" and an admin approves it under "Review requests" on the Automations page, or with `triggers approve` / `reject`; a member's form button reads "Submit for approval"); the old version keeps running meanwhile. Deleting is admin-only.
- When an automation starts failing (not on every repeat failure), Nori posts a short notice to the automation's origin channel, by default the Slack or Discord channel it was created from (none for dashboard-created automations). Use `--origin-channel-id <id>` on create or update to send notices to a shared Slack channel instead (the bot must be in it; a DM only for a personal automation, and only its author's own), or `--clear-origin-channel` on update to stop them.
- In a project session, `triggers create` files the trigger under `$NORI_PROJECT_ID` (except with `--personal true`). Pass `--project <id>` or `--project ''` to change that; `update` only changes it when `--project` is passed.
- A run of a project automation records a project run and starts by reading the project's docs.md, which it may also fix; while the project is archived or held, its firings wait. A coordinator-delivered run records nothing in project work: its record is the coordinator's conversation and the automation's last run.
- A project's coordinator can create a one-time reminder delivered to itself between one hour and 14 days out without admin approval, while it has fewer than 3 waiting, each at least an hour apart. Everything else follows the approval rule above.

<system-reminder> Webhook URLs are unauthenticated. Treat them as secrets. </system-reminder>
