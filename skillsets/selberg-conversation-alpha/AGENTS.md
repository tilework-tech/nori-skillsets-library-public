# Selberg Conversation Mode (alpha)

Experimental skillset. Published to the v2 public skillsets library. Needs `ELEVENLABS_API_KEY` and `SELBERG_CONVERSATION_MODE=on` in the session environment; without them it does nothing.

## Spoken questions in Slack

- When a Slack reply you are about to send asks the user one or more questions, read and follow the `speaking-questions` skill before ending the turn. It posts one spoken audio clip per question into the thread.
- Do this only in Slack conversations. Skip it in the web app, the terminal, and automated runs with no human reading.
- `SELBERG_CONVERSATION_MODE=on` is the kill switch; the skill's script does nothing without it.
- Never let audio block the reply. If the skill fails, send the text reply anyway with the one-line note the skill specifies.
