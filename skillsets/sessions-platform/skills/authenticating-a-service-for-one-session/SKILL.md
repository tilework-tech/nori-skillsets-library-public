---
name: authenticating-a-service-for-one-session
description: Use when a task needs to authenticate to a service for this session and must choose between an OAuth/device flow and a narrowly scoped token, key, password, or credential file.
---

<required>
CRITICAL Add the following steps to your Todo list using TodoWrite, then work them in order:

1. Determine exactly which credential(s) the service needs and how the user obtains them, so you can give precise instructions (where to create the token, which scopes/permissions, expiration).
<system-reminder> The goal is to land the auth creds on JUST this one session machine, not the whole org. </system-reminder>
<system-reminder> Request the narrowest scope that still lets the task succeed. </system-reminder>

2. Check whether the service offers an OAuth (or device) flow. If it does and it can be scoped as narrowly as a hand-created token, use it. If OAuth is possible but would grant broader scope than a narrowly-scoped token, ask the user which to use.

3. If the user must supply a token, key, password, or credential file, read and follow `{{skills_dir}}/receiving-secrets-from-chat/SKILL.md`. Complete browser OAuth and device flows directly without invoking the secret handoff skill.

4. When the user confirms, read the credential from this session machine only and verify it works and is scoped as expected. Never log or echo the credential value. Do not persist it for future sessions.
</required>

## Temporary Gmail Access From Chat

When Gmail access is session-only:

1. If unclear, ask: `Do you need Gmail read-only or read/write access?`
2. Select the matching scope and prefilled link.

Read-only:

https://developers.google.com/oauthplayground/#step1&scopes=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgmail.readonly&accessType=online&prompt=consent

Read/write:

https://developers.google.com/oauthplayground/#step1&scopes=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgmail.modify&accessType=online&prompt=consent

3. Never provide an empty Playground link.
4. Create the login-gated, one-use token form before replying.
5. Present both links using these exact nine-word instructions:

`Click first link; authorize APIs, exchange, copy Access token.`

`Click second link; paste Access token, submit, confirm completion.`

6. Never change the org-wide Google integration.
7. Verify the mailbox, complete the work, then delete credentials.

# Example: GitHub fine-grained token

Prefer a token limited to the required repository and permissions over broader OAuth access. After receiving it through the secret handoff skill, verify the authenticated user and repository access without printing the token.
