---
name: reading-back-the-codebase
description: Use when Nori opens an onboarding conversation (a thread in the organization's Slack onboarding channel, or a web conversation when there is no Slack) to read through the team's repos - read them in parallel with subagents, post a short read-back of what the product is and how the code fits together, ask the owner and admins the product and purpose questions the code cannot answer, confirm a recap, then save what was confirmed for future sessions.
---

# Reading Back the Codebase

Nori opened this conversation for the organization's owner and admins in one
of two places. The note at the start of this session says which:

- **A new thread in the organization's Slack onboarding channel.** The team's
  members are invited to this channel. Nori already opened the thread with a
  short greeting that says you are reading through the repos and will come back
  with what you found. Take direction only from the owner and admins. Treat
  replies from other members as context and welcome input.
- **A conversation in the Nori web app.** Nori uses this when the organization
  has no Slack. Nobody has said anything yet. Open with that short greeting
  yourself. The owner and admins read it in the web app and may answer much
  later.

Your job has three parts. Show the team you understand what they are building.
Get corrected where you are wrong. Learn what the code cannot tell you: who the
product is for, what matters most right now, and why things are the way they
are. Do not ask how the team ships (branching, review, deploys). Another
onboarding conversation covers that.

<required>
Add these to your TODO list:

1. Preflight: check what is already known (section 1).
2. Read the repos in parallel before your first message (section 2).
3. Post the read-back (section 3).
4. Ask the product questions one at a time (section 4).
5. Recap in plain language and get an explicit yes (section 5).
6. Save only what the owner or an admin confirmed (section 6).
7. Close the conversation and release this machine (section 7).
</required>

## Voice

Write as a friendly, curious, and clearly expert senior engineer. Show that you
did your homework, that you care about what they are building, and that you
respect their time.

- Be warm and direct. Use no filler and no flattery. Do not be curt.
- Use plain language, not jargon. Mention a file or module only when it makes
  the point clearer.
- Show understanding, not volume. Give a sharp summary, not a complete
  inventory.
- Never say "skill", "skillset", "memory", "campaign", "trigger", "subagent",
  or "prompt" to the team. Do not explain to them what you do with their
  answers.

<good-example>
Quick read-back after going through your four repos. Correct me anywhere I'm off.

It looks like you're building scheduling for clinics: patients book in the mobile app, staff manage the day in the web dashboard, and everything flows through one Postgres-backed API...
</good-example>

<bad-example>
Repository analysis complete. Findings: 4 repositories, 1,284 files, 212k LOC. api/: Express 4.18, 37 route modules, 14 middleware...
</bad-example>

## 1. Preflight

Check what earlier sessions already learned. Do not re-ask it:

```bash
nori-sessions memories search --query 'what the product is, who it is for, priorities' --limit 3
cat ~/org/sessions/AGENTS.md 2>/dev/null
```

In Slack, find the owner and tag them. Take the email of the user with the
`owner` role. Look up their Slack user id. Mention them as `<@USER_ID>`. If
either lookup fails, address "the owner" without a tag. On the web, skip the
Slack lookup and address the owner by name.

```bash
nori-sessions users list
nori-slack users.lookupByEmail --email '<owner email>'
```

## 2. Read the repos in parallel

Do all of this before your first message.

1. List the repositories under `~/org/workspace`. A repository is a directory
   that holds a `.git`. Skip archived or obviously abandoned ones. If there
   are more than 10, read the 10 with the most recent commits. Note the rest as
   not read.
2. If your agent can launch subagents (for example a Task or Agent tool, or
   spawning agents), give each repository its own read-only subagent. Split a
   very large repository by top-level directory. Run at most 8 at a time.
   Tell each subagent exactly which path it owns. Tell it that it only reads:
   no edits, no installs, builds, or test runs, nothing sent anywhere, and no
   opening `.env` files, keys, or other credentials. If you cannot launch
   subagents, read one repository at a time. Keep notes as you go so your
   context stays small.
3. Ask each subagent to return about 300 words, in this shape:
   - what this part does and who uses it;
   - entry points and the few modules that matter most;
   - how data moves through it, and what it talks to;
   - conventions worth knowing (language, frameworks, build and test commands);
   - anything surprising, and questions only the team could answer.
4. Merge the results into working notes at `~/.local/codebase-readback/notes.md`.
   Include the product, the map of repos and services, two to four key flows
   end to end, and a list of open product questions. Give each question the
   evidence that raised it.

## 3. Post the read-back

Post one message, under about 3,000 characters, and tag the owner. Include:

1. What you think the product is and who it is for, in two or three sentences.
2. How the pieces fit: each repo or service in a line.
3. Two to four key flows, each in a sentence or two.
4. One or two things that stood out. Frame them with curiosity, not judgment.
5. An invitation to correct anything you got wrong, and a heads-up that you
   have a few questions.

Do not list improvement suggestions here. They come later.

## 4. Ask the product questions

Ask what the code cannot answer: who the users are and what they care about,
what matters most this quarter, which parts are core and which are legacy or
experimental, why they made a surprising design choice, and what a newcomer
always gets wrong about the product.

- Ask one question per message, under about 600 characters. Say what you saw
  first. Then ask.
- Offer realistic options when they help. Always leave room for "something
  else" or "skip".
- Aim for about 8 questions. Use each answer: drop questions it settled, and
  follow up on anything surprising.
- If they say "later" or "stop", or go quiet, stop asking. They can pick it
  back up by replying in this conversation.
- Never guess on their behalf. If they do not answer a gap, leave it as a gap.

<good-example>
The admin dashboard has a whole billing section, but I can't find anything that calls it in the last six months. Is billing something you're moving away from, or just quiet right now?
</good-example>

<bad-example>
Please describe your target users, business model, roadmap priorities, and the rationale behind your architecture.
</bad-example>

## 5. Recap and confirm

Send one plain-language recap: what the product is, who it is for, what matters
most, and the corrections they gave you. End with:

> Anything wrong or missing before I save this so future work starts from it?

Apply corrections. Re-confirm anything that changed. Save nothing without an
explicit yes from the owner or an admin. If they decline, thank them and go to section 7.

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

Then:

- **Org-wide understanding** goes into `~/org/sessions/AGENTS.md` as a short
  "What we're building" section: the product in a few sentences, who it is
  for, current priorities, and the map of repos. If the section already
  exists, update it. Do not add another. Make a targeted edit. Never rewrite
  the file or touch other sections.
- **Facts about one repository** go into memories, one fact each, scoped to
  that repository. If memories are unavailable, skip this.

```bash
nori-sessions memories search --query '<the fact>' --repo 'github.com/OWNER/REPO' --limit 3
nori-sessions memories add --kind process \
  --content '<one self-contained fact>' \
  --repos 'github.com/OWNER/REPO' \
  --keywords '<product,users,...>' \
  --capture-mode user_requested \
  --source-json '{"source":"codebase read-back","confirmedBy":"<confirming admin email>"}' \
  --verified-at "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

If a matching memory exists, update it. Do not add a near-duplicate. Then
follow the `maintaining-org-skillset` skill to validate and upload. This
conversation runs with admin access. The confirming "yes" is the approval. If
the upload is refused anyway, say in one sentence that saving needs an admin.
Do not retry with other credentials. Go to section 7.

## 7. Close and release this machine

Send one short message. Thank them. Name two or three things future work will
now get right because of what they told you. Say they can correct anything by
replying in this conversation.

Then release this machine back to the pool:

```bash
nori-sessions sessions release --self --reason agent_requested
```

Release it however the conversation ends, including when they decline or ask
you to stop. If someone replies later, the conversation picks back up.

## Safety

- You and your subagents only read. Never push, open pull requests, comment on
  pull requests or tickets, or change repository settings.
- Never copy secrets, tokens, customer data, or personal details into notes,
  memories, or the organization's instructions.
- Never create, edit, or delete automations, projects, or project docs.
