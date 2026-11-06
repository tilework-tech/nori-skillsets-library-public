---
name: speaking-questions
description: Use in Slack before sending a final reply that asks the user one or more questions - generates one labelled spoken MP3 per question with ElevenLabs and uploads them into the thread.
---

<required>
CRITICAL: Add the following steps to your task tracker: TaskCreate (claude), update_plan (codex), etc.

1. Check the preconditions.
2. Run `speak_questions.py` once on the final draft reply.
3. Finish the reply based on the script's result.
<system-reminder> Run the script at most once per reply. A retry would post duplicate clips into the thread. </system-reminder>
</required>

# Steps

1. Check the preconditions.

Both must hold, otherwise skip this skill and send the reply as normal:
- The conversation is in Slack and a human is reading.
- The final draft reply asks the user at least one question.

The script checks the `SELBERG_CONVERSATION_MODE` kill switch itself.

2. Run the script on the final draft reply.

Write the exact reply text you will send to a new file under `$(mktemp -d)` with the Write tool. Do not inline the reply into a shell heredoc or argument. Use the Slack channel ID and the root thread ts from the conversation context (the `p…` part of the conversation link, with a dot inserted six digits from the end).

```bash
for f in ~/.nori/env.d/*.sh; do source "$f"; done
python3 {{skills_dir}}/speaking-questions/speak_questions.py \
  --out-dir "$(mktemp -d)" --channel CHANNEL_ID --thread-ts ROOT_TS < DRAFT_FILE
```

The script:
- makes one `claude -p` call (Claude Haiku) that rewrites each question for listening, with up to five sentences of context;
- voices every question with ElevenLabs in parallel, dropping to one at a time if the account's concurrency limit is hit;
- uploads `question-1.mp3`, `question-2.mp3`, … into the thread in order, titled `Question 1`, `Question 2`, …, each spoken clip opening with "Question one", "Question two", …;
- caps output at 10 clips.

It prints `{"clips": [...], "skipped": ...}`. Exit 0: every clip it produced was posted, or there was nothing to do (`skipped` set, or no questions found). Exit 1: some clips failed (each failed clip has an `error`). Exit 2: nothing was generated (missing key or LLM failure; see stderr).

3. Finish the reply.

- Exit 0: send the text reply unchanged. Do not mention or link the clips; they are already in the thread.
- Exit 1: send the text reply and add one line naming the failed clips, e.g. `(Audio for question 2 failed.)`.
- Exit 2: send the text reply and add `(Audio unavailable this time.)`.

# Configuration

Set as Nori custom env vars (for example `ELEVENLABS_API_KEY` at org scope and `SELBERG_CONVERSATION_MODE` at personal scope), never in this skillset:

| Variable | Default | Notes |
|---|---|---|
| `SELBERG_CONVERSATION_MODE` | unset | Must be `on`; kill switch |
| `ELEVENLABS_API_KEY` | — | Required |
| `ELEVENLABS_VOICE_ID` | `21m00Tcm4TlvDq8ikWAM` (Rachel) | |
| `ELEVENLABS_MODEL_ID` | `eleven_flash_v2_5` | |
| `SELBERG_TTS_CONCURRENCY` | `4` | Parallel ElevenLabs requests |
| `SELBERG_LLM_MODEL` | `claude-haiku-5-5` | Uses the session's Claude login |
