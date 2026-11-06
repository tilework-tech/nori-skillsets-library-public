---
name: stating-claims
description: Use when answering a big question - one whose answer rests on several facts about code, systems, or behavior - or when I say "big question", and when I reply with "check" and claim numbers. Opens the answer with a numbered claims list that marks each claim tested, testable, untestable, or disproved.
---

<required>
CRITICAL: Add the following steps to your task tracker: TaskCreate (claude), update_plan (codex), etc.

1. Decide whether this is a big question.
2. Sort every claim the answer depends on into one of the four markers.
3. Write the numbered claims list at the very top of the reply, in the exact format below.
4. Write the rest of the answer below the list.
5. End the reply with the check prompt line.
6. If my reply asks you to check claims, run every requested check, then re-post the full claims list with updated markers.
</required>

# 1. Decide whether this is a big question

A question is big when the answer depends on several facts you could be wrong about: how code works, what a system does, whether a change is safe, or why something broke. If I say "big question", treat it as big. Skip the claims list for small talk, one-line lookups, and simple edits.

# 2. Sort the claims

List the facts the answer rests on, not every sentence. Mark each one:

| Marker | Meaning | Rule |
|---|---|---|
| 🟢 | Tested | You gathered hard proof in this conversation: a file and line you read, a command and its output, or a test run. Name the proof inline. Without proof, never use 🟢. |
| 🟠 | Testable, not yet checked | You believe it and you know an objective check that would settle it. Give every 🟠 a `Check:` sub-item. If you cannot write a concrete check, use ❓ instead. |
| ❓ | Not testable | A belief, judgment, or prediction that no check you could run would settle. |
| 💥 | Checked and false | A 🟠 whose check proved it wrong. Use it only after a re-check. |

A `Check:` names exactly what you will do: the file to read, the command or test to run, or the API to call. Pick the cheapest check that settles the claim.

# 3. Format

Start the reply with a bold `Claims` line and one numbered list. Put the marker first in each item, then the claim. Put a 🟠's check on an indented sub-bullet that starts with `Check:`.

```markdown
**Claims**
1. 🟢 Drafts persist to localStorage (`chatStore.ts:150`).
2. 🟠 Messages are immutable after streaming.
   - Check: read `finalizeTurn` in `liveConversation.ts`.
3. ❓ Most readers will not notice the difference.
4. 🟠 The flag defaults to off.
   - Check: run `bun test claims-ledger-flag.test.ts`.
```

Keep each claim to one line. Use the same text in every chat client: web, Slack, and CLI.

# 4. The rest of the answer

Write the answer below the list. Do not restate the claims.

# 5. Check prompt line

If the list has any 🟠, end the reply with this line:

```
Reply `check 2, 4` or `check all` to verify the 🟠 claims.
```

Use the real 🟠 numbers in the example.

# 6. Re-check loop

My reply asks for checks when it says `check` followed by claim numbers, `check all`, or names a claim in words. `check all` means every 🟠.

For each requested claim:

- Run its check for real. If there are several, launch one subagent per check in parallel. Have each subagent return its verdict with the proof.
- If the claim held, mark it 🟢 and name the proof.
- If the claim failed, mark it 💥 and say what you found.
- If the check cannot settle it, mark it ❓ and say why.

Then re-post the full claims list. Keep every claim's number and text. Update the markers of the checked claims and leave the rest unchanged. After the list, say what changed and whether any 💥 changes the original answer. If any 🟠 remain, end with the check prompt line again.
