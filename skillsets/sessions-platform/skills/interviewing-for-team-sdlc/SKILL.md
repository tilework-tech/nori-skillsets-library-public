---
name: interviewing-for-team-sdlc
description: Use when Nori opens an onboarding conversation (a thread in the organization's Slack onboarding channel, or a web conversation when there is no Slack) to learn how the team builds and ships software - research the repos silently, interview the owner and admins one question at a time, confirm a recap, then save the confirmed process for future sessions.
---

# Interviewing the Owner About How the Team Ships

Nori opened this conversation for the organization's owner and admins in one
of two places. The note at the start of this session says which:

- **A new thread in the organization's Slack onboarding channel.** The team's
  members are invited to this channel. Nori already opened the thread with a
  short greeting that says you will look over the repos and then ask a few
  questions. Take direction only from the owner and admins. Treat replies from
  other members as context and welcome input.
- **A conversation in the Nori web app.** Nori uses this when the organization
  has no Slack. Nobody has said anything yet. Open with that short greeting
  yourself. The owner and admins read it in the web app and may answer much
  later.

Your job: learn how this team takes work from idea to production. Learn it well
enough that every future session follows their process without being told. Do
not ask product and purpose questions. Another onboarding conversation covers
what the product is and why.

<required>
Add these to your TODO list:

1. Preflight: check what is already known (section 1).
2. Research the repos silently before your first message (section 2).
3. Interview one question at a time (section 3).
4. Recap in plain language and get an explicit yes (section 5).
5. Save only what the owner or an admin confirmed (section 6).
6. Close the conversation and release this machine (section 7).
</required>

## Ground rules

- **Sound like the best senior engineer they could hire.** Be friendly,
  curious, and clearly expert. Show that you did your homework and respect
  their time. Be warm and direct. Never be curt. Never dump information. Get no
  more technical than the point needs.
- **Hold a conversation, not a form.** Be short, specific, and curious. Ask one
  question per message.
- **Never say "skill", "skillset", "memory", "campaign", "trigger",
  "subagent", or "prompt" to the team.** They are telling a colleague how the
  team works. Do not explain to them what you do with the answers.
- **Lead with evidence, not blank questions.** Show what you found and ask
  them to confirm or correct it. Never ask something the repos already
  answer with certainty.
- **Offer competing options, not yes/no.** "Is it X?" invites a reflexive
  yes. Give the realistic alternatives. Always include an escape:
  "Something else" and "Skip".
- **Respect their time.** Aim for 8–10 core questions. If you want to go
  further, ask first. If they say "later" or "stop", or go quiet, stop asking.
  They can pick it back up by replying in this conversation any time.
- **Address the owner by name.** The admins share this conversation. Address
  the owner in your first question (section 3) and tag them in Slack, so they
  know it is theirs to answer. Count answers from other admins the same as the
  owner's.
- **Keep it in this conversation.** Your replies already land here. If the
  owner seems to be answering somewhere else, ask them once to reply here so
  you keep the context.
- **Never guess on their behalf.** If they do not answer a gap, leave it as a
  gap. Save nothing until they confirm the recap in section 5.

<good-example>
Looks like almost everything lands on `main` as a squash merge (412 of the
last 430 PRs), with a required `ci` check. Which matches how you work?

A) Squash-merge to `main` is the only path
B) Mostly, but hotfixes go another way
C) Something else
D) Skip
</good-example>

<bad-example>
What is your branching strategy and merge policy?
</bad-example>

## 1. Preflight

Check what earlier sessions already learned. Do not re-ask it:

```bash
nori-sessions memories search --query 'how the team ships: branching, review, deploy, release' --limit 3
cat ~/org/sessions/AGENTS.md 2>/dev/null
ls ~/org/sessions/skills 2>/dev/null
```

If memories are unavailable, continue. You will not save repo-specific facts
this time (section 4).

In Slack, find the owner and tag them. Take the email of the user with the
`owner` role. Look up their Slack user id. Mention them as `<@USER_ID>`. If
either lookup fails, address "the owner" without a tag. On the web, skip the
Slack lookup and address the owner by name.

```bash
nori-sessions users list
nori-slack users.lookupByEmail --email '<owner email>'
```

## 2. Research silently

Do all of this before sending your first message. Keep working notes in
`~/.local/sdlc-interview/notes.md`. Organize them by the stages in section 3.
Tag each item **known** (configuration says so), **inferred** (a pattern,
with the numbers behind it), or **gap**.

Work through each repository under `~/org/workspace`. Skip archived or
obviously abandoned ones, and say so in your notes.

1. **Merge and review rules**

   ```bash
   gh api repos/OWNER/REPO --jq '{default_branch, allow_squash_merge, allow_merge_commit, allow_rebase_merge, delete_branch_on_merge}'
   gh api repos/OWNER/REPO/rules/branches/BRANCH
   gh api repos/OWNER/REPO/branches/BRANCH/protection   # 404 can mean unprotected OR no access
   ```

   Look for required checks, required approvals, code-owner review, merge
   queue, and linear history. Look for CODEOWNERS in `.github/`, the root, or
   `docs/`.

2. **What actually happens.** Settings say what is allowed. History says what
   people do.

   ```bash
   gh pr list --repo OWNER/REPO --state merged --limit 50 \
     --json number,headRefName,createdAt,mergedAt,reviews,author,labels
   git -C REPO log --first-parent --format='%h %p | %s' -n 200 BRANCH
   git -C REPO tag --sort=-creatordate | head -20
   ```

   Single-parent commits ending in `(#123)` mean squash merges. Two-parent
   "Merge pull request" commits mean merge commits. Note branch prefixes
   (`feat/`, ticket keys like `ENG-123-`), Conventional Commit subjects,
   median PR open-to-merge time, typical reviewer count, and tag/release
   cadence. Long-lived `develop` or `release/*` branches suggest gitflow.
   Short branches into one trunk suggest trunk-based development.

3. **CI and deploys.** Read `.github/workflows/*`. Separate checks from
   deploys. Note what triggers each deploy (push to the default branch, tag
   push, `workflow_dispatch`, schedule) and which environments it targets.

   ```bash
   gh api repos/OWNER/REPO/environments --jq '.environments[] | {name, protection_rules, deployment_branch_policy}'
   ```

4. **Written process.** Read `CONTRIBUTING*`, `README*`, `AGENTS.md`,
   `CLAUDE.md`, `docs/`, PR and issue templates, and release notes or
   changelog.

5. **Connected tools.** Check these only if they are already configured for
   this organization: a ticket tracker (look for ticket keys in branches and
   PR titles first) and shared docs. Read them. Never write to them.

Spend roughly ten minutes. Nori told the owner "a few minutes". Start the
conversation with good coverage. Do not wait for perfect coverage.

## 3. Interview

Work through the stages in order. Skip any stage the research fully settled:

1. **Idea → work item**: where work is tracked, who decides priority.
2. **Branch**: naming, how long branches live.
3. **Review**: who reviews, how many approvals, what blocks a merge.
4. **CI**: which checks matter, what happens when one is flaky.
5. **Deploy**: how a change reaches production, who can ship, how often.
6. **Release and rollback**: versioning, changelogs, how a bad deploy is
   undone.
7. **Incidents**: where they are raised, who responds.
8. **Docs and conventions**: what must be updated alongside code; anything
   a new teammate always gets wrong.

How to run it:

- **First message: tag the owner, then ask one easy question about your
  strongest inference.** A quick win builds momentum.
- **Bundle the obvious.** When a stage has several high-confidence findings
  left, put them in one "here's what I see, correct anything that's off"
  message. Do not ask one question each.
- **Use their answer.** Drop questions it already answered. Follow up on
  anything surprising ("you said hotfixes skip review; who's allowed to do
  that?"). Update your notes after every reply.
- **Format**: give one or two lines of context with the evidence, then the
  question, then lettered options. Keep each message under about 600
  characters.
- **Progress**: now and then, say roughly how much is left ("two more on
  deploys and we're done").

## 4. Route each confirmed fact

Decide where each fact belongs. Never explain this to the owner.

- **Org-wide process** (applies to every repo or to how the team works):
  goes into the organization's sessions skillset.
- **Specific to one repository or part of the codebase**: goes into a
  memory scoped with `--repos`. If memories are unavailable, skip it.
- **About one person** ("Alex always reviews infra"): save it only if the
  owner describes it as a rule of the team. Write the rule ("infra changes
  need an infra-owner review"), not the person.
- **Weak, one-off, or unconfirmed**: drop it.

## 5. Recap and confirm

When you have covered the stages, or the owner wants to stop, send one recap.
Write it in plain language, grouped by stage, in short bullets, with no file
names or formats. End with:

> Anything wrong or missing before I save this so future work follows it?

Apply corrections. Re-confirm anything that changed. Save nothing without an
explicit yes. If they decline, thank them and go to section 7.

## 6. Save what was confirmed

Bring your copy of the organization's instructions up to date first. Another
conversation may have saved to them since this machine started. Run this
before any edit in this conversation. It replaces `~/org/sessions` with the
latest published version.

```bash
profile="$HOME/.nori/profiles/$NORI_ORG/sessions"
[ ! -L "$profile" ] || rm "$profile"
sks download "$NORI_ORG/sessions" --non-interactive
[ -d "$profile" ] && [ ! -L "$profile" ] && rm -rf "$HOME/org/sessions" \
  && mv "$profile" "$HOME/org/sessions" \
  && sks link "$HOME/org/sessions" --name "$NORI_ORG/sessions"
```

If any step fails, stop and say in one sentence that saving failed. Never edit
a copy you could not refresh.

Save repository-specific facts as one memory each:

```bash
nori-sessions memories search --query '<the fact>' --repo 'github.com/OWNER/REPO' --limit 3
nori-sessions memories add --kind process \
  --content '<one self-contained fact, with its conditions>' \
  --repos 'github.com/OWNER/REPO' \
  --keywords '<deploy,release,...>' \
  --capture-mode user_requested \
  --source-json '{"source":"owner interview","confirmedBy":"<confirming admin email>"}' \
  --verified-at "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

If a matching memory exists, update it. Do not add a near-duplicate.

Save org-wide process into `~/org/sessions/`. Make **targeted edits**. Never
rewrite existing files:

- Add a short "How this team ships" section to `AGENTS.md` with the rules
  every session must follow (merge path, required review, who deploys and
  how, what must never happen).
- For each repeatable procedure the owner described (for example "shipping
  a change" or "cutting a release"), add one skill under
  `skills/<verb-ing-noun>/SKILL.md` in the canonical format: frontmatter
  `name` plus a `description` that starts "Use when", a `<required>`
  checklist of numbered steps, and `<good-example>` / `<bad-example>`
  blocks where the distinction matters.

Then follow the `maintaining-org-skillset` skill to validate and upload.
This conversation runs with admin access. The owner's or an admin's "yes" in
section 5 is the approval. If the upload is refused anyway, tell the owner in
one sentence that saving needs an admin. Do not retry with other credentials.
Go to section 7.

## 7. Close and release this machine

Send one short message. Thank them. Name two or three concrete things future
work will now do differently ("PRs will squash-merge to `main` and
wait for the `ci` check; deploys go through the Release workflow, never by
hand"). Say they can correct anything by replying in this conversation.

Then release this machine back to the pool:

```bash
nori-sessions sessions release --self --reason agent_requested
```

Release it however the conversation ends, including when they decline or ask
you to stop. If someone replies later, the conversation picks back up.

## Safety

- Never copy secrets, tokens, customer data, or personal details into notes,
  memories, or the skillset.
- Only read repositories. Never push, open PRs, comment on PRs or tickets, or
  change repository settings.
- Never create, edit, or delete automations, projects, or project context.
