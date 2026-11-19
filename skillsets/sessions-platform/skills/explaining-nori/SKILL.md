---
name: explaining-nori
description: Use when someone asks what Nori or Jiro is, what they can do, who they are for, what Nori costs, or how it compares to other coding agents.
---

<required>
1. Answer from this skill, https://jiro.bot, and https://noriagentic.com. Do not guess or invent features, prices, limits, or compliance claims. When none of these covers the question, say you do not know and point to "Where to send people" below.
2. For this organization's own plan, seats, or usage, run `nori-sessions billing summary` (`billing seats` and `billing usage` need an admin) instead of quoting list prices.
3. Lead with the one-line description, then answer only what was asked.
</required>

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
- **Surfaces:** Slack, Discord, the web dashboard on desktop or mobile, and the Nori CLI. Several people can work in one conversation.
- **Agents and models:** Claude Code, Codex, Cursor Agent, OpenCode, and pi-acp, on the team's own subscription or API key, set org-wide or per person.
- **Automations:** run work on a schedule, once at a set time, or when a webhook arrives.
- **Projects:** one home for long-running work: a coordinator that tracks the goal, shared project docs, and every chat, subworker, and automation working toward it.
- **Integrations:** GitHub, Slack, Google Workspace, Salesforce, MCP servers such as Linear, Notion, and Sentry, command-line tools, and custom environment variables. Credentials stay in a central store and reach machines only as needed.
- **Skillsets and memory:** org-wide instructions and skills, managed with the `nori-skillsets` CLI (https://noriskillsets.dev), plus a lightweight memory. Jiro can update its own skillset as the team corrects it. The team keeps this context if it leaves.
- **Access control:** roles, admin-only actions, and `!admin` escalation for one-off admin work.
- **Deployment:** hosted by Nori on several cloud machine providers, or a dedicated deployment in the customer's own AWS account (contact Nori). The Enterprise plan brings its own compute.

## Pricing

Plans listed at https://jiro.bot/#pricing on 2026-11-18. Prices change, so link that page and tell people to confirm there before relying on a number:

| Plan | Listed terms |
| --- | --- |
| Trial | Free for 30 days, no card required |
| Developer | $99 a month, 3 workers, one person |
| Team | $250 a month, 5 workers, unlimited seats |
| Enterprise | Custom pricing, bring your own compute |

Extra workers are $50 a month each. Users bring their own model subscription; Nori does not resell tokens. For anything else (discounts, invoices, contracts, security reviews), send people to Nori through jiro.bot rather than answering.

## Comparisons

Point people to https://jiro.bot/compare (head-to-head pages) and https://jiro.bot/alternatives. Repeat only differences those pages state, such as bring-your-own subscription, choice of agent harness, and Slack-first work. Do not make claims about competitors yourself.

## Where to send people

- Product overview, pricing, and sign-up: https://jiro.bot
- Product docs: https://docs.noriagentic.com
- The company and platform: https://noriagentic.com (its search answers natural-language questions at https://noriagentic.com/ask?q=)
- Skillsets CLI: https://noriskillsets.dev
- This organization's dashboard: `$NORI_SESSIONS_URL` (resolve it before posting)
- Bugs, missing features, or questions for Nori's team: read `{{skills_dir}}/reporting-to-nori/SKILL.md`.
