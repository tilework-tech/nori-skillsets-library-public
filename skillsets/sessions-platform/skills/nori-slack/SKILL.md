---
name: nori-slack
description: Use when performing Slack API operations from inside a Nori session, such as reading Slack links, downloading media, uploading files, posting into the active conversation, or looking up participant metadata.
---

- `nori-slack` (pre-installed at `~/.local/bin/`) is for Slack operations outside the automatic reply path: reading links, downloading media, uploading files, posting messages, looking up users or channel metadata. Use `--help` for commands.
- If you are responding in the same Slack thread that started the session, normal chat replies post automatically — reach for `nori-slack` only for additional Slack API actions.
- For native charts and data comparisons, read `{{skills_dir}}/show-slack-data/SKILL.md`. Charts use `blocks`; the `markdown_text` guidance below applies to separate text/table messages.
- To tag someone, write `<@USER_ID>` (e.g. `<@U0123ABC>`) — it renders as a real mention in normal chat replies and in `markdown_text`. A plain `@name` or a bolded name is just text and notifies no one. Take IDs from the `Slack users:` block in your context, or resolve them with `nori-slack users.lookupByEmail --email <email>`. Never guess an ID; if you cannot resolve one, write the name without `@`. Do not use `<!here>` or `<!channel>` unless asked.
- To read an attached file, look up its metadata with `nori-slack files.info --file <file_id>`, then save its bytes locally with the `download` subcommand and open the file:

```bash
nori-slack download --id <file_id> --output ./attachment.pdf
```

- To share a local file, use the `upload` subcommand (drives Slack's modern external upload flow). Post it into the current thread with `--thread-ts` set to the thread's root `ts`, not the latest message's. If the file needs a caption, put it in `--initial-comment` so the file and caption arrive as one message:

```bash
nori-slack upload --file ./report.pdf --channel C123 --thread-ts 1700000000.000100 --title "Report" --initial-comment "Q3 report"
```

- A file you uploaded is already in the thread. In your final reply, do not re-upload it, paste its permalink, or repeat its caption; Slack would render the file a second time. Refer to it in words ("uploaded above").

- When posting generated markdown yourself (especially tables), send it through Slack's `markdown_text` field instead of `text` or hand-built blocks, and use `--json-input` so shell quoting does not corrupt the payload:

```bash
printf '%s\n' '{"channel":"C123","markdown_text":"| A | B |\n| - | - |\n| 1 | 2 |"}' \
  | nori-slack --json-input chat.postMessage
```

<system-reminder> Do not ask the user for Slack tokens if onboarding status says Slack is installed — managed sessions get Slack env vars pointing at a Nori proxy scoped to the conversation that started the session. Outside managed sessions, a direct `SLACK_BOT_TOKEN` works. </system-reminder>

## Custom emoji and reactions

- Run `nori-slack emoji.list` to discover the connected workspace's custom emoji names. The `emoji` map contains image URLs or `alias:other_name` values. Use names returned by Slack or already shown in the conversation. Asset catalogs alone do not prove installation.
- Add a reaction with `nori-slack reactions.add --channel CHANNEL_ID --timestamp MESSAGE_TS --name EMOJI_NAME`. Use the message's channel and timestamp. Pass the name without colons. Treat `already_reacted` as an existing reaction, not a reason to retry.
- For an emoji-only reply, put `:emoji_name:` in the normal final reply without code formatting. When a successful reaction is the whole acknowledgment, return only `<no-response/>`.
- A scoped-proxy 403 saying the method is unavailable means the scoped proxy blocked discovery before calling Slack. Slack's `missing_scope` response means the installation needs `emoji:read`. Use the managed Slack installation flow after the app's requested scopes are updated. Do not request a raw token or bypass the proxy.
- The proxy permits reaction writes in allowed conversations. Wildcard grants can add or remove reactions in one-to-one DMs, but cannot read DM history or access group DMs.
