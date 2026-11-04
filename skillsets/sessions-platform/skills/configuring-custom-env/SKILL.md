---
name: configuring-custom-env
description: Use when adding, listing, or removing custom environment variables that should be distributed to every Nori session in the org.
---

<required>
- Use the `nori-sessions integrations` custom commands
- Pick a name of uppercase letters, digits, and underscores that does not start with a digit (e.g. `MY_API_KEY`).
- If `set-custom` fails with `"field":"key"`, the name itself was rejected. Do not retry the same name; read `message`, then choose another name.
  - `"error":"invalid_key"`: the name breaks the format rule above.
  - `"error":"reserved_key"`: a built-in integration or the session machine already sets that name (for example `SLACK_APP_TOKEN`, `GITHUB_TOKEN`, `AWS_ACCESS_KEY_ID`, `PATH`). Use the name the message suggests, such as `MY_SLACK_APP_TOKEN`, or configure the owning integration instead.
</required>

<system-reminder> Changes are distributed to running sessions on next config refresh. </system-reminder>
