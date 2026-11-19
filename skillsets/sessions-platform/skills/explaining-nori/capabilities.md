# What people can and cannot do in Nori

A reference for "can I ...?", "how do I ...?", and "what happens when ...?" questions. Many answers vary by org, plan, role, feature flag, or compute backend; each bullet says so where it does. When this file and live state disagree, live state wins: check `nori-sessions <group> --help` and this org's own settings (see "Answering usage questions" in `SKILL.md`).

Roles used below: **owner**, **admin**, and **member** are org roles. In a chat, **contributors** can prompt and **followers** can only read. "Admin" includes owners unless a bullet says owner only.

## Sessions and machines

- Each conversation runs on its own isolated cloud machine, claimed from the org's pool when the chat starts. Other chats never see its files.
- **What is wiped:** the machine. When a session is released, restarted, or destroyed, everything on the machine is gone: files outside git repositories, installed tools, running processes and dev servers, shell history.
- **What persists:**
  - The conversation transcript, readable in the dashboard history.
  - A checkpoint taken at the end of each turn of every git repository (and linked worktree) under `~/org/workspace`, including uncommitted and untracked changes.
  - Checkpoints leave out gitignored files (except under `.worktrees/` and inside linked worktrees) and build and dependency folders such as `node_modules`, `dist`, `build`, `.next`, `target`, `.venv`, and `__pycache__`, at any depth.
  - Checkpoints are not pushed to the git remote. Push a branch for anything that must outlive the conversation or be seen by others.
  - Work done after the last finished turn is not in a checkpoint.
- **Checkpoint limits:** 2 GiB per checkpoint by default. Above that, checkpointing pauses for the session (with a notice in the chat where there is one) and resumes once the workspace is small enough. Only the newest few checkpoints per session are kept. No fixed retention period for transcripts or checkpoints is published; ask Nori.
- **Resuming:** send a message in the old chat in the dashboard, reply in the same Slack or Discord thread, use `!resume` in Slack to pick from past sessions, or run `nori-sessions sessions resume`. A resumed conversation runs on a fresh machine with the conversation and the last checkpoint restored. If the files cannot be restored, the web offers to resume with the conversation only. A new chat never sees another chat's files.
- **Idle:** a session with no activity for 1 hour is marked idle, and an idle session is released after 12 more hours. Running turns keep it active. Admins can change both timeouts (`nori-sessions fleet set-settings --help`).
- **Release vs Restart vs Destroy:**
  - Release (`!done` or `!release` in Slack or Discord, "Release session" in the web chat menu, or `nori-sessions sessions release`): ends the session, returns the machine to the pool, and keeps the conversation resumable. Contributors or admins.
  - `!restart` in a thread: restarts the agent on the same machine and continues the conversation; the machine's files stay. Contributors or admins.
  - Restart on a fleet row (Settings, admin): ends the live session and frees its machine; the next message resumes the conversation on a fresh machine, as after a release.
  - Destroy (fleet row): deletes the machine. Admin only.
  - Restart Fleet (Settings): deletes and reprovisions every machine, including machines in use, which interrupts all running work. Admin only.
- **Concurrency:** the number of sessions running at once is capped by the org's machine allowance. With usage-based billing off, the cap is the lower of the fleet size and the billed machine count; with it on, the billed allowance applies and extra work can start an overage machine. Over the cap, new web chats wait in a queue instead of failing. Idle warm-pool machines do not count. Check `nori-sessions billing summary` (admin).
- **Machine size:** varies by backend and org. Where the org has machine sizes turned on, admins choose small (1 vCPU, 2 GiB) to xlarge (8 vCPU, 16 GiB), and a custom agent can have its own size. Memory and CPU readings inside the machine (`free`, `/proc/meminfo`, `nproc`) are not reliable.

## What an agent on the machine can do

- Run shell commands, install packages and tools for the session, clone repos the org's GitHub app can reach, run tests and builds, open pull requests, and use a real Chrome browser that people can watch and take over.
- **Persistent tools:** an install lasts only for that session. For every session, an admin adds it to the org setup script (Settings > Sessions, or `nori-sessions fleet get-setup` / `fleet set-setup --org-script-file`). The script runs when machines are provisioned or refreshed, not in running sessions.
- **Sharing a running app:** the session URL serves the most recently started port, and `<session URL>/port/<N>/` serves any port. The link is not public: viewers must sign in to the dashboard as members of the same org. Any member can view the app; contributors and admins also get the shell, chat, and browser. The link stops working when the session ends. Ports 8080-8089, 2019, 6901, and 9222 are reserved.
- **Docker:** depends on the compute backend. The default hosted sandbox runtime cannot run a Docker daemon. VM-based backends (the legacy hosted VM backend, or an org Nori has configured for a VM runtime) run Docker, and the admin "Enable Docker" setting applies only to the legacy VM backend. Other backends do not ship Docker. Check `docker info` in the session.
- **Network:** outbound internet access is open on hosted backends. Only an experimental backend applies a domain allowlist.
- **Scheduling:** use automations, never cron or sleep loops on the machine, because the machine goes away.

## Surfaces and chat commands

- Slack, Discord, the web dashboard (desktop, mobile, installable as a PWA), the Nori CLI (`nori cloud`), and a terminal attached to the session through Handroll.
- **Several people in one conversation:** yes in Slack and Discord threads. Each message is attributed to its author, and org members who post become contributors. Who may talk to the agent depends on the org's Slack access mode (open: anyone in the workspace; guarded, the default: org members plus listed exceptions; strict: admins plus exceptions) or Discord mode (open, or members who linked their account with `!link`). On the Developer plan, only members can use the Slack and Discord bot.
- **Web chats** have no invite-to-chat feature: only contributors prompt there. Admins can prompt other people's chats only when the org allows it.
- **Thread commands** (`!help` lists them): `!done` / `!release` release the session; `!tagonly` toggles replying to every message vs only @mentions; `!admin` asks for a 30-minute admin grant that any org admin approves; `!status`, `!cancel`, `!interrupt <prompt>`, `!compact`, `!restart`, `!skillsets`, `!model`, `!provider`, `!shell` / `!urls`. Slack only: `!resume`, `!catchup`, and `!project` (needs the org's channel-mode feature and its project-command setting). Write commands with no space after `!`.

## Roles and access

- **Owner only:** change plan or capacity, opt in to usage-based billing, grant or remove the owner role.
- **Admin:** Settings (Fleet, Sessions, Users, Security, Billing, and Views where custom views are on), the setup script, org-wide integrations and custom env vars, the org default provider and model, custom agents, approving automations, deleting automations, Destroy and Restart fleet, uploading the org skillset.
- **Any member:** chat, create projects, propose automations (an admin approves them), connect personal integrations where the org has access control, view a session's shared app.
- **Invites:** admins only, from Settings > Users ("New Invite" link with max uses, optional email domain, and expiry, which joins as member; or "Add by Email" with a role) or `nori-sessions invites create`. Only owners can add an owner. The Developer plan cannot add members.
- **Reading chats:** owners and admins can read every chat. Members see chats they contributed to or follow, plus project chats by default; an admin can restrict members to their own chats (`nori-sessions access policy set --help`).
- **`!admin` escalation:** from a session, admin-only commands are refused until the person replies `!admin` and an org admin approves; the grant lasts 30 minutes.

## Integrations and credentials

- **Kinds:** built-ins (GitHub app "Jiro (by Nori)", Slack, Discord, Google Workspace, Salesforce), MCP servers from a catalog of about 70 (Linear, Sentry, Notion, PostHog, Datadog, Atlassian, Figma, and more) or any custom MCP URL, managed CLI presets (AWS, Snowflake, Luma), and custom environment variables. List what is connected with `nori-sessions integrations mcp list --all-scopes` and `nori-sessions onboarding status`.
- **Scope:** org-wide by default (admin). Where the org has access control, people can also connect personal integrations and env vars for their own sessions, and admins can scope them to one custom agent. When names collide, agent beats personal beats org.
- **Who acts as whom:** a chat gets the personal credentials of its starter, the conversation's first contributor. Automations and project runs get only org credentials, except a personal automation, which acts as its author.
- **GitHub identity:** pushes use the GitHub app. Where the admin enabled GitHub user attribution (Settings > Security), each person connects their own GitHub account on the Integrations page, and PRs, comments, and reviews then show as them. `GH_TOKEN` and `GITHUB_TOKEN` cannot be set as custom env vars.
- **When changes apply:** a newly connected MCP server, and the tokens and env vars of any integration, reach the next new chat or automation run, with no fleet restart; the current chat does not gain a new MCP server. A saved custom env var is also pushed to running machines (new shells pick it up). Install scripts of CLI tools, setup script changes, and org skillset uploads run only when a machine is provisioned, so machines already waiting in the pool can lack them for a while.
- **Secrets:** never paste secrets into chat; the agent serves a private form behind the dashboard login instead. Integration tokens and keys are delivered to session machines as files the agent can read.

## Automations

- **Kinds:** a cron schedule (with a timezone; UTC when none is given on the CLI), a one-time reminder, a webhook, or a run after another automation.
- **Create:** the dashboard Automations page or `nori-sessions triggers create`.
- **Approval:** an admin's automation is live immediately. A member's create or edit waits as "Change awaiting approval" until an admin approves it under "Review requests"; the old version keeps running meanwhile. Only admins delete automations.
- **Where output goes:** each run is a chat in the dashboard. With a Slack channel set, each run posts a new thread there (the bot must be in the channel). With `--deliver-to coordinator`, it wakes a project's coordinator. Personal automations (where access control is on) run as their author, either standalone or in the author's Slack DM, never in a project.

## Projects

- A project is one home for long-running work: a coordinator agent that holds the goal, a shared `docs.md` that agents and people edit, the chats and subworkers doing the work, and automations such as heartbeats that wake the coordinator.
- **Start one:** Projects page > New project (name, desired outcome, optionally start now), move existing chats into it from the sidebar ("Move to project"), `nori-sessions projects create`, or `!project` in a Slack thread where the org enables it. Any member can create one.

## Agents and models

- **Harnesses:** Claude Code, Codex, Cursor Agent, Antigravity (Gemini, with a Google AI Studio key), OpenCode, and pi. More (such as Goose, GitHub Copilot CLI, Grok Build, Kimi Code, Cortex Code) are behind feature flags or deployment settings. `nori-sessions agents registry` lists the harnesses and token providers this org can use, and `nori-sessions agents usable` the agents a person can start a chat with.
- **Models and credentials:** the team brings its own subscription or API keys. Token providers such as OpenRouter, Fireworks AI, Cloudflare Workers AI, or a custom OpenAI- or Anthropic-compatible endpoint can also be connected. Nori does not provide or resell a model.
- **Org default provider and model:** admin only. Connect and enable the provider, then Integrations > Token providers > "Set as org default", or `nori-sessions config set-provider` and `config set-model` (`config get-models` lists ids; `config set-enabled-providers` picks which are offered). `fleet set-agent` changes the agent's name and style, not the model. There is no per-person default; people can switch a thread's model with `!model` or `!provider`, or pick another agent.
- **Custom agents:** a named @handle with a provider and optional model, skillset (its instructions), machine size, thinking level, display name, response style, and integrations. Admins build them on the Agents page or with `nori-sessions custom-agents add`. People use them by @handle in Slack, in the chat picker, or by assigning them to automations and projects.
- **Org rules for every session:** put them in the org sessions skillset's `AGENTS.md` and upload it (admin, or an approved `!admin`); machines provisioned after the upload get it, not running sessions. Memories are searched on demand and are not rules every session follows.

## Dashboard

- Areas: Chats (Following, Yours, Archived, and All for admins), Projects, Agents (admin), Automations, Integrations, Factory (where turned on), and Settings (admin).
- **Billing:** Settings > Billing (admins; members cannot see it) or `nori-sessions billing summary`. Billing is per machine, not per seat: Team has no seat cap, Developer is one person. Owners change the plan; admins can open the billing portal.
- **Custom views:** where the org has custom views turned on, a person can ask the agent to build their own home page view.

## Deployment and security

- Each hosted org gets its own single-tenant Nori deployment at its own `<org>.norisessions.com` address, isolated from other customers. One machine serves one session.
- Admins control integrations, credentials, and privileged actions; chats are kept as transcripts.
- **Own cloud:** a dedicated deployment in the customer's own AWS account is possible by contacting Nori (jiro.bot's Enterprise plan lists bring-your-own compute); it is not a self-serve setting. Other clouds and on-premises deployment are not documented. Do not say which parts of Nori would run inside the customer's account; that is agreed with Nori.
- **Certifications:** no compliance certification (such as SOC 2) is claimed on Nori's sites. Send security reviews, data retention, and compliance questions to Nori.

## Not possible or not supported

- Keeping a machine or its non-git files after release; seeing one chat's files from another chat.
- Public, unauthenticated preview links.
- Cron jobs or long sleeps on the machine as a scheduler.
- Members changing org defaults, the setup script, billing, or org-wide integrations, or creating custom agents, without an admin.
- Setting `GH_TOKEN`, `GITHUB_TOKEN`, or other reserved names as custom env vars.
- Making integration or setup changes appear in a chat that is already running.
