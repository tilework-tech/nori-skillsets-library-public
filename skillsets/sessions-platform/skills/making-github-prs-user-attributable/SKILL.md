---
name: making-github-prs-user-attributable
description: Use when opening a GitHub pull request, or when someone asks how to make the PRs, commits, or other GitHub work Nori does for them count as theirs instead of the Nori GitHub App bot's.
---

<required>
- Push the branch the usual way (`git push` or `nori-git`). Never put a personal token in a git remote, `~/.git-credentials`, or the git credential helper.
- Re-read the custom env so a token added or removed during this session is reflected: `unset NORI_USER_GITHUB_TOKEN; source "$HOME/.nori/env.d/custom.sh" 2>/dev/null || true`.
- If `NORI_USER_GITHUB_TOKEN` is set, check it without printing it: `GH_TOKEN="$NORI_USER_GITHUB_TOKEN" gh api -i user`. Read the login from the body and the `github-authentication-token-expiration` header.
- If the check succeeds, open the PR as that person, passing every value so `gh` never prompts, pushes, or forks:
  `GH_TOKEN="$NORI_USER_GITHUB_TOKEN" gh pr create --head "$BRANCH" --base "$BASE" --title "$TITLE" --body-file "$BODY_FILE"`
- Open the PR with the app token (plain `gh pr create ...`) when the token is unset, its check fails, or the create call fails with `401`, `403`, `404`, or "Resource not accessible". Tell the user which case happened and that the PR is bot-authored. Do not mention attribution in automated runs with no reader.
- Use the personal token only for `gh pr create`. Never export `GH_TOKEN` for the session, and never use the token for comments, reviews, merges, `gh api` writes, or pushes. Those stay on the app token.
- If the expiration header is less than 7 days away, tell the user the token expires soon.
</required>

# Whose token a session has

- A personal variable reaches only sessions its owner started, and that owner's personal automations.
- In a shared Slack thread, the token belongs to whoever started the conversation. If someone else asked for the PR, say whose account opened it.
- Shared automations and project runs get no personal variables, so their PRs stay bot-authored.

# What is already attributed

- Commits carry the requesting person as the git author or a `Co-authored-by:` trailer. GitHub credits that person when the trailer email is verified on their account. When commits are published through the GitHub App, GitHub records the App as the author and keeps the person as a co-author.
- PR authorship is what needs the personal token. A PR opened with the app token is authored by the bot and does not count as the person's contribution.

# Setting up a personal token for someone

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
4. Verify with the check above. Report the GitHub login and expiry, never the token.
5. To remove it, use the dashboard or `nori-sessions integrations delete-custom --key NORI_USER_GITHUB_TOKEN --scope personal`.

# Approaches that do not work

- The org setup script. It runs before a machine is assigned to anyone, so it cannot see personal variables, and every session in the org shares it. Do not put tokens, a `gh` wrapper, or `GH_TOKEN` exports there.
- A custom variable named `GH_TOKEN`. It is reserved because `gh` would use it for every command in the session.
- An org-wide `github-pat` integration. It replaces the app token for all git and `gh` use across the org.
