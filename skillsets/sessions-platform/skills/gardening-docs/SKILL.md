---
name: gardening-docs
description: Use when Nori's weekly docs gardening run asks you to find documentation that no longer matches the code, or is missing where people need it, in the organization's repositories and propose one focused fix.
---

# Gardening Docs

No one is watching this run. Nori started it on a schedule. The request that
started it ends with this organization's settings: which repositories to work
in, whether the team has agreed to pull requests from you yet, and whether your
final reply goes to a Slack channel. Those settings override anything below.

Find the one documentation problem most worth fixing this week. Fix it in a
pull request or propose the fix, as the settings allow. A week with nothing
worth fixing is a good outcome. If nothing is worth fixing, say nothing. Never
invent work.

<required>
Add these to your TODO list:

1. Pick the repositories, tidy up your stale pull requests, and skip any with your previous fix still open (section 1).
2. Find stale or missing docs, with evidence (section 2).
3. Choose at most one fix (section 3).
4. Make the fix or write the proposal, as the settings allow (section 4).
5. Finish with one reply, or `<no-response/>` (section 5).
</required>

## 1. Repositories

Work in the repositories the settings name. "Every repository in the
workspace" means the repositories cloned under `~/org/workspace`. A named
repository is the folder of that name (or the last part of `owner/name`)
there. If a repository is not cloned, skip it. If you post a reply, mention
the skipped repository.

Before anything else, check each repository for your own open docs pull
request from an earlier week:

```bash
gh pr list --repo <owner/name> --state open --json number,headRefName,updatedAt,author,url \
  --jq '.[] | select(.headRefName | startswith("docs-gardening/"))'
```

- If you opened one and it has had no activity for three weeks (`updatedAt`),
  close it and delete its branch. Add a one-line comment saying nobody picked
  it up and it can be reopened:
  `gh pr close <number> --repo <owner/name> --delete-branch --comment '...'`.
  You opened it if its author is your own account
  (`gh api user --jq .login`). If that command fails because you are signed
  in as an app, you opened it if its author is a bot (`author.is_bot`). Never
  close anyone else's pull request.
- If one is still open after that, skip that repository this week. Keep at
  most one open docs pull request from you per repository.

## 2. Find what is stale or missing

Look in the places where wrong docs cost people time:

- The README, `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, and per-folder docs
  near code that changed recently (`git log --since='2 weeks ago' --stat`).
- Setup, build, and test instructions. Run them on this machine when they
  are local and safe to repeat. Never run deploy, release, or migration
  instructions, or anything that touches shared or production systems. Check
  those only against the scripts, CI config, and manifests.
- Paths, commands, environment variables, flags, and links the docs name.
  Check each one still exists.
- Folders with real complexity and no doc at all, where a short doc would
  save the next person an hour.

For each candidate, write down the exact claim, where it is, and the evidence
that it is wrong or missing: the file, command output, or commit. If you have
no evidence, drop the candidate. Do not rewrite docs for style, tone, or length.

## 3. Choose at most one fix

Rank candidates by how likely they are to mislead someone soon: setup and
build instructions first, then architecture and folder docs, then everything
else. Pick the top one, or a tightly connected set in one repository (for
example, a renamed command used in three docs). If nothing clears the bar,
stop.

## 4. Fix or propose

If the settings say to open pull requests:

1. Branch from the default branch: `docs-gardening/<short-topic>`. Section 1
   relies on that prefix.
2. Make the smallest edit that makes the docs true. Keep the existing voice
   and structure.
3. If the repository has its own docs checks or link checks, run them.
4. Commit with a `docs:` message, push, and open a pull request (not a
   draft) with no reviewers. In the description, state what was wrong, the evidence, and
   what changed. Never merge, and never push to the default branch.

If the settings say the team has not agreed to pull requests yet, change
nothing in the repository. Your reply is the proposal: what is wrong, the
evidence, and the exact change you would make. Someone may answer "yes" in
the thread your reply starts. If so, make the fix as above and reply with the
pull request link.

Do not repeat a proposal. If you can read the channel's recent history
(`nori-slack conversations.history --channel <channel id> --limit 50`), skip
any proposal you made there in the last four weeks that nobody said yes to.
Pick the next candidate instead.

## 5. Reply

The team sees your final reply. Write it as a colleague's short update, not
a report:

- One or two sentences on what was wrong and why it matters.
- The evidence in a line.
- The pull request link, or the exact change you would make and a
  question asking whether to open it.

<good-example>
The setup steps in `api/README.md` still say `make bootstrap`, but that target was removed in #412 and new machines now use `just setup`. Anyone following the README hits an error on step two.

PR fixing the three places it appears: https://github.com/acme/api/pull/431
</good-example>

<bad-example>
## Weekly Documentation Report
I reviewed 14 files across 3 repositories. Overall documentation health is good! ...
</bad-example>

If nothing cleared the bar, or you skipped every repository, reply with only
`<no-response/>`. Then nothing is posted.

Exception: on your first run, right after the team switched you on, the
request says so. On that run, post a sentence or two on what you checked
instead.

## Safety

- Never merge, approve, or push to a default branch. Open pull requests with
  no reviewers.
- At most one pull request per run.
- Change documentation only. If a doc is wrong because the code is wrong, say
  so in your reply instead of changing code.
- Never copy secrets, tokens, or customer data into docs, commits, or replies.
- Do not create, edit, or delete automations, projects, or project context.
