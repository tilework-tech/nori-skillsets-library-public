---
name: configuring-github
description: Use when installing, verifying, or troubleshooting the Jiro (by Nori) GitHub app - including pushes rejected for a missing `workflows` permission and GitHub access that stopped working because the app was uninstalled on GitHub.
---

<required>
CRITICAL Add the following steps to your Todo list using TodoWrite:

- Check `nori-sessions onboarding status`: `.github.installAvailable` is `true` when an org admin can install the app here. If `.github.managedByOrg` is set, that parent org's admins manage the install instead.
- Have an org admin install the app: either from the dashboard's Integrations page (GitHub card, **Install GitHub App**), or with a link from `nori-sessions integrations github add-url` (the `url` field). Only an org admin's session can create the link, and only an org admin should open it. The link works once and expires after 10 minutes, so create it right before handing it over and create a new one if it expires or was already used. There is no token to paste back — GitHub's install page handles everything.
- Verify by running `nori-sessions onboarding status`. The `.github` object should show `installed: true, configured: true`.
</required>

<system-reminder> Repository access is managed by the GitHub App installation settings, not a Nori allowlist. If `.github.missingWorkspaceRepos` is present in the status output, the user must add those repos to the app installation before provisioning sessions that need them. </system-reminder>

# Editing GitHub Actions workflow files

A push that creates or changes anything under `.github/workflows/` fails with:

```
refusing to allow a GitHub App to create or update workflow `.github/workflows/<file>` without `workflows` permission
```

`nori-git publish` reports the same refusal as ``GitHub refused .github/workflows/<file>: this token lacks the `workflows` permission``. Before a plain `git push` of such a change, the pre-push hook warns ``nori-git: this push changes .github/workflows/<file>, which needs the `workflows` permission``; the push still runs, and GitHub decides.

This is deliberate, not a broken install. A pushed workflow runs with the repository's secrets, so only admin sessions (started by an admin or approved with `!admin`) can get the `workflows` permission. Reinstalling the app or editing its permissions on GitHub does not change this.

To push the change:

1. **Allow admin sessions to edit GitHub Actions workflows** must be on in Settings › Security on the Nori dashboard. It is on by default for organizations created after the setting was added; older organizations have it off until an org admin turns it on. Without this setting, admin escalation does not add the permission.
2. The user replies `!admin` in the thread and an admin approves the request. You cannot trigger this yourself; ask and end your turn.
3. Approval re-issues this session's git token with the elevated permissions, but an already-running shell may still hold the old one. Run `source "$HOME/.nori/env.d/github.sh"`, then retry the push.

If GitHub still refuses after `!admin` approval, the org's GitHub App installation has not accepted the `workflows` permission. A GitHub organization owner must accept the app's updated permissions on GitHub.

The elevation is temporary. If the user prefers not to elevate, push the rest of the change, and give them the workflow file diff to commit themselves.

# GitHub access stopped working

If git operations that previously worked start failing with authentication errors or `Repository not found`, the GitHub App may have been uninstalled or suspended on GitHub's side. Run `nori-sessions onboarding status` and check `.github.installationProblem`:

- `uninstalled` — the app was removed on GitHub. Have the user open the dashboard's Integrations page and click **Reinstall GitHub App**, or give an org admin a fresh one-use link from `nori-sessions integrations github add-url`. If `.github.managedByOrg` is set, that parent org's admins must reinstall it instead.
- `suspended` — a GitHub organization owner must unsuspend the installation on GitHub.
- absent — Nori checks the installation periodically and whenever the Integrations page opens. If the user confirms they removed the app, ask them to open the Integrations page, then check the status again.

Do not send the user to an **Update repository access** link for an uninstalled app; it points at the deleted installation and returns a 404 on GitHub. Verify the fix with `nori-sessions onboarding status` as above.

A GitHub personal access token configured as an integration keeps git working in the meantime, but it does not repair the app installation.
