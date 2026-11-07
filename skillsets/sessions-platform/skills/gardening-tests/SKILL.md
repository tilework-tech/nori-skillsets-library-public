---
name: gardening-tests
description: Use when Nori's weekly test gardening run asks you to add a regression test for recently changed code that no test covers, fix a flaky test, or remove a test that no longer tests anything, in the organization's repositories, and propose one focused change.
---

# Gardening Tests

No one is watching this run. Nori started it on a schedule. The request that
started it ends with this organization's settings: which repositories to work
in, whether the team has agreed to pull requests from you yet, and whether your
final reply goes to a Slack channel. Those settings override anything below.

Make the test suite a little more trustworthy each week with one focused
change. Try these in order of preference:

1. Add one regression test for recently changed code that no test covers.
2. Fix one test that the repository's own CI shows to be flaky.
3. Remove one test that no longer tests anything.

A week with nothing worth changing is a good outcome. If nothing is worth
changing, say nothing. Never invent work.

<required>
Add these to your TODO list:

1. Pick the repositories, tidy up your stale pull requests, and skip any with your previous change still open (section 1).
2. Check the repository's tests run, and record the baseline (section 2).
3. Look for candidates in order: missing tests, flaky tests, dead tests (section 3).
4. Prove the change with the evidence its kind needs (section 4).
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
  --jq '.[] | select(.headRefName | startswith("tests-gardening/"))'
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
  most one open test pull request from you per repository.

Work from a fresh copy of each repository's default branch. Never work from
the checkout's current branch or uncommitted changes:

```bash
git -C <repo> fetch origin
git -C <repo> worktree add "$(mktemp -d)/<repo>" origin/<default branch>
```

When you are done, remove the worktree
(`git -C <repo> worktree remove <path>`).

## 2. Baseline

Find how the repository runs its tests. Check its docs, `AGENTS.md`, package
scripts, `justfile` or `Makefile`, and CI config. Use those commands. Some
repositories run test files one at a time. Running many files in one process
can fail for reasons that have nothing to do with the code. Run the tests for
the files you will look at. Retry a failure once, and note the result. If the
tests do not run on this machine, skip that repository and say why in your
reply. Never run tests that need production or shared systems.

## 3. Find candidates, in order

Stop at the first kind that gives you a candidate worth sending.

**Missing tests.** Look at code changed in the last two weeks
(`git log --since='2 weeks ago' --stat`). Start with commits that changed
code but no tests. Find a behavior in it that no test
exercises: a branch, an error path, or an edge case a caller depends on. If
the repository has a coverage tool, use it. Otherwise, read the tests for that
code. Treat line coverage only as a hint. A line can run in some other test
without anything checking what it does. Skip trivial code such as getters,
constants, and pure wiring.

**Flaky tests.** Look at the repository's recent CI runs for a test that
failed and then passed on the same commit, either in two runs for the same
`headSha` or in a run that was retried (`attempt` above 1; earlier attempts
are in `gh run view <id> --attempt <n>`):

```bash
gh run list --repo <owner/name> --limit 50 --json databaseId,attempt,conclusion,headSha,name
```

Before changing anything, find the cause (timing, ordering, shared state,
real clocks, network). Do not use a retry or a longer timeout as the fix.

**Dead tests.** A test that no longer tests anything: it has no assertions,
it is always skipped, it exercises code that no longer exists, or it repeats
another test exactly. A test that is merely slow, old, or failing is not dead.
Never remove a failing test. It is the team's signal.

For each candidate, write down the file, the behavior or test, and the
evidence: the commit, the coverage gap, the CI runs, or the matching test. No
evidence, no candidate.

## 4. Prove it

- **A new test** must build, pass five runs in a row, and fail when you
  break the behavior it covers on purpose. Break it in a scratch copy of the
  repository (for example a second `git worktree`), never in the copy you
  will commit from. The test must check one behavior, through the code's
  public interface, with real assertions. Do not test mocks. Do not write
  tests that only restate the implementation.
- **A flaky-test fix** must pass at least twenty runs in a row locally, and
  you must be able to say what made it flaky. If you cannot reproduce or
  explain the flakiness, propose nothing.
- **A dead-test removal** must show why the test cannot fail, or which test
  it repeats, and the suite must still pass without it with coverage no lower.

If the proof fails, drop the candidate. Go back to section 3.

## 5. Change or propose

If the settings say to open pull requests:

1. Branch from the default branch: `tests-gardening/<short-topic>`. Section 1
   relies on that prefix.
2. Change only tests, and test helpers or fixtures the change needs. Never
   change the code under test.
3. Follow the repository's test conventions: file location, naming,
   framework, and style.
4. Commit, push, and open a pull request (not a draft) with no reviewers. In
   the description, state what was missing, flaky, or dead, the evidence, and
   the proof from section 4. Never merge, and never push to the default branch.

If the settings say the team has not agreed to pull requests yet, change
nothing in the repository. Your reply is the proposal: what is missing,
flaky, or dead, the evidence, and the exact change you would make. Someone may
answer "yes" in the thread your reply starts. If so, make the change as above
and reply with the pull request link.

Do not repeat a proposal. If you can read the channel's recent history
(`nori-slack conversations.history --channel <channel id> --limit 50`), skip
any proposal you made there in the last four weeks that nobody said yes to.
Pick the next candidate instead.

## 6. Reply

The team sees your final reply. Write it as a colleague's short update, not
a report:

- One or two sentences on what was missing, flaky, or dead and why it
  matters.
- The evidence and proof in a line.
- The pull request link, or the exact change you would make and a question
  asking whether to open it. If the test is short, show it in a code block.
  If it is longer, describe what it sets up and asserts in two or three lines
  instead.

<good-example>
`retryUpload` in `web/src/upload.ts` gained a give-up path last week (#388), but nothing tests that it stops after three attempts, so a regression there would retry forever.

PR adding one test; it passes 5/5 and fails if the attempt limit is removed: https://github.com/acme/web/pull/402
</good-example>

<bad-example>
## Weekly Test Health Report
Coverage is 71.3%. I found 14 areas that could use more tests! ...
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
- Change tests only. If a test shows the code is wrong, say so in your reply
  instead of changing the code or the test to match it.
- Never remove or skip a failing test to make the suite pass.
- Never copy secrets, tokens, or customer data into tests, commits, or
  replies.
- Do not create, edit, or delete automations, projects, or project docs.
