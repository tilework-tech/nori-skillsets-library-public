---
name: making-github-prs-user-attributable
description: Use when opening a GitHub pull request or acting on GitHub for someone, or when someone asks how to make the PRs, commits, or other GitHub work Nori does for them count as theirs instead of the Nori GitHub App bot's.
---

<required>
- Before any `gh` command that writes (PRs, comments, reviews), re-read the GitHub env so a connection added or removed during this session is reflected:
  `unset GH_TOKEN NORI_GITHUB_USER_LOGIN NORI_USER_GITHUB_TOKEN; for f in github-user custom; do source "$HOME/.nori/env.d/$f.sh" 2>/dev/null || true; done`
- If `GH_TOKEN` is now set, the session's person connected their GitHub account. Plain `gh` commands act as `$NORI_GITHUB_USER_LOGIN` with the Nori app badge. Open PRs with every value passed, so `gh` never prompts, pushes, or forks:
  `gh pr create --head "$BRANCH" --base "$BASE" --title "$TITLE" --body-file "$BODY_FILE"`
- Otherwise, if `NORI_USER_GITHUB_TOKEN` is set, use it for the PR only: check it with `GH_TOKEN="$NORI_USER_GITHUB_TOKEN" gh api -i user`, then run `GH_TOKEN="$NORI_USER_GITHUB_TOKEN" gh pr create ...`. Never export it or use it for anything but `gh pr create`.
- If a `gh` call fails with `401`, `403`, `404`, or "Resource not accessible", run `unset GH_TOKEN` and retry once with the app token. Tell the user what happened and that the result is bot-authored.
- With neither set, act with the app token. When a person is reading, run `nori-sessions integrations github-user status` once:
  - `available` and not `connected`: share its `connectUrl` so they can connect their GitHub account.
  - `needsReconnect`: say GitHub stopped accepting their connection and share `connectUrl`.
  - Not `available`: say an org admin can turn on GitHub attribution, or offer the personal token fallback below.
  Do not mention attribution in automated runs with no reader.
- Never print, log, or copy `GH_TOKEN` or `NORI_USER_GITHUB_TOKEN`. Never put either in a git remote, `~/.git-credentials`, the git credential helper, or the org setup script. Publish commits the usual way (`nori-git commit` or `nori-git publish`); it picks the connected account up itself.
</required>

# Whose GitHub account a session uses

- The person who started the session: the first person to prompt on the web, Slack, or Discord, or the author of a personal automation.
- In a shared Slack thread, that person acts for everyone in it. If someone else asked for the work, say whose account it ran as.
- Shared automations and project runs act as the Nori app.
- Commits: with a connected account, `nori-git` publishes a single new commit as that person, signed by GitHub. Longer or more complex histories, and sessions without a connected account, are published as the Nori app, with the person kept as a `Co-authored-by:` trailer that GitHub credits when the email is verified on their account.

# GitHub attribution (connected accounts)

- Availability: the org needs Nori's `github-user-attribution` flag, and an org admin turns it on in Security settings → GitHub attribution, or with `nori-sessions fleet set-setup --github-user-attribution true`. Only admins can change it.
- Connecting: the person opens `connectUrl` from `nori-sessions integrations github-user status` (the dashboard's Integrations → GitHub card) in a browser signed in to Nori and approves the GitHub consent screen. Their GitHub account must be able to reach the org's GitHub App installation; otherwise the connect is refused and nothing is stored.
- The connection reaches sessions they start within moments. A shell opened earlier must re-read the env as above.
- What it can do: whatever both the person and the Nori app may do on GitHub, on every repository the app is installed on that the person can reach. GitHub shows their avatar with the app badge.
- Disconnecting: the same Integrations card. It revokes the token on GitHub.
- An agent can read the status but cannot connect or disconnect for someone.

# Personal token fallback

Use this only where GitHub attribution is not available. It covers PR authorship only.

1. Check that the org supports personal variables. If a personal write fails with `scope must be 'org'`, personal variables are off for this org. Say so and stop. Never store one person's token org-wide, because every PR in the org would then be authored as them.
2. Have the person create a fine-grained personal access token at https://github.com/settings/personal-access-tokens/new:
   - Resource owner: the GitHub organization that owns the repositories.
   - Repository access: the repositories they want attributed, or all repositories.
   - Permissions: Pull requests read and write. Metadata read is added automatically. Add Contents read only if `gh pr create` reports it missing. Do not grant Contents write.
   - Expiration: the longest the organization allows. When the organization requires approval, the token can only read public resources until an owner approves it.
3. Have them store it under the name `NORI_USER_GITHUB_TOKEN`, using one of these routes:
   - Dashboard, preferred: Integrations → Custom environment variables → Manage, scope Personal. Give them the resolved `$NORI_SESSIONS_URL/integrations#integration-custom` link. This needs no `!admin` and the token never passes through chat.
   - From this session: the person replies `!admin`. After approval, run `source "$HOME/.nori/env.d/broker-auth.sh"`. Collect the token with `{{skills_dir}}/receiving-secrets-from-chat/SKILL.md`, then run `nori-sessions integrations set-custom --key NORI_USER_GITHUB_TOKEN --value-file "$TOKEN_FILE" --scope personal` and delete the file.
     If that skill is not installed, use the dashboard route.
   - Never ask them to paste the token into chat or pass it with `--value`.
4. Verify with `GH_TOKEN="$NORI_USER_GITHUB_TOKEN" gh api -i user`. Report the GitHub login and the `github-authentication-token-expiration` header, never the token. Warn when it expires within 7 days.
5. To remove it, use the dashboard or `nori-sessions integrations delete-custom --key NORI_USER_GITHUB_TOKEN --scope personal`.

# Approaches that do not work

- The org setup script. It runs before a machine is assigned to anyone, so it cannot see who started the session, and every session in the org shares it. Do not put tokens, a `gh` wrapper, or `GH_TOKEN` exports there.
- A custom variable named `GH_TOKEN`. It is reserved because `gh` would use it for every command in the session.
- An org-wide `github-pat` integration. It replaces the app token for all git and `gh` use across the org.
