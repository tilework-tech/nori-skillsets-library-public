---
name: receiving-secrets-from-chat
description: Use when a user needs to provide this session with an API key, access token, password, private key, cookie, credential file, or other secret through Slack, Discord, web chat, or another non-terminal conversation. Never ask them to paste or upload a secret into chat.
---

<required>
CRITICAL Add the following steps to your Todo list, then work them in order:

1. Determine the exact text values or files to receive and where the current session will read them.

2. Create a private temporary directory with `mktemp -d`, set `umask 077`, and serve a small form on a session port. Accept only the required fields or files, write them atomically without replacing an existing file, and use mode `0600`. Accept exactly one successful submission, stop accepting requests immediately afterward, and never log, echo, or place secret values in command arguments.

3. Resolve the public session port URL and verify its login gate before sharing it. An unauthenticated curl must redirect to `/auth/login`.

4. Give the user the resolved URL with its trailing slash, explain which fields or files to submit, ask them to reply when finished, and end the turn.
<system-reminder> Do not poll. The user cannot see the link until the turn ends. </system-reminder>

5. After the user confirms, verify the submission using metadata only and use the secret from its file. Delete the temporary directory when the task is complete.
<system-reminder> Never send the secret through chat. Keep it on this session machine only, and do not persist it unless the user explicitly requests a separate secure persistence workflow. </system-reminder>

6. Ask the user if they want to persist the secret as an env variable or part of the session setup script.
</required>

<system-note> This skill only transfers secrets. The calling workflow decides which credential to request, its scope and expiration, and how to verify it. </system-note>
