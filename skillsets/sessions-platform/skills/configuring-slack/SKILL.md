---
name: configuring-slack
description: Use when installing or verifying the Nori Slack app for an org so agents can read and respond to Slack workspace messages and threads.
---

<required>
CRITICAL Add the following steps to your Todo list using TodoWrite:

- Run `nori-sessions onboarding status` and read `.slack`. If it already shows `installed: true, configured: true`, stop: Slack is connected. Installing needs an org admin; for anyone else the status has no install links, so ask an admin to do it, or to approve this session's `!admin` request.
- Install the app:
  - Shared Nori Slack app (the default, `.slack.installAction` is `shared`): run `nori-sessions onboarding slack install` and give the user the link it returns. Do not hand out `.slack.installUrl` itself; for the shared app it is an API path, not a page.
  - Dedicated app (`.slack.installAction` is `dedicated`, for orgs that have one): give the user `.slack.installUrl` (or `.slack.dedicated.installUrl`).
  - Or have an admin use the Slack card on the dashboard's Integrations page.
  The user authorizes the app in their browser. There is no token to paste back; the OAuth flow saves credentials. End your turn while they do it.
- If the workspace is already connected to another Nori organization, an admin of this org approves moving it here with `nori-sessions onboarding slack approve-transfer --workspace-id <id>`.
- Verify with `nori-sessions onboarding slack readiness` and `nori-sessions onboarding status` (`.slack` should show `installed: true, configured: true`). Then invite the bot to the channels it should use.
</required>
