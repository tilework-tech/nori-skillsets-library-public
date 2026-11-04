---
name: gardening-utils
description: Use when Nori's weekly utils gardening run asks you to find code that rewrites a helper the repository already has and propose switching a few call sites to that helper without changing behavior.
---

# Gardening Utils

No one is watching this run. Nori started it on a schedule. The request that
started it ends with this organization's settings: which repositories to work
in, whether the team has agreed to pull requests from you yet, and whether your
final reply goes to a Slack channel. Those settings override anything below.

Find one place where code re-implements a helper the repository already has.
Switch a handful of call sites to that helper with no change in behavior. Keep
the change small and boring. A reviewer should be able to approve it in two
minutes. A week with nothing worth changing is a good outcome. If nothing is
worth changing, say nothing. Never invent work.

<required>
Add these to your TODO list:

1. Pick the repositories, tidy up your stale pull requests, and skip any with your previous change still open (section 1).
2. Find re-implemented helpers, with evidence (section 2).
3. Choose at most one helper and a few call sites (section 3).
4. Prove the behavior is identical (section 4).
5. Make the change or write the proposal, as the settings allow (section 5).
6. Finish with one reply, or `<no-response/>` (section 6).
</required>

## 1. Repositories

Work in the repositories the settings name. "Every repository in the
workspace" means the repositories cloned under `~/org/workspace`. A named
repository is the folder of that name (or the last part of `owner/name`)
there. If a repository is not cloned, skip it. If you post a reply, mention
the skipped repository.

Before anything else, check each repository for your own open pull requests
from earlier weeks:

```bash
gh pr list --repo <owner/name> --state open --json number,headRefName,updatedAt,author,url \
  --jq '.[] | select(.headRefName | startswith("utils-gardening/"))'
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
  most one open utils pull request from you per repository.

Work from a fresh copy of each repository's default branch. Never work from
the checkout's current branch or uncommitted changes:

```bash
git -C <repo> fetch origin
git -C <repo> worktree add "$(mktemp -d)/<repo>" origin/<default branch>
```

When you are done, remove the worktree
(`git -C <repo> worktree remove <path>`).

## 2. Find re-implemented helpers

Start from the helpers the repository already has: shared `utils`, `lib`,
`helpers`, `common`, or standard-library folders, and functions the
repository's own docs or `AGENTS.md` tell people to use. Read each helper and
its tests until you know exactly what it does.

Then look for code that does the same thing by hand: the same few lines
repeated, an inline version of the helper's logic, or a local copy of the
helper. Start with code that changed recently (`git log --since='4 weeks ago'
--stat`). New copies appear there.

For each candidate, write down the helper, every call site you would change,
and why the hand-written code is the same thing. If you have no evidence, drop
the candidate.

The switch must be worth a reviewer's time. It must remove real repeated logic
or a copy that could drift from the helper. Swapping one idiom for another
equivalent one line is not enough.

Do not create a new helper, change a helper's behavior or signature, rename,
move files, or reformat. Do not touch generated, vendored, or migration code.

## 3. Choose at most one helper

Pick one helper and the call sites where the hand-written code is plainly the
same. Keep it small: usually two to five call sites, in one repository. If
you are not sure about a call site, leave it out. If nothing clears the bar,
stop.

## 4. Prove the behavior is identical

For each call site, compare the hand-written code and the helper on every
input the call site can see, including empty, missing or null values, errors,
ordering, and side effects such as logging or mutation. If any of these
differ, drop that call site.

Before changing anything, run the repository's build, type check, lint, and
the tests that cover the affected files, and note the results. Use the
repository's own commands (package scripts, `justfile`, CI config). They may
run test files one at a time. Running many files in one process can fail for
reasons that have nothing to do with the code. Retry a failure once. If they
still fail, stop work on that repository. Never send a change you cannot
verify.

## 5. Change or propose

If the settings say to open pull requests:

1. Branch from the default branch: `utils-gardening/<helper-name>`. Section 1
   relies on that prefix.
2. Change only the chosen call sites. No unrelated edits.
3. Run the same checks as in section 4. All of them must pass. If any fail,
   drop the change and stop.
4. Commit, push, and open a pull request (not a draft) with no reviewers. In the
   description, name the helper, list the call sites, explain why each is the
   same behavior, and show the checks you ran before and after. Never
   merge, and never push to the default branch.

If the settings say the team has not agreed to pull requests yet, change
nothing in the repository. Your reply is the proposal: the helper, the call
sites, why the behavior is the same, and the exact change you would make.
Someone may answer "yes" in the thread your reply starts. If so, make the
change as above and reply with the pull request link.

Do not repeat a proposal. If you can read the channel's recent history
(`nori-slack conversations.history --channel <channel id> --limit 50`), skip
any proposal you made there in the last four weeks that nobody said yes to.
Pick the next candidate instead.

## 6. Reply

The team sees your final reply. Write it as a colleague's short update, not
a report:

- One or two sentences on what was duplicated and why switching helps.
- The evidence in a line.
- The pull request link, or the exact change you would make and a question
  asking whether to open it.

<good-example>
Three handlers in `api/routes/` parse the `?limit=` query by hand, and two of them let `limit=0` through. `parsePageLimit` in `api/lib/paging.ts` already handles that and is used everywhere else.

PR switching the three handlers over, with build and tests green before and after: https://github.com/acme/api/pull/512
</good-example>

<bad-example>
## Weekly Code Quality Report
I scanned 1,240 files and found 37 opportunities for refactoring! ...
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
- Never change behavior. If the hand-written code and the helper differ, or
  the helper itself looks wrong, and it looks like a bug, say so in your
  reply instead of changing it.
- Never copy secrets, tokens, or customer data into code, commits, or replies.
- Do not create, edit, or delete automations, projects, or project context.
