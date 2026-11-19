---
name: fixing-unspecified-platform-problems
description: Use when asked to find whatever is hurting this organization's Nori users without a specific problem named - a nightly platform health run, or "what's broken lately?" - by reading the org's own service logs for the past 24 hours, picking at most one painful failure category, tracing its cause through chats, setup scripts, CI, and repos, and proposing one evidence-backed fix to the org's platform owners.
---

# Fixing Unspecified Platform Problems

Nobody has told you what is wrong. Find the single problem most likely to be
hurting this organization's users, prove what causes it, and propose one fix.
Finding nothing painful and actionable is a good outcome. Never invent work.

When the request that started you ends with this organization's settings
(where to post, which repositories, whether you may open pull requests),
those settings override anything below. When no one is watching the run, your
final reply is the only thing anyone sees.

<required>
Add these to your TODO list:

1. Freeze one 24-hour window and capture the first two queries (section 1).
2. Answer the triage question from those results (section 2).
3. Stop with "no actionable finding" if no painful category emerges (section 5).
4. Investigate the one category: impact, then cause (section 3).
5. Write a fix proposal only if the cause is supported (section 4).
6. Check for an earlier proposal of the same problem (section 4).
7. Finish with exactly one of the four outcomes (section 5).
</required>

## 1. Freeze the window and run the first two queries

Use `nori-sessions logs query`. It reads this organization's own service logs
with LogsQL, using this machine's credentials. No other access is needed.

Freeze the window once. Use the same window for every query in the run, so
counts stay comparable:

```bash
LOG_END_EPOCH=$(date -u +%s)
LOG_START=$(date -u -d "@$((LOG_END_EPOCH - 86400))" +%Y-%m-%dT%H:%M:%SZ)
LOG_END=$(date -u -d "@$LOG_END_EPOCH" +%Y-%m-%dT%H:%M:%SZ)
EVIDENCE_DIR=$(mktemp -d)

org_logs() {
  local name="$1" query="$2"
  printf '%s\n' "$query" > "$EVIDENCE_DIR/$name.logsql"
  nori-sessions logs query --start "$LOG_START" --end "$LOG_END" \
    --limit 10000 --query "$query" | tee "$EVIDENCE_DIR/$name.json"
}
```

Run both queries before you form any opinion:

```bash
org_logs by-event '* | stats by (service, level, event) count() as n | sort by (n desc)'
org_logs raw-messages 'event:log.raw | collapse_nums prettify | stats by (_msg) count() as n | sort by (n desc) | limit 30'
```

The second query is not optional. Lines that a service printed outside its
structured logger get `event:log.raw` and no `level`. The most painful
repeated failure is often there, and a severity filter misses it.
`collapse_nums prettify` replaces IDs and numbers with `<N>`, `<UUID>`, and
similar markers, so repeats of one message group together.

Read the whole first result, not just the top. Busy info events fill the top
rows, and a rare painful event (five failed session starts) sits near the
bottom. The second query's `limit 30` is a deliberate top 30; rerun it
without the limit if the 30th row still looks like a failure.

How to read the output:

- The command prints JSON with a `lines` array. Each row of a `stats` query is
  one group, and its count is a string (`"n":"5358"`).
- A `tips` array means the result reached `--limit` and may be cut off.
  Narrow the filter or the window and run it again. Never draw conclusions
  from a cut-off result.
- An `{"ok":false,...}` result is an access failure, not an empty log (see
  section 5).

## 2. The triage question

Answer this from the two results:

> What single underlying problem in the past 24 hours is likely causing the
> most user pain? No painful, actionable finding is a valid answer.

Do not ask yourself for a "root cause" yet. A cause named this early is
usually a symptom described with confidence.

Rules for reading the counts:

- **Do not start from `level:error` alone.** Many errors are harmless (a
  failed emoji reaction, an expected 404), and many painful failures have no
  level at all.
- **Count affected work, not log lines.** Retries, paired start/end records,
  and warn/info pairs for one failure are a single incident. Find the
  record's identifier fields with `field_names` (section 3), then count
  distinct values: `... | stats by (event) count() as n, count_uniq(<id field>) as affected`.
- **Check what happened next.** A transport that closed and then reconnected,
  a retry that succeeded, or an idle machine that was cleaned up on purpose
  is not user pain. Look for the success record that follows the failure.
- **Do not require `org_id`, `service`, or `level` on every row.** Raw lines
  and some services carry none of them; raw lines name their process in
  `unit` instead. These logs already belong to this organization.
- **Separate the failure from its cause.** The logs can show that machines
  became unusable. They may not show what made them unusable. Exit code 137
  alone does not prove the machine ran out of memory.

A category is worth investigating when it plausibly breaks or noticeably
slows real work for users: lost or missing replies, failed session starts,
setup scripts that fail, integrations that keep failing, or repeated
user-visible errors. A high count is not enough on its own. Pick at most one
category. If none qualifies, go to section 5 and stop.

## 3. Investigate the one category

Use the same window for follow-up queries. Always wrap alternatives in
parentheses. A bare `OR` binds looser than the space between filters and
escapes the rest of the query:

```bash
org_logs failures '(level:error OR level:warn) event:transport.* | stats by (_time:1h, event) count() as n | sort by (_time)'
org_logs samples '"<distinctive text from the message>" | fields _time, service, level, event, _msg | limit 50'
org_logs field-names '"<distinctive text>" | field_names'
```

Filter on a constant piece of the message. Never paste collapsed text from
the raw-messages query: `<N>` and `<UUID>` never match the stored text, so you
get a false zero. Use `field_names` to find which identifiers a record carries
before you count or join on them. Raw lines are timestamped when they were
collected, not when they were written, so treat their exact times as
approximate. Start with `stats` queries. Pull raw rows only as samples
with `fields` and `limit`.

Then follow the evidence outside the logs. Use whatever this organization can
reach:

| Evidence | Commands |
|----------|----------|
| Current machines and fleet | `nori-sessions health`, `nori-sessions fleet status`, `nori-sessions sessions list` |
| Problems shown in the dashboard | `nori-sessions notifications list` |
| Which chat a machine served | `nori-sessions transcripts resolve-session --session-machine-name <name>` |
| What happened in that chat | `nori-sessions transcripts summary --id <id>`, then `transcripts get --id <id>` (follow its `tips` to page) |
| Setup script | `nori-sessions fleet get-setup` (admin), else the newest `scriptType: "setup"` entry from `nori-sessions scripts list`, then `scripts get --id <version id>`. A saved version can be older than the live script; say so if you could not use `fleet get-setup` |
| CI and code | `gh run list`, `gh run view <id> --log-failed`, and the repositories under `~/org/workspace` |
| Slack-side symptoms | `nori-slack`, within the scopes it was granted |

Access limits to expect:

- `transcripts list --scope all` and `fleet get-setup` need org admin
  access. Use what you can reach. Note what you could not read.
- One machine can serve several chats. Check that a resolved chat's time
  matches the incident before you treat it as affected.
- GitHub and Slack may not be connected. Do not assume they are.

The cause is **supported** when you can point to the evidence that links the
failure to it: a log line, a transcript turn, a script line, a CI log, or a
commit. Work from timing alone is a hypothesis, not a cause.

If the cause sits inside Nori's own platform, such as Nori's service code or
its hosting, you cannot see it from here. Do not claim you found it.
Write the result as an escalation to Nori (section 4) with the impact and
the log evidence you do have.

## 4. Propose one fix

Write a proposal only when the cause is supported. Choose the smallest fix
that removes it:

- **Setup script change.** Write the exact diff against the current script
  (section 3). Never apply it yourself. Changing the setup
  script changes every future session, so a platform owner must approve it.
- **Repository fix or CI change.** Make it in a pull request only if the
  settings allow pull requests. Otherwise describe the exact change and ask.
  Branch from the default branch as `platform-fix/<short-topic>`. Open the
  pull request without a draft flag and without reviewers. Never merge, and
  never push to a default branch.
- **Integration or configuration change.** Name the exact setting and value.
  Never change it yourself.
- **Nori platform problem.** Write an escalation to Nori with the impact, the
  evidence, and what you could not see. Ask the platform owners to forward it
  to Nori.

Before you deliver, check whether this problem was already reported:

- Read recent history in the channel you will post to, if you can
  (`nori-slack conversations.history --channel <channel id> --limit 50`).
- Look for open pull requests on `platform-fix/` branches and for matching
  open issues:
  `gh pr list --repo <owner/name> --state open --json number,headRefName,url --jq '.[] | select(.headRefName | startswith("platform-fix/"))'`.

This check applies to every outcome in section 5, not only proposals. If you
already reported the same problem, the same open question, or the same access
failure in the last four weeks and nobody acted, do not post it again. Add a
reply in that thread only if the impact has clearly grown. Otherwise treat
this run as having no new finding. If your own `platform-fix/` pull request
for it is still open, do not open another.

Write the proposal in this order and keep it short:

> **Impact** → **supported cause** → **proposed fix** → **how to validate it** → **decision needed**

<good-example>
Slack rejected 1,240 "thinking" status updates in the last 24h with `must be less than 51 characters [loading_messages]`, so users see no progress indicator while the agent works. The over-long loading messages are not in our setup script, org skillset, or repos, so this looks like a Nori platform bug. Fix needed from Nori: keep each loading message under 51 characters. Validate: `event:log.raw "loading_messages" | stats count()` should drop to 0. Can you forward this to Nori?
</good-example>

<bad-example>
## Nightly Platform Health Report
I ran 14 queries. Overall the platform looks healthy! Errors: 3,412. Warnings: 9,881. Top events: ...
</bad-example>

Someone may answer "yes" in the thread your reply starts. If so, make the
change the settings allow, or the pull request, and reply with the result.

Deliver it where the settings say. In a conversation with a person, your
reply is the proposal. Contact only destinations the settings or the person
named. Finding an email address or a channel does not authorize you to use
it.

## 5. Finish with one of four outcomes

| Outcome | When | Reply |
|---------|------|-------|
| No actionable finding | Neither query returned `ok:false` or `tips`, and nothing met the bar in section 2 | Unattended: only `<no-response/>`. With a person: one sentence on what you checked |
| Investigation incomplete | A credible category emerged, but you could not support a cause | What hurts, the evidence so far, the open question, and what access or data would settle it |
| Fix proposed | Cause supported (section 4) | The proposal, or the pull request link |
| Evidence access failed | A query or required read failed, or results stayed cut off | Which command failed and its error. Never report this as "no finding" |

An unattended run whose only result was already reported (section 4) also
ends with `<no-response/>`.

## Safety

- Read-only by default. Change nothing outside a `platform-fix/` pull
  request that the settings allow.
- Never edit the setup script, integrations, environment variables,
  automations, or the org skillset. Propose those changes.
- At most one proposal and one pull request per run.
- Never put secrets, tokens, customer message text, or personal data into a
  proposal, commit, or issue. Quote log text only after collapsing IDs, and
  quote only what proves the point.
