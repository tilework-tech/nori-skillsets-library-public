# Org Sessions Template

## Org Configuration

Edit durable org session configuration in:

```
~/org/sessions/
```

When you edit this configuration, it doesn't immediately apply to either
your session or to future sessions. To persist these edits, you must follow
the `maintaining-org-skillset` skill. You should have access to that, but
if you cannot find it then you should also look for
`nori-sessions-upload.sh` directly. That script will persist your changes
from this org sessions folder, up to your organization skillset used by all
future sessions.

## Memory

Keep stable org-wide preferences and rules in `~/org/sessions/AGENTS.md`.
Leave task-specific notes and unreviewed observations out.

## Workspace Context

The workspace at `~/org/workspace/` is specific to this session. It is not
shared across sessions (other than changes to the git version controlled
repos there). If you need repo-specific or task-specific agent
context, use the repo's own `AGENTS.md` and skills, or advise the user that
they can activate a task-specific skillset in the workspace.
