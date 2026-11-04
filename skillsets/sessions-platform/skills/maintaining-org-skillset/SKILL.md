---
name: maintaining-org-skillset
description: Use after editing any file in the org sessions skillset to test and upload changes so future sessions receive them.
---

<required>
CRITICAL Add the following steps to your Todo list using TodoWrite:

- Edit through `~/org/sessions/` (a symlink to the true location at `~/.nori/profiles/${NORI_ORG}/sessions/`). Contents: `AGENTS.md`, `skills/`, `nori.json`.
- Test the change. A running agent does not reload instructions mid-conversation — for behavioral changes, start a new chat on the same session machine to confirm the agent interprets the change as intended. For small obvious edits, verifying the file reads correctly is enough.
- If you added a new skill directory under `~/org/sessions/skills/`, declare it in `~/org/sessions/nori.json` under the `skills` array with `id`, `name`, and `description` fields.
- Run `nori-sessions-upload.sh` and confirm it prints success. Future sessions download the updated skillset during provisioning.
</required>

<system-reminder> For the org sessions package, always use `nori-sessions-upload.sh`, never `sks upload` directly — the wrapper enforces org-scoped publishing and refuses to publish to the public registry. Other skillsets (e.g. workstream packages) use `sks upload` directly. </system-reminder>
