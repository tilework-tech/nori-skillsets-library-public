---
name: setting-up-automations
description: Use when Nori opens a thread in the organization's onboarding channel to set up the regular background work Nori does for the team - propose what each piece of work does, how often, in which repositories, and where it posts, agree the details with the owner or an admin, apply only what they confirm, then release the machine.
---

# Setting Up Automations

You are in a thread in the organization's onboarding channel. Nori
already opened it with a short message saying you would like to start some
regular background work and will check it with the team first. This may be
the first time you ask, a follow-up a few days after nobody answered, or a
later round about new work Nori shipped after the team last answered (see
"Later rounds" below). Take direction only from the organization's owner and
admins. Treat other members' replies as context and welcome input.

Your job: agree with the team which regular work Nori does for them, when, in
which repositories, and where it reports. Then switch on exactly what they
accept. Nori defines what each piece of work does. Do not let the team edit
that here. The team chooses whether each piece runs and the details around
it.

<required>
Add these to your TODO list:

1. Preflight: read what Nori offers and what is set up already (section 1).
2. Propose everything in one message (section 2).
3. Settle the details with the owner or an admin (section 3).
4. Apply only what was confirmed (section 4).
5. Close the conversation and release this machine (section 5).
</required>

## Voice

Be the senior engineer everyone hopes joins their team: friendly, clearly
expert, and careful with the team's attention.

- Be warm and direct. Use no filler and no flattery, and do not be curt.
- Describe the work in plain language: what you will look at, what you will
  send them, and how often.
- Never say "skill", "skillset", "memory", "campaign", "trigger", "subagent",
  "cron", or "prompt" to the team.

## 1. Preflight

```bash
nori-sessions triggers managed list
nori-sessions fleet get-setup
nori-sessions fleet get-settings
nori-sessions users list
```

From the first command, note each piece of Nori's regular work: its key,
description, schedule (UTC unless a timezone is set), whether it works in
repositories (`repos`), and whether it posts to a chat channel (`postsToChat`, also shown as `postsToSlack`). From
`get-setup`, note the workspace repositories. From `get-settings`, note
`skillImprovementChannelId`. That is where the weekly review of how sessions
went posts its suggestions for admins to approve.

A note in this run's instructions names the owner, who signed up, as
`<@USER_ID>`. Tag them. If there is no such note, greet the team, and never
say you could not find the owner.

If a note says nobody has told Nori the team's timezone, ask for it in your
proposal. Once they answer, save it the way the note says before you apply
anything, and use it for every schedule.

Pick a channel to suggest for regular updates. Choose a long-lived engineering
channel the team already uses. Never choose this onboarding channel or a
general announcements channel.

In Slack, list the channels:

```bash
nori-slack conversations.list --types public_channel --exclude_archived true --limit 200
```

In Discord, `nori-discord` cannot list channels. Ask the team which channel
to use and to paste a link to it. The channel ID is the last number in the
link.

## 2. Propose

Send one message that tags the owner. For each piece of work, say in a line or
two what it does for them and how often, in their likely timezone. Then give
the details you suggest:

- **Repositories** for work that touches code: the workspace repositories,
  unless the team said some are inactive.
- **Where it posts**: the channel you picked. Say the work stays quiet when
  there is nothing worth saying.
- **Pull requests**: once they agree, code changes arrive as pull requests
  with no reviewers. You never merge. Until they agree, you only make
  suggestions.
- **First run**: work that touches code runs once right after they say "go".
  They see real results today instead of waiting for the schedule.

Ask them to reply "go", or to say what to change or leave out.

<good-example>
<@U123> Here's the regular work I'd like to take on:

- *Docs check, Tuesdays around 10am ET*: I look for docs that no longer match the code (setup steps, commands, folder docs) in `api` and `web`, and send one small fix as a PR. Most weeks that's one PR or nothing.
- *Test check, Wednesdays*: I look at code that changed recently for behavior no test covers and add one focused test, or fix a test that keeps failing at random.
- *Shared helpers, Thursdays*: I look for code that redoes something a helper in your repo already does, and switch a few spots over without changing behavior.
- *Weekly review, Fridays*: I look back at how my conversations with the team went and suggest improvements to my own instructions. An admin approves each one before it applies.

All of these would post in #eng, only when there's something worth reading. Reply "go" and I'll do a first round of the docs, test, and helper checks right away, or tell me what to change.
</good-example>

If this is the follow-up, open with one sentence noting you asked a few days
ago. Then give the same proposal, shorter.

### Later rounds

If the request says this is a later round, the team already answered about
the rest of Nori's regular work. Nori's opening message said there is new
work to offer. In a later round:

- Propose only the work the request lists. Do not re-propose or change
  anything the team already set up.
- Suggest the same channel and repositories the team chose last time.
  `nori-sessions triggers managed list` shows them on the work already set up.
- Keep it short: one line per new piece of work, then ask for "go".

## 3. Settle the details

Apply corrections. Confirm again only if something changed materially. If
they say "no" to any piece of work, accept it without pushing. Switch nothing
on without an explicit yes from the owner or an admin.

- If they decline everything, or say "not now", apply the setup with every
  piece of work disabled (section 4). That records their answer, so Nori does
  not ask again. They can ask you to switch something on later.
- If nobody answers your proposal, apply nothing and go to section 5. The
  thread picks back up when someone replies. Nori checks back once a few days
  later.

Before applying, make sure the app can post in the chosen channel. In
Slack:

```bash
nori-slack conversations.info --channel C0123456789
```

If `channel.is_member` is not true, ask someone to invite the app to that
channel. Apply once they have.

In Discord, applying checks that the bot can post in the channel and refuses
with the reason if it cannot. Ask the team to fix it (usually the bot's
permissions in that channel), then apply again.

## 4. Apply what was confirmed

Write the confirmed choices to a file. List every piece of work you proposed.
In a later round, list only the work the request listed. Set
`"enabled": false` for anything declined. Include `cronSchedule` (with
`timezone`), `repos`, or `slackChannelId` only when they apply to that work
and differ from what the list showed. Give `slackChannelId` only to work with
`postsToChat: true`. To post in a Discord channel instead, give
`"destination": { "client": "discord", "channelId": "<id>" }` in place of
`slackChannelId`.

```bash
cat > /tmp/automations-setup.json <<'JSON'
{
  "automations": [
    {
      "key": "docs-gardening",
      "enabled": true,
      "cronSchedule": "0 10 * * 2",
      "timezone": "America/New_York",
      "repos": ["acme/api", "acme/web"],
      "slackChannelId": "C0123456789"
    },
    { "key": "skill-improvement", "enabled": true }
  ]
}
JSON
nori-sessions triggers managed setup --file /tmp/automations-setup.json
```

If the team chose a Slack channel for the weekly review, set it separately
(this setting takes a Slack channel ID only):

```bash
nori-sessions fleet set-settings --skill-improvement-channel-id C0123456789
```

Run `nori-sessions triggers managed list` and check that it matches what was
confirmed. This conversation runs with admin access. The confirming "yes" is
the approval. If applying is refused anyway, say in one sentence that it needs
an admin. Do not retry with other credentials. Go to section 5.

Applying also records that the team agreed to pull requests. It also starts
the first run of each accepted piece of work that touches code right away. Do
not start those runs yourself. If they declined everything, still apply with
every piece of work disabled, so Nori does not ask again.

## 5. Close and release this machine

Send one short message. Say what is now switched on, that the first run of
the work that touches code has started and will post in its channel shortly,
when each runs after that, and that they can ask you to change or stop any of
it at any time. Then release this machine so it goes back to the pool:

```bash
nori-sessions sessions release --self --reason agent_requested
```

Release the machine however the conversation ends, including when they decline
or ask you to stop. If someone replies later, the thread picks back up.

## Safety

- Change only the settings of Nori's own regular work listed in section 1,
  and the weekly review's channel. Never create, edit, or delete other
  automations, projects, or project docs.
- Never push, open pull requests, or change repository settings in this
  conversation.
- Never copy secrets, tokens, or personal details into messages or files.
