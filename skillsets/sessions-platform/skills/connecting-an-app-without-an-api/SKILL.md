---
name: connecting-an-app-without-an-api
description: Use when the user wants the agent to act on their behalf in a consumer app that has no developer API or API-key page (e.g. Partiful) - the user signs in to their own account in a private browser, and the agent reuses that sign-in to do work for them. This is the no-API equivalent of an OAuth "Connect your account" button.
---

<required>
*CRITICAL* Add the following steps to your Todo list using TodoWrite, then work them in order:

- Research the tool. Confirm that the tool or app does not have a developer API or an MCP server.
  - If it does, confirm with the user to integrate through one of those routes. Mention that this often is more stable and works better.
    - If the user confirms, read {{skills_dir}}/nori-sessions/SKILL.md and fall back to the Changing Runtime Context rules.
  - If it does not, look for existing third party developer tools and clis that wrap the application. Focus your token setup around that cli.
  - Research how to get a durable token (long-lived refresh token or persistent session cookie) for later reuse.
    - If that does not exist, fall back to a temporary token.
- Explain the plan to the user: you will open a private browser on this session that only they can reach; they will sign in to their own
   account themselves; you will save the resulting sign-in so you can continue as them. Wait for their go-ahead.
- Open the app in the session's built-in browser (mechanism below). Give them the live view URL and ask them to sign in,
   then end your turn. <system-reminder> Do not poll -- an open turn never reaches the user so they would never see the link. </system-reminder>
- When the user says they are signed in, read the signed-in session. Capture the *complete* signed-in state (cookies and
   the browser's local site storage). Verify with a read-only call.
- Ask whether to stay signed in for future sessions. Mention that saving the sign-in to the org's shared integration
   store means anyone in the organization's future sessions can also act as this signed-in account
   - If the user agrees, store it with {{skills_dir}}/configuring-custom-env/SKILL.md
   - Use nori-sessions to modify the setup script with a cli.
   - Use nori-skillsets to modify the org sessions skillset with information about the new integration.
<system-note> For temp tokens, just tell the user this is a one off. </system-note>
- Walk the user through the new capability.
- Use the connection for the work they actually asked for.
</required>

<system-note> See also: `{{skills_dir}}/authenticating-a-service-for-one-session/SKILL.md` </system-note>

# Hosting the private browser (mechanism)

Use the session's built-in browser: read and follow
`{{skills_dir}}/using-a-web-browser/SKILL.md`. Run `nori-browser`, open the
app's sign-in page in it, and give the user the live view link it prints. The
live view sits behind the session's sign-in gate, so only the user can reach it.

Confirm the gate is live before sharing -- an unauthenticated request must
bounce to login:

```bash
curl -sS -o /dev/null -w '%{http_code}\n' "$NORI_SESSION_URL/browser/"
# expect a redirect (e.g. 302) to /auth/login
```

Then hand the user the link and **end the turn**:

```
Open this and sign in to your own account:
<live view link from nori-browser>

It's a normal browser running on this session, reachable only by you.
Reply "done" once you can see your account home.
```

Once they confirm, capture the complete signed-in session from the same
browser. `storageState({ indexedDB: true })` saves cookies, local storage, and
the browser's local site database in one shot:

```js
const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
const state = await browser.contexts()[0].storageState({ indexedDB: true });
```
