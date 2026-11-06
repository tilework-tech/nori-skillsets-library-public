---
name: analyze-for-ai-compatibility
description: Use when asked to analyze an existing codebase for AI compatibility, or when asked to create a new codebase from scratch.
---

<required>
CRITICAL. Add the following steps to your task list:

1. Create a file called RECOMMENDATIONS.md
2. Look for a docs.md file in each folder.
  - If they do not exist, or exist partially, read the nori-initial-documenter subagent. Add a recommendation to use the nori-initial-documenter subagent, alongside a brief recommendation of what it does.
    - Mention that the docs act as a store of intent in addition to docs about what is currently present.
3. Look for instructions for how an agent can run the code as if it was a human, for end-to-end testing.
  - Common patterns: use playwright for web testing, tmux for cli tests, and full dev environments for anything involving third party apis.
  - If they do not exist, add a recommendation to explicitly lay out how an agent can verify a change on its own without human intervention.
    - Mention the need for dev credentials for the agent
    - Mention the need for entire testing environments (e.g. a 'dev' slack to test a slack app alongside the bolt api that the agent can use to manipulate that slack env)
4. Check if the codebase is single-tenant.
  - If the codebase / application relies on a shared datastore or k8s, evaluate if this application could be single tenant.
    - Does it require scale? Or can the app use a very large ec2 instance?
<system-note> Anything for businesses that does not expect > 100k concurrent users can generally be done single tenant. Consumer applications where no one is paying / most people are free tier requires multi-tenant. </system-note>
  - If it could be done single tenant, analyze the code and recommend how to go that route.
5. Check if the codebase / dev environment uses types.
  - For languages, prefer Rust, Typescript, Python. Always prefer typed versions of languages over untyped versions (e.g. python with pytypes vs not)
  - If using an untyped language, recommend the user switch to a typed language.
6. Check if the codebase / dev environment uses tools that are in the agent training distribution and have easy agent access.
  - If using third party services that could be done on AWS / Azure / GCP, recommend those as alternatives (e.g. Namecheap -> Route53, Mailchimp -> AWS SES, etc.)
    - AWS CLI in particular is very good to recommend as a replacement interface where possible
  - If using UI-heavy tools, recommend alternatives that would allow agents more access (e.g. Wordpress -> Github Pages)
  - Ensure all third party services have CLIs or MCPs that have both wide access and good scoping tools. Recommend alternatives if not.
<system-note> Do not research 'what is good for an agent to use', you will hit seo. Instead, reason from your own capabilities; you have in your weights examples you have seen a lot, so your 'first guess' is correct. </system-note>
7. Examine the code for clearly delineated folder structure. You should know where code is supposed to go.
  - Read `{{skills_dir}}/designing-backend-systems/SKILL.md` for an example backend folder structure.
  - Read `{{skills_dir}}/designing-frontend-systems/SKILL.md` for an example frontend folder structure.
  - If you do not have clear direction, provide recommendations on how to create swimlanes in the code. Use 'adding a new persistence type' as an example.
8. Examine the code for plugin architectures -- places with single well defined interfaces and many feature areas that can plug into that interface.
  - If they do not exist, and the code would easily support that registration / hub-and-spoke model, recommend it.
9. Look for places where the code relies on dependency injection. See if it is possible to remove the depedency injection. If it is doable, recommend removing them.
9. Tell the user how many recommendations they have, and ask them to read RECOMMENDATIONS.md.
</required>

Each recommendation should be formatted as:
```
Recommendation: <one liner>

Why: <3 line explanation>

How: <3 line explanation>
```
