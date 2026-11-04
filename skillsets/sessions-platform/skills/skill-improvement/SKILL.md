---
name: skill-improvement
description: Use when running a scheduled skill-improvement review of recent session transcripts to propose improvements to the org sessions skillset.
---

# Skill Improvement

You are running a scheduled, headless review of the team's recent sessions.
Your job: find lessons in the transcripts, then propose small, concrete
improvements to the org sessions skillset (`~/org/sessions/`). An org admin
reviews your proposals before anything is published. Never publish directly
in this role.

## 1. Fetch recent transcripts

List transcripts from the last week:

```bash
curl -s -H "Authorization: Bearer $NORI_SESSIONS_TOKEN" \
  "$NORI_SESSIONS_URL/api/skill-improvement/transcripts"
```

Fetch each session's transcript by id:

```bash
curl -s -H "Authorization: Bearer $NORI_SESSIONS_TOKEN" \
  "$NORI_SESSIONS_URL/api/skill-improvement/transcripts/<sessionId>"
```

Transcripts are JSONL event streams (user messages, agent messages, tool
calls). Skip transcripts that are clearly prior runs of this same
skill-improvement review.

Review at most 50 transcripts per run. The listing includes a `size` field.
If there are more than 50, rank them by likely signal, not just recency:

- Rank sessions where humans participated (Slack sessions) above unattended
  trigger runs. Corrections come from humans.
- Skip tiny transcripts. A few KB means the session did nothing.
- Expect very large transcripts to have low signal density. For oversized
  transcripts, the fetch endpoint returns only the most recent few MB
  (`truncated: true` in the response). That part holds the resolution and
  corrections.
- You may leave the rest unreviewed. Next week's run will see anything still recent.

## 2. Check prior review outcomes

Before you draft anything, fetch recently rejected and pending proposals.
Do not re-propose what the team already turned down or is still reviewing.

```bash
curl -s -H "Authorization: Bearer $NORI_SESSIONS_TOKEN" \
  "$NORI_SESSIONS_URL/api/skillset-changes?status=rejected&limit=20"
curl -s -H "Authorization: Bearer $NORI_SESSIONS_TOKEN" \
  "$NORI_SESSIONS_URL/api/skillset-changes?status=pending&limit=20"
```

Treat rejection reasons as feedback about what kinds of changes this team
does not want.

## 3. Extract lessons

Look for:

- **Corrections** — a human told the agent it did something wrong. This is
  the highest signal. A single explicit correction qualifies on its own.
- **Repeated instructions** — the same guidance given in at least 2 distinct sessions.
- **Frustration or rework** — the agent looped, guessed, or had to be steered.
- **Successful patterns** — workflows worth codifying so they happen by default.

A lesson qualifies only if it meets all of these rules:

- Evidence from at least 2 distinct sessions backs it, unless it is an
  explicit human correction.
- It is concrete and conditional ("when X, do Y"), never an aphorism.
- It changes behavior. If knowing it would not alter what the agent does,
  drop it.

## 4. Draft deltas

Read the current skillset state under `~/org/sessions/` and draft **targeted
edits to specific files**: add a bullet, amend a section, or add a small new
skill file. Never rewrite a whole SKILL.md or AGENTS.md. Repeated full
rewrites erode detail. Make each proposal reviewable on its own.

Safety rules:

- Never copy secrets, credentials, tokens, or customer data from transcripts
  into skill content. Describe the lesson, not the sensitive values.
- Write file paths relative to the skillset root (e.g.
  `skills/deploying/SKILL.md`). Never use absolute paths or `..`.

Read the current published version of the org skillset for `baseVersion`:

```bash
sks info "$NORI_ORG/sessions" 2>/dev/null || cat ~/org/sessions/nori.json
```

## 5. Submit exactly one run

Submit at most 5 proposals in a single batch. Zero proposals is a valid
outcome. Do not pad weak findings to fill a digest.

```bash
curl -s -X POST -H "Authorization: Bearer $NORI_SESSIONS_TOKEN" \
  -H "Content-Type: application/json" \
  "$NORI_SESSIONS_URL/api/skillset-changes/runs" \
  -d '{
    "summary": "<2-3 sentence overview of what you found>",
    "sessionsReviewed": <count>,
    "proposals": [
      {
        "title": "<short imperative title>",
        "rationale": "<why, citing the evidence pattern>",
        "currentFiles": { "<path>": "<current full content, empty object for new files>" },
        "suggestedFiles": { "<path>": "<proposed full content>" },
        "baseVersion": "<current published version>",
        "sourceSessionIds": ["<sessionId>", "..."]
      }
    ]
  }'
```

This call stores the proposals and posts the review digest to the team's
Slack channel automatically. Finish by reporting how many sessions you
reviewed and how many proposals you submitted.
