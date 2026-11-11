---
name: using-the-sessions-ui
description: Use when explaining or reasoning about the Nori Sessions web UI, dashboard surfaces, fleet controls, or the difference between Release, Restart, and Destroy.
---

# Using the Nori Sessions UI

## The two web surfaces

- The shared organization dashboard manages conversations, sessions, the fleet, integrations, triggers, users, security, and the skill registry.
- Each claimed session machine has its own web surfaces. `$NORI_SESSION_URL/shell/` opens a shell on the machine and `$NORI_SESSION_URL/port/<N>/` serves its listening ports. The session's chat lives in the dashboard at `$NORI_SESSIONS_URL/chat/TRANSCRIPT_ID`.
- Do not confuse the shared dashboard with the per-session URLs. A fleet action in the dashboard changes session capacity; opening a per-session URL only connects to that claimed machine.

## Main dashboard areas

- **Chat and Sessions** show live and durable conversation history.
- **Fleet** shows machine lifecycle, session ownership, recent activity, provider, and per-machine controls.
- **Fleet Setup, Integrations, Users, and Security** manage organization-wide configuration and access. Some of these surfaces require an Admin or Owner role.
- **Triggers** manages unattended scheduled and webhook-driven work.
- **Skillsets, Skills, Agents, and related registry pages** manage the agent context and capabilities available to sessions.

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
