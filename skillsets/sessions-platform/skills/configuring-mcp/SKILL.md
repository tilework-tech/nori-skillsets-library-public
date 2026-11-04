---
name: configuring-mcp
description: Use when a user wants to connect an MCP server integration (Linear, Notion, Sentry, a custom or self-hosted server) or a static-token CLI integration to the org so its tools reach every session.
---

<required>
CRITICAL Add the following steps to your Todo list using TodoWrite:

- Identify the server. Search the built-in catalog for a known provider with
  `nori-sessions integrations mcp catalog --search NAME`; each hit returns its
  serverUrl and authType. For a server that is not in the catalog, get its
  remote URL from the user and confirm it advertises OAuth with
  `nori-sessions integrations mcp probe --server-url SERVER_URL`.

- Connect an OAuth server and hand the auth link to the user. Run
  `nori-sessions integrations mcp connect --provider ID --name HANDLE --server-url SERVER_URL`
  (use the catalog entry's id, or `custom` for a server not in the catalog; a
  server without Dynamic Client Registration also needs `--client-id` and
  `--client-secret` from a client you pre-registered with it).
  The response carries an authUrl. Post that URL into the thread as plain text
  with no formatting around it. When the user opens it and approves, Nori Sessions
  finishes the connection and adds it to the org integrations — you run nothing
  else.

- Handle the localhost fallback. If `connect` returns needsLocalhost instead of
  an authUrl, the server requires a local redirect. Give the user the returned
  scriptUrl to run on their own machine, then poll
  `nori-sessions integrations mcp localhost-status --session-id SESSION_ID`
  until the status is completed.

- Connect a static-token server instead of OAuth when the server only takes an
  API key or bearer token. Do not ask the user to paste the secret into chat;
  obtain it with the `receiving-secrets-from-chat` skill, then run
  `nori-sessions integrations mcp connect --provider ID --name HANDLE --bearer-token TOKEN`.
  A managed CLI tool that only needs static env vars uses
  `nori-sessions integrations cli connect --name HANDLE --provider ID --env-vars '{"KEY":"value"}'`.

- Verify. `nori-sessions integrations mcp list` should show the server with a
  connected status. To confirm the credential is live, list its tools with
  `nori-sessions integrations mcp tools --name HANDLE`.
</required>

<system-reminder> A connected server is distributed to newly provisioned sessions, not the one you are running in. It reaches active sessions only after the fleet reboots or cycles, so tell the user the tools will not appear mid-session. </system-reminder>

<system-reminder> Connections are org-wide by default. When the org has access control on, `connect`, `update`, `delete`, `reauth`, and `tools` also take `--scope personal` (the requesting person's own connection) or `--scope agent --agent HANDLE` (one custom agent's); `delete --scope personal --owner EMAIL` lets an admin remove someone else's. `mcp list --all-scopes` adds agent rows, plus personal rows only to their owner or a signed-in admin (so not to an agent in a session). From a session, personal and agent scope only work while an org admin has approved this session's `!admin` request: ask the user to reply `!admin`, end your turn, and after approval re-source `$HOME/.nori/env.d/broker-auth.sh` before retrying. The change is made and audited as the person the session works for. </system-reminder>

<system-reminder> Manage a server later with `nori-sessions integrations mcp update --name HANDLE ...` (integration mode, env var name, disabled tools) and `nori-sessions integrations mcp delete --name HANDLE`. Reconnect an expired credential in place with `nori-sessions integrations mcp reauth --name HANDLE` rather than deleting and re-adding it — add `--bearer-token TOKEN` for a static-token server, or for an OAuth server post the fresh authUrl it returns just like connect. </system-reminder>
