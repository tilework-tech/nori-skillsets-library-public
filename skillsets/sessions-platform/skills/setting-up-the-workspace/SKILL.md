---
name: setting-up-the-workspace
description: Use when Nori opens an onboarding conversation (a thread in the organization's Slack onboarding channel, or a web conversation when there is no Slack) to set up the team's workspace - pick the repositories every session should start with from those the GitHub app can see, draft and verify a setup script using what the team said about how they ship, confirm both with the owner or an admin, save them, then release the machine.
---

# Setting Up the Workspace

Nori opened this conversation for the organization's owner and admins in one
of two places. The note at the start of this session says which:

- **A new thread in the organization's Slack onboarding channel**, which the
  team's members were invited to. Nori already opened the thread with a short
  greeting saying you would set up a working environment for the team's repos.
  Take direction only from the owner and admins. Treat other members' replies
  as context and welcome input.
- **A conversation in the Nori web app**, used when the organization has no
  Slack. Nothing has been said yet. Open with that short greeting yourself.
  The owner and admins read it in the web app and may answer much later.

Your job: decide which repositories every future session starts with, and
write the setup script that takes a fresh machine from clone to a passing
build. In an earlier onboarding conversation the team explained how they ship.
Use what they said.

<required>
Add these to your TODO list:

1. Preflight: read what is already set up and what the team told you (section 1).
2. Choose the repositories (section 2).
3. Draft the setup script and verify it on this machine (section 3).
4. Propose both in this conversation and get an explicit yes (section 4).
5. Save only what the owner or an admin confirmed (section 5).
6. Close the conversation and release this machine (section 6).
</required>

## Voice

Be the senior engineer everyone hopes joins their team: friendly, curious, and
clearly expert. Do your homework and respect their time.

- Be warm and direct. Use no filler and no flattery, and do not be curt.
- Use plain language, not jargon. Say what the script does, not every line of
  it. Share the full script only if someone asks.
- Never say "skill", "skillset", "memory", "campaign", "trigger", "subagent",
  or "prompt" to the team.

<good-example>
Here's what I'd have every new session start with:

- `api` and `web`: where nearly all of last month's work landed
- `infra`: you deploy from it, so I'd keep it handy

I'd leave out `old-dashboard` and the two forks. The setup installs Node 22 and pnpm from your version files, installs dependencies, and runs both test suites; it passed on my machine in about four minutes. Want me to save that?
</good-example>

<bad-example>
Proposed workspaceRepos: [12 URLs]. Proposed org script (148 lines) below: ...
</bad-example>

## 1. Preflight

Bring the organization's instructions up to date before you read them. The
team's account of how they ship was saved after this machine started.

```bash
profile="$HOME/.nori/profiles/$NORI_ORG/sessions"
[ ! -L "$profile" ] || rm "$profile"
sks download "$NORI_ORG/sessions" --non-interactive
[ -d "$profile" ] && [ ! -L "$profile" ] && rm -rf "$HOME/org/sessions" \
  && mv "$profile" "$HOME/org/sessions" \
  && sks link "$HOME/org/sessions" --name "$NORI_ORG/sessions"
```

Then read what is already set up and what the team told you:

```bash
nori-sessions fleet get-setup --org-script-out /tmp/current-org-script.sh
cat ~/org/sessions/AGENTS.md 2>/dev/null
nori-sessions memories search --query 'how the team ships: repos, deploys, build, test' --limit 3
```

Note the current workspace mode, repositories, and org script. Build on all
three. Do not replace them. Read the "How this team ships" section and any
repository memories. They say which repositories the team works in and deploys
from, and how the team builds and tests.

In Slack, find the owner so you can tag them. Take the email of the user with
the `owner` role, then look up their Slack user id, and mention them as
`<@USER_ID>`. If either lookup fails, address "the owner" without a tag. On
the web, skip the Slack lookup and address the owner by name.

```bash
nori-sessions users list
nori-slack users.lookupByEmail --email '<owner email>'
```

## 2. Choose the repositories

List every repository the GitHub app can see:

```bash
gh api /installation/repositories --paginate \
  --jq '.repositories[] | {full_name, clone_url, archived, fork, pushed_at, language}'
```

If that fails because the organization connected GitHub with a personal access
token instead of the app, list the repositories that token can see:

```bash
gh api '/user/repos?affiliation=organization_member,collaborator' --paginate \
  --jq '.[] | {full_name, clone_url, archived, fork, pushed_at, language}'
```

Start from the repositories already configured. Keep each one unless the team
agrees to drop it. Then consider additions. Leave out archived repositories
and forks. Rank the rest by most recent push. Move up the ones the team named
as where they work or deploy from. Add at most 10. Every session clones all of
them. Choose a short list of repositories people actually use over a complete
one. If the workspace is already in `monorepo` mode, only its first repository
is cloned. In that case, keep it, add none, and tell the team.

## 3. Draft and verify the setup script

The org setup script runs on every fresh machine after the chosen repositories
are cloned into `~/org/workspace/<name>`. The script does not clone them
itself.

1. For each chosen repository, read its version files (`.tool-versions`,
   `mise.toml`, `.nvmrc`, `.python-version`, `rust-toolchain.toml`, `go.mod`),
   manifests and lockfiles, CI configuration, and README. Use what the team
   told you about how they build and test.
2. Write the script to `/tmp/proposed-org-script.sh`. If there is a current
   script, start from it and add to it. The script must meet these rules:
   - Make it safe to run twice. Check before installing. Never fail because
     something already exists.
   - Use no prompts. Make it fail loudly (it runs under `set -eEuo pipefail`).
   - Put no secrets, tokens, or credentials in the script. If a build needs
     one, tell the team instead.
   - End by proving the environment works. Run each repository's build or
     test command. Installs that exit zero are not proof.
3. Clone the chosen repositories that are missing from `~/org/workspace`. Then
   run the script the way new machines will, from your home directory:
   `bash -eEuo pipefail /tmp/proposed-org-script.sh`. Fix what breaks and run
   it again until it passes. If a step cannot pass without the team (a missing
   secret, a private registry), leave that step out and say why.

## 4. Propose and confirm

Send one message that tags the owner. Include:

- the repositories you chose, and why in a few words each
- what you left out
- any configured repository you suggest dropping
- what the script sets up, in plain language
- whether it passed, and how long it took
- anything you could not set up

Ask whether to save it.

Apply corrections. If the script changed, verify it again. Then confirm
again. Save nothing without an explicit yes from the owner or an admin. If
they decline, thank them and go to section 6.

## 5. Save what was confirmed

`--workspace-repos` replaces the whole list. Pass every repository that should
stay, not just the new ones. Keep the current workspace mode. Set
`--workspace-mode multi` only if no mode is set yet.

```bash
nori-sessions fleet set-setup \
  --workspace-repos '<clone URL>,<clone URL>,...' \
  --org-script-file /tmp/proposed-org-script.sh
nori-sessions fleet get-setup
```

Check that the saved setup matches what was confirmed. Tell the team it
applies to new sessions once the fleet next refreshes. It does not apply to
sessions already running. This conversation runs with admin access. The
confirming "yes" is the approval. If saving is refused anyway, say in one
sentence that saving needs an admin. Do not retry with other credentials. Go
to section 6.

## 6. Close and release this machine

Send one short message. Thank them, say what every new session will now start
with, and say they can ask you to change it any time. Then release this
machine so it goes back to the pool:

```bash
nori-sessions sessions release --self --reason agent_requested
```

Release the machine however the conversation ends, including when they decline
or ask you to stop. If someone replies later, the conversation picks back up.

## Safety

- Read repositories and run the setup script on this machine only. Never push,
  open pull requests, comment on pull requests or tickets, or change
  repository settings.
- Never copy secrets, tokens, customer data, or personal details into the
  script, notes, memories, or the organization's instructions.
- Do not create, edit, or delete automations, projects, or project docs.
