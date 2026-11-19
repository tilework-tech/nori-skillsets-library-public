---
name: using-the-sessions-ui
description: Use when explaining or reasoning about the Nori web UI, dashboard surfaces, fleet controls, or the difference between Release, Restart, and Destroy.
---

# Using the Nori UI

## The two web surfaces

- The shared organization dashboard manages conversations, projects, automations, integrations, the agent library, and settings for the fleet, users, security, and billing.
- Each claimed session machine has its own web surfaces. `$NORI_SESSION_URL/shell/` opens a shell on the machine and `$NORI_SESSION_URL/port/<N>/` serves its listening ports. The session's chat lives in the dashboard at `$NORI_SESSIONS_URL/chat/TRANSCRIPT_ID`.
- Do not confuse the shared dashboard with the per-session URLs. A fleet action in the dashboard changes session capacity; opening a per-session URL only connects to that claimed machine.

## Main dashboard areas

- **Chat** shows live and durable conversation history. The sidebar scopes are Following, Yours, Archived, and All (admins only). Tick chats and use the row menu's "Move to project…" to group them.
- **Projects** groups long-running work: its coordinator, project docs, chats, and automations. Any member can choose New project and give it a name and a desired outcome; "Start now" sends the outcome to the coordinator as its first message.
- **Agents** (admins only) holds custom agents, the Library of skillsets, skills, and subagents, and the Builder (`/agents/new`). A custom agent is an @handle with a provider and optional model, skillset, machine size, thinking level, display name, response style, integrations, and who can use it. People use custom agents by @handle in Slack, from the chat picker, or by assigning them to automations and projects.
- **Automations** manages unattended scheduled, reminder, and webhook-driven work.
- **Integrations** connects GitHub, Slack, Google Workspace, MCP servers, CLI tools, and custom environment variables. Its Token providers area holds model accounts (Claude, Codex, OpenRouter, custom endpoints); an admin's "Set as org default" on a provider's card sets the org default provider and model. Where access control is on, members connect personal integrations here too.
- **Factory** shows the daily assessment of how the org ships software, when the org has it turned on.
- **Settings** (Admin or Owner) has the Fleet (machine lifecycle, session ownership, provider, per-machine controls, and setup), Sessions (agent name and style, thread startup card, workspace and setup script, automations and release timeouts), Users (invites and roles), Security, and Billing sections, plus Views when custom views are on.

## Who sees what

- Members see Chat, Projects, Automations, and Integrations. Agents and Settings are admin only, and Billing is admin only inside Settings.
- Members can create projects and propose automations; an admin approves a member's automation ("Change awaiting approval", reviewed under "Review requests") before it runs.
- Only owners change the plan or make someone an owner.
- For the full list of what each role can do, read `{{skills_dir}}/explaining-nori/capabilities.md`.

## Fleet action vocabulary

| Action | Where | What it does |
| --- | --- | --- |
| Release / `!done` | Active chat or session command | Ends the claim, freeing a running-conversation slot, and resets the machine into the warm pool (or deletes it when the pool is full). |
| Restart | Fleet row | Ends that live session, freeing a running-conversation slot, and resets the machine into the warm pool (or deletes it when the pool is full). Depending on the fleet backend, the underlying machine may be reset or replaced. |
| Destroy | Fleet row; Admin or Owner | Ends that live session and deletes the selected machine. Fleet replenishment keeps the warm pool at its configured size. |
| Restart Fleet | Fleet toolbar; Admin or Owner | Deletes and reprovisions the whole fleet, including machines with live sessions. This interrupts all active work in the fleet. |
| Restart Oldest Idle | Fleet toolbar | Finds the least recently active claimed-idle session and ends it, freeing a running-conversation slot. It never selects a session that is actively working. |
| New Session | Fleet toolbar | Claims ready capacity for a new web session. If none is ready, the request waits for capacity rather than reusing an active session. |

Restart and Destroy both end the current live session and do not preserve its current machine workspace. The practical distinction is capacity lifecycle: Restart resets and returns capacity; Destroy deletes that machine and fleet replenishment creates a replacement. Durable conversation history, captured checkpoints, and externally stored changes are separate from the ephemeral machine workspace.

Sessions are designed to be ephemeral. Describe the concrete effect of an action without treating an abandoned or idle session like a durable server. For an active session, plainly say that Restart or Destroy ends current work; for an inactive session, avoid alarmist data-loss language.
