---
name: configuring-slack
description: Use when installing or verifying the Nori Slack app for an org so agents can read and respond to Slack workspace messages and threads.
---

<required>
CRITICAL Add the following steps to your Todo list using TodoWrite:

- Get the install URL from `nori-sessions onboarding status` (the `.slack.installUrl` field) and have the user open it in their browser to authorize the app in their workspace. There is no token to paste back — the OAuth flow saves credentials automatically.
- Verify by running `nori-sessions onboarding status`. The `.slack` object should show `installed: true, configured: true`.
</required>
