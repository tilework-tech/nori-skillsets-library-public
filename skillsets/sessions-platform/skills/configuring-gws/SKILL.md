---
name: configuring-gws
description: Use when connecting or authenticating the Google Workspace (gws) integration for an org so sessions can use the gws CLI for Drive, Gmail, Calendar, Docs, Sheets, Slides, and Tasks, plus the YouTube Data and Analytics APIs. Use this instead of walking the user through gcloud.
---

<required>
CRITICAL Add the following steps to your Todo list using TodoWrite:

- This is an org-wide change, so it requires admin escalation. You cannot trigger `!admin` yourself — ask the user to reply `!admin` in this thread, then end your turn and wait for the approval to land.
- Once approved, re-source the auth env file so the admin command uses the fresh token instead of the stale one captured at session start: `source "$HOME/.nori/env.d/broker-auth.sh"`.
- Get the connect link with `nori-sessions integrations gws-connect-link` (prints `{"url":"..."}`). Post that URL to the user and ask them to open it in their browser and complete the Google consent screen. There is no token to paste back — the OAuth flow saves the org credentials automatically.
- After the user confirms they finished consent, re-source the gws credentials so the `gws` CLI works in this session immediately: `source "$HOME/.nori/env.d/gws-credentials.sh"`. Future sessions receive it automatically.
- Verify with a real call, e.g. `gws drive files list --params '{"pageSize":1}'`. Do not fall back to `gcloud`.
</required>

<system-reminder> If `gws-connect-link` returns `404 GWS OAuth not configured`, Nori has no Google OAuth client set up yet — that is a separate prerequisite, not something the connect link can fix. Surface this to the user rather than retrying. </system-reminder>

<system-reminder> When access control is on, Google accounts can also be personal or per-agent. Any member can connect their own personal Google account, and an admin can connect one for a custom agent, from the Google Workspace card on the Integrations page (a signed-in browser is required, even with an approved `!admin`; `gws-connect-link` only issues the org link). Each connect chooses Read-only or Read and write. A session gets exactly one account: its agent's, else the person who started it, else the org's. No `!admin` is needed for a personal connect. A write failing with insufficient scopes may mean the session's account was connected read-only. </system-reminder>

<system-reminder> The `gws` CLI has no YouTube service. Call the YouTube APIs directly with the same token, e.g. `curl -sS -H "Authorization: Bearer $GOOGLE_WORKSPACE_CLI_TOKEN" "https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true"`. Before blaming scopes on a YouTube error, check what the token actually grants: `curl -s "https://oauth2.googleapis.com/tokeninfo?access_token=$GOOGLE_WORKSPACE_CLI_TOKEN" | jq -r .scope`. Only if the YouTube scopes are missing was the integration connected before they were added; an org admin must then reconnect via `nori-sessions integrations gws-connect-link`. Other failures are not fixed by reconnecting: `quotaExceeded` (the YouTube quota is shared across all Nori orgs), `forbidden` (YouTube is disabled for the account in the Workspace Admin console), or `youtubeSignupRequired` / an empty `items` list from `channels?mine=true` (the account has no channel). </system-reminder>
