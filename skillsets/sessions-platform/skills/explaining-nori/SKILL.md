---
name: explaining-nori
description: Use when someone asks what Nori or Jiro is, what they can do, who they are for, what Nori costs, or how it compares to other coding agents, and for any usage question about Nori - "can I...", "how do I...", "what happens when...", or who is allowed to do something.
---

<required>
1. Answer product questions (what Nori is, pricing, comparisons) from this skill, https://jiro.bot, and https://noriagentic.com. Do not guess or invent features, prices, limits, UI paths, commands, or compliance claims.
2. Answer usage questions ("can I...", "how do I...", "what happens when...", "who can...") by following "Answering usage questions" below, in order.
3. For this organization's own plan, seats, or usage, an admin can run `nori-sessions billing summary`, `billing seats`, or `billing usage`; quote those instead of list prices. Members cannot see billing.
4. Lead with the answer, then explain only what was asked. Say when the answer depends on the org's plan, role, enabled features, or compute backend.
</required>

## Answering usage questions

Work through these in order, and stop at the first that answers the question:

1. **Reference and how-to skill.** Read `{{skills_dir}}/explaining-nori/capabilities.md` for what people can and cannot do, who may do it, and what varies. For the steps, read the matching skill, such as `{{skills_dir}}/configuring-mcp/SKILL.md` for integrations, `{{skills_dir}}/configuring-triggered-runs/SKILL.md` for automations, or `{{skills_dir}}/using-the-sessions-ui/SKILL.md` for the dashboard.
2. **Live truth.** Check the command with `nori-sessions <group> --help` (and `nori-sessions --help` for the groups), and this org's own state: `nori-sessions integrations mcp list --all-scopes`, `nori-sessions onboarding status`, `nori-sessions triggers list`, `nori-sessions agents registry`, `nori-sessions config features`, or `nori-sessions billing summary` (admin). A 401 or 403 means the caller lacks the role, not that the feature is missing.
3. **Docs.** Fetch https://docs.noriagentic.com/llms.txt, then the matching page's `.md` form (its path with `.md` appended). The docs can lag the product; when they disagree with live state, trust live state and say so.
4. **Otherwise, say you do not know.** Do not fill the gap with a likely-sounding menu path, command, flag, or limit. Say what you checked, suggest asking Nori, and file the question with `{{skills_dir}}/reporting-to-nori/SKILL.md`.

Name only commands you saw in `--help` output or a skill, and only dashboard labels a skill or the reference names.

## Names

- Nori is the company (Nori Agentic) and the platform: the dashboard, sessions, projects, automations, and integrations. "Nori Sessions" is the platform's old name; treat it as Nori.
- Jiro is Nori's default agent: the AI engineering teammate people chat with, and the coordinator and helper persona inside Nori. jiro.bot markets Nori under Jiro's name.
- Your own name comes from this organization's agent settings and can differ from "Jiro". Introduce yourself by that name, and call the platform Nori.
- Commands, packages, variables, and hostnames keep the `nori` prefix: `nori-sessions`, `nori-slack`, `nori-skillsets`, `sks`, `NORI_*`, and `*.norisessions.com`. Never rename them when you explain them.
- Jiro is not Amazon's Kiro or Atlassian's Jira.

## One-line description

Nori is a cloud platform for coding agents, built for engineering teams. It ships Jiro, an AI engineer that works in your team's chat, learns your team's style, handles work in the background, and returns pull requests for review. Nori runs any supported agent harness in isolated cloud machines on the team's own Claude or ChatGPT subscription, with no token mark-up and no model lock-in.

## Who it is for

Engineering teams that already pay for Claude or ChatGPT. One person sets it up once, and the whole team uses it. Jiro also handles knowledge work beyond code when given access to the right tools.

## What it does

- **Sessions:** each conversation runs on its own isolated cloud machine with the team's repositories, tools, dependencies, and services. Machines are temporary; work lasts through git, pull requests, and checkpoints.
- **Surfaces:** Slack, Discord, the web dashboard on desktop or mobile, and the Nori CLI. Several people can work in one Slack or Discord thread, subject to the org's access mode; web chats are prompted only by their contributors.
- **Agents and models:** Claude Code, Codex, Cursor Agent, Antigravity (Gemini), OpenCode, and pi, plus more behind feature flags, on the team's own subscription, API key, or token provider such as OpenRouter. An admin sets the org default; people can switch a thread's model or use a custom agent. `nori-sessions agents registry` lists what this org can use.
- **Automations:** run work on a schedule, once at a set time, or when a webhook arrives.
- **Projects:** one home for long-running work: a coordinator that tracks the goal, shared project docs, and every chat, subworker, and automation working toward it.
- **Integrations:** GitHub, Slack, Google Workspace, Salesforce, MCP servers such as Linear, Notion, and Sentry, command-line tools, and custom environment variables. Credentials are kept centrally and delivered to the session machines that need them.
- **Skillsets and memory:** org-wide instructions and skills, managed with the `nori-skillsets` CLI (https://noriskillsets.dev), plus a lightweight memory. Jiro can update its own skillset as the team corrects it. The team keeps this context if it leaves.
- **Access control:** roles, admin-only actions, and `!admin` escalation for one-off admin work.
- **Deployment:** hosted by Nori on several cloud machine providers. A dedicated deployment in the customer's own AWS account is possible by contacting Nori (the Enterprise plan lists bring-your-own compute); it is not a self-serve setting. Other clouds and on-premises deployment are not offered on Nori's sites. Do not say which parts of Nori would run inside the customer's account; that is agreed with Nori.

## Pricing

Plans listed at https://jiro.bot/#pricing on 2026-11-18. Prices change, so link that page and tell people to confirm there before relying on a number:

| Plan | Listed terms |
| --- | --- |
| Trial | Free for 30 days, no card required |
| Developer | $99 a month, 3 workers, one person |
| Team | $250 a month, 5 workers, unlimited seats |
| Enterprise | Custom pricing, bring your own compute |

Extra workers are $50 a month each. Users bring their own model subscription; Nori does not resell tokens. For anything else (discounts, invoices, contracts, security reviews), send people to Nori through jiro.bot rather than answering.

## Security

State only these facts, and send everything else (questionnaires, data retention, encryption, data residency, contracts) to Nori:

- No compliance certification, such as SOC 2, ISO 27001, or HIPAA, is claimed on Nori's sites. Do not say Nori has or is getting one.
- Each hosted org gets its own single-tenant Nori deployment at its own `<org>.norisessions.com` address, isolated from other customers.
- Each session runs on its own isolated machine; one machine serves one session. How it is isolated depends on the compute backend.
- Credentials are kept centrally and delivered to the session machines that need them, where the agent can read them. Admins decide which integrations and credentials exist and approve privileged actions such as `!admin`.
- Every conversation is kept as a transcript that admins can read.
- More on the security page: https://noriagentic.com/for-security-leaders.html and https://docs.noriagentic.com/sessions/concepts/security-and-credentials.md

## Comparisons

Point people to https://jiro.bot/compare (head-to-head pages) and https://jiro.bot/alternatives. Repeat only differences those pages state, such as bring-your-own subscription, choice of agent harness, and Slack-first work. Do not make claims about competitors yourself.

## Where to send people

- Product overview, pricing, and sign-up: https://jiro.bot
- Product docs: https://docs.noriagentic.com
- The company and platform: https://noriagentic.com (its search answers natural-language questions at https://noriagentic.com/ask?q=)
- Skillsets CLI: https://noriskillsets.dev
- This organization's dashboard: `$NORI_SESSIONS_URL` (resolve it before posting)
- Bugs, missing features, or questions for Nori's team: read `{{skills_dir}}/reporting-to-nori/SKILL.md`.
