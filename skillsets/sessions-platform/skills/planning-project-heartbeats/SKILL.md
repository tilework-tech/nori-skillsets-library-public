---
name: planning-project-heartbeats
description: Use when a project needs to keep moving without someone prompting it - turning a vague goal ("keep improving it", "keep an eye on X", "check in daily", "follow up after the launch") into heartbeats and reminders that wake the project coordinator, or when a coordinator schedules itself.
---

Use an automation delivered to the project coordinator (`--deliver-to coordinator`) whenever a project should make progress while no one talks to it. Each run wakes the coordinator conversation and gives it one AUTOMATION turn. The coordinator then plans, delegates to subworkers, and reports from the project's goal, instructions, and recent work.

<required>
CRITICAL Add these steps to your todo list:

- Read the project goal and docs.md (`nori-sessions projects get`, `nori-sessions projects docs get`) and the project's automations (`nori-sessions triggers list --project "$NORI_PROJECT_ID"`).
- Name the outcome the person wants. Name what shows it is done.
- Pick the schedule shape from the table below. Use one heartbeat per project. Add a separate job only for a different cadence or audience.
- Write the prompt as standing instructions (below).
- Confirm four things with the person: the cadence in plain words, the IANA timezone, the first run time, and when to review or stop it.
- Save it with the commands below. Report the approval status.
</required>

## Choose the shape

| They say | Propose |
|---|---|
| "keep it moving", "make it better over time", "work on it while I'm away" | A weekday heartbeat every 3–4 hours in working hours, e.g. `0 9-18/3 * * 1-5` |
| "keep an eye on X", "watch X" | A heartbeat matched to how fast X changes (hourly for a rollout, daily for a backlog) that reports only changes |
| "check in daily", "send me a digest", "status every morning" | A weekday cron around 9:00 their time with one short report, e.g. `0 9 * * 1-5` |
| "follow up after the launch / merge / call" | One-time reminders at fixed offsets, such as one day and one week later |
| "until it is done", "see it through" | A heartbeat plus a review reminder in 1–2 weeks; pause the heartbeat once the goal is met |
| "remind me", "check back on this" | One one-time reminder |

- Propose the table's default and let the person adjust it. If the cadence matters and their words do not settle it, ask.
- Keep a check-in that pings people separate from heartbeats that do work. Schedule check-ins inside working hours.
- Schedule a coordinator automation at most once an hour. For anything faster, use a webhook or a standalone automation.
- If the person names no timezone, use the one on their Slack profile. Tell them which you used.
- Use fewer, well-instructed runs. Each heartbeat costs a coordinator turn, and a woken coordinator stays up until it is idle.

## Write the prompt

Write standing instructions, not a one-time task. Cover:

- What to look at: open pull requests, failed runs, the backlog, a dashboard, a channel.
- What counts as progress, and which next steps to start when there is room.
- Limits: how many new subworkers per run, and what not to touch. The coordinator defaults to at most 2 new subworkers per run, and none while 5 or more project pull requests wait for review.
- What to report and where. Report at the top level only vital findings, new or large plans, and conflicts between workstreams. Let workers report their own results in their threads.
- When to stop: the done condition. After it, the coordinator proposes pausing the heartbeat.

## Save it

From the project's coordinator, a one-time reminder takes effect at once if all of these hold:

- It is between one hour and 14 days out.
- The coordinator has fewer than 3 reminders waiting.
- It is at least an hour from each waiting reminder.

```bash
nori-sessions triggers create --type reminder --deliver-to coordinator \
  --scheduled-at "<ISO time with offset>" --name "<short name>" --prompt "<what to check and do>"
```

A recurring heartbeat, and every other reminder, waits for admin approval:

```bash
nori-sessions triggers create --type cron --deliver-to coordinator \
  --cron-schedule "0 9-18/3 * * 1-5" --timezone "<IANA timezone>" \
  --name "PROJECT_NAME heartbeat" --prompt "<standing instructions>"
```

- Outside a project session, add `--project PROJECT_ID`.
- Never pass `--slack-channel-id`, `--slack-thread-ts`, `--run-as-admin`, `--personal`, `--custom-agent-id`, `--agent-provider`, `--model`, `--skillset`, or `--size`. The API refuses them. The run uses the coordinator's agent and answers where the coordinator already talks.
- Never deliver a webhook or internal event to the coordinator. The API refuses it, because an outside payload must not steer the coordinator. Use a standalone or Slack-thread automation for those, and have it report into the project.
- If the response has `status: "pending_admin_approval"`, give the person the `approvalUrl`. Tell them the heartbeat is not active until an admin approves it.
- To stop a heartbeat, run `nori-sessions triggers update --id TRIGGER_ID --enabled false`. Never clear `--deliver-to` to stop one: each run would then start a standalone project session.

## What a run does

- If the coordinator is not running, Nori restores its conversation on a machine. Otherwise the run joins it.
- If the coordinator is busy (a person's turn, a work update, or another automation), the run waits up to 15 minutes from claiming it. Then it fails as `coordinator_busy`. It never interrupts.
- Nori records the run on the automation (last run status and the coordinator's reply), not as project work. The run never reports itself back to the coordinator.
- A coordinator bound to a Slack channel answers there. A reply of `<no-response/>` posts nothing.
