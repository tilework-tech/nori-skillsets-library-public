---
name: configuring-github
description: Use when installing, verifying, or troubleshooting the Nori GitHub app - including pushes rejected for a missing `workflows` permission and GitHub access that stopped working because the app was uninstalled on GitHub.
---

<required>
CRITICAL Add the following steps to your Todo list using TodoWrite:

- Get the install URL from `nori-sessions onboarding status` (the `.github.installUrl` field) and have the user open it in their browser to authorize the app for their repos. There is no token to paste back — the OAuth flow handles everything.
- Verify by running `nori-sessions onboarding status`. The `.github` object should show `installed: true, configured: true`.
</required>

<system-reminder> Repository access is managed by the GitHub App installation settings, not a Nori allowlist. If `.github.missingWorkspaceRepos` is present in the status output, the user must add those repos to the app installation before provisioning sessions that need them. </system-reminder>

# Editing GitHub Actions workflow files

A push that creates or changes anything under `.github/workflows/` fails with:

```
refusing to allow a GitHub App to create or update workflow `.github/workflows/<file>` without `workflows` permission
```

This is deliberate, not a broken install. A pushed workflow runs with the repository's secrets, so session git tokens never include the `workflows` permission by default. Reinstalling the app or editing its permissions on GitHub does not change this.

To push the change:

1. An org admin turns on **Allow admin sessions to administer GitHub repositories and the organization** on the Security page of the Nori dashboard. Without this setting, admin escalation does not add the permission.
2. The user replies `!admin` in the thread and an admin approves the request. You cannot trigger this yourself; ask and end your turn.
3. Approval re-issues this session's git token with the elevated permissions, but an already-running shell may still hold the old one. Run `source "$HOME/.nori/env.d/github.sh"`, then retry the push.

The elevation is temporary. If the user prefers not to elevate, push the rest of the change, and give them the workflow file diff to commit themselves.

# GitHub access stopped working

If git operations that previously worked start failing with authentication errors or `Repository not found`, the GitHub App may have been uninstalled or suspended on GitHub's side. Run `nori-sessions onboarding status` and check `.github.installationProblem`:

- `uninstalled` — the app was removed on GitHub. Have the user open the dashboard's Integrations page and click **Reinstall GitHub App** (the same link is `.github.installUrl`). If `.github.managedByOrg` is set, that parent org's admins must reinstall it instead.
- `suspended` — a GitHub organization owner must unsuspend the installation on GitHub.
- absent — Nori checks the installation periodically and whenever the Integrations page opens. If the user confirms they removed the app, ask them to open the Integrations page, then check the status again.

Do not send the user to an **Update repository access** link for an uninstalled app; it points at the deleted installation and returns a 404 on GitHub. Verify the fix with `nori-sessions onboarding status` as above.

A GitHub personal access token configured as an integration keeps git working in the meantime, but it does not repair the app installation.
