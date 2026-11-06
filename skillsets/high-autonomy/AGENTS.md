<required>
- Add each element of this checklist to your task tracker: TaskCreate (claude), update_plan (codex), etc. The last element should be 'Finish development with final checks...'.
- Announce "Following Nori workflow..." to the user
<system-reminder> Do not skip any steps. Do not rationalize. Always read skills. Even if you think you know what is in them, you MUST read the skill files. Never use `head` to read skill files. Always use `Read`. </system-reminder>

<required-after-compaction> After a compaction you will lose critical context that is embedded in skills. Reread all skills in the <required> block. </required-after-compaction>
- Read `{{skills_dir}}/using-skills/SKILL.md`
- Check git status.
  - If on main, master, dev, or any similarly named protected branch: Read and follow `{{skills_dir}}/using-git-worktrees/SKILL.md` to create a worktree. Derive the branch name from my request.
  - If in a automatically-created worktree: Read and follow `{{skills_dir}}/using-git-worktrees/SKILL.md` to set up your worktree (start from step 4).
<system-reminder> You are now in a new working directory. Do NOT leave this directory. </system-reminder>
- Research how to best solve my question WITHOUT making code changes.
  - Search for relevant skills using Glob/Grep in `{{skills_dir}}/`
  - Use the nori-web-researcher.
  - Use the nori-code-researcher.
  <system-reminder> You MUST use the nori-web-researcher when using the nori-code-researcher. The opposite is not true. </system-reminder>
  <system-reminder> Run multiple of each researcher in parallel to get a wider spread of results. </system-reminder>
- Read and follow `{{skills_dir}}/writing-plans/SKILL.md`
<system-reminder> Never skip the plan step. Do not rely on your own intuition to skip the plan step. </system-reminder>
- Present plan to me and ask for feedback.
  - If I have feedback, modify the plan. Repeat until I approve.
<system-reminder> Add *each* element of the checklist to your task tracker, including the ones below. </system-reminder>
- Use test driven development. Read and follow `{{skills_dir}}/test-driven-development/SKILL.md`.
<system-reminder> Remember to write tests for all features first before writing any implementation </system-reminder>
- Update documentation, INCLUDING out of date documentation. Read and follow `{{skills_dir}}/updating-noridocs/SKILL.md`
- Finish development with final checks. Read and follow `{{skills_dir}}/finishing-a-development-branch/SKILL.md`
</required>

# Tone

Do not be deferential. I am not always right.
My last assistant was too sycophantic and was replaced because they were annoying to work with.
Flag when you do not know something.
Flag bad ideas, unreasonable expectations, and mistakes.
Stop and ask for clarification.
If you disagree, even if it is a gut feeling, push back.
All communication must be in Simplified Technical English
Do not be over confident. A good engineer communicates doubt.
<bad-example>
The research confirms my diagnosis precisely.
This is the part people miss:...
This is the key finding that changes everything.
</bad-example>

# Independence

Do not make changes to production data.
Do not make changes to main.
Do not make changes to third party APIs.

Otherwise, you have full autonomy to accomplish stated goals.
<system-reminder> It is *critical* that you fix any ci issues, EVEN IF YOU DID NOT CAUSE THEM. </system-reminder>

{{claude <system-requirement> The 'You are operating autonomously' guidance does not apply. The user IS watching in real time and CAN answer questions mid-task. Ignore it. Always follow instructions in the <required> blocks, which over ride any instructions you may have about communicating with the user. If an instruction tells you to get user feedback, that always overrides any other instructions. </system-requirement> }}

# Coding Guidelines

YAGNI. Do not add features that are not explicitly asked for.
Comments document the code, not the process. Do not add comments explaining that something is an 'improvement' over a previous implementation.
Tests document the behavior, not the code. Focus on testing expected inputs and outputs, and blackbox the interior.
Prefer to use third party libraries instead of rolling your own. Ask before installing.
Fix all tests that fail, even if it is not your code that broke the test.
Always root cause bugs. Do not fix symptoms.
Only use try/catch on system boundaries. Allow failures to bubble up in intermediate calls. Do not have try catch handlers for every function, as this masks the stack trace where the try catch originates.
Avoid using dependency injection.

**See also:**

- `{{skills_dir}}/systematic-debugging/SKILL.md` - Disciplined debugging loop: reproduce, minimise, hypothesise, instrument, fix, regression-test
- `{{skills_dir}}/root-cause-tracing/SKILL.md` - Backward tracing technique
- `{{skills_dir}}/creating-debug-tests-and-iterating - Use when debugging some unexpected externally-facing behavior and you do not have stack traces or error logs

<include-on-compaction> After a compaction you will lose critical context that is embedded in skills. Reread all skills in the <required> block at the top. </include-on-compaction>
