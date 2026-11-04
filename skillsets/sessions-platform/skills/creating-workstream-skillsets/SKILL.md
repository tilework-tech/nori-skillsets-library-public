---
name: creating-workstream-skillsets
description: Use when a repo, team, or project needs its own agent context beyond the org defaults.
---

<required>
CRITICAL Add the following steps to your Todo list using TodoWrite:

- Create with `sks new ${NORI_ORG}/<workstream-name>`, or fork the org skillset as a starting point: `sks fork ${NORI_ORG}/sessions ${NORI_ORG}/<workstream-name>`
- Add repo-specific context to its AGENTS.md and skills under its `skills/` directory.
- Publish with `sks upload ${NORI_ORG}/<workstream-name>`
- Activate it:
  - In Slack: `!skillsets switch <workstream-name>`
  - As a trigger default: dashboard under Triggers > Edit
  - In the org setup script: `sks switch` commands for specific workspace paths after cloning repos
- If you edited files in `~/org/sessions/` to reference the new workstream, follow the `maintaining-org-skillset` skill to test and upload.
</required>

<system-note> Workstream skillsets layer on top of the org skillset, they do not replace it. The org skillset at ~/org/ stays active; a workstream at ~/org/workspace/ adds context via directory hierarchy. </system-note>
