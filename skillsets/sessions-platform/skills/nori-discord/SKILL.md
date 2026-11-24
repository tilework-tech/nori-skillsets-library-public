---
name: nori-discord
description: Use when acting in the Discord thread that started a Nori session beyond the automatic reply - reading earlier messages in the thread or its parent channel, opening a pasted Discord message link, reacting, uploading or downloading files, or looking up who is in the thread.
---

- `nori-discord` (pre-installed at `~/.local/bin/`) reaches only the Discord thread this session serves, plus read-only access to the channel that thread was opened in, through a Nori proxy. Posting and uploading always go to the thread, and reactions go on thread messages (or the message that opened it). Other channels cannot be read, even with a link. The bot token never reaches this machine. Its token and endpoint are in `~/.nori/env.d/discord-conversation.sh`, which shells load on start; if a command says there is no token, run `source ~/.nori/env.d/discord-conversation.sh` in the same command. The file exists only in sessions started from Discord.
- Your final reply posts itself into the thread. Use `nori-discord` only for anything extra, and do not repeat in the final reply what you already posted or uploaded.
- Every command prints one JSON line. When a response leaves something out (an older page, an attachment, people beyond the scanned messages), its `tips` array gives the exact command that gets it; run that instead of guessing flags. Run `nori-discord` alone for the command list and `--help` on any command for its options.

```bash
nori-discord history --limit 50            # oldest first, 1-100; page back with --before <oldest-id> (see tips)
nori-discord participants                  # people who wrote in the latest 100 thread messages
nori-discord channel-history --around <thread-id>  # parent channel around where the thread opened (read-only)
nori-discord channel-history --limit 20    # newest parent-channel messages; page with --before/--after (see tips)
nori-discord get-message --message https://discord.com/channels/<server>/<channel>/<message>  # a pasted link, or an id
nori-discord react --message <message-id> --emoji 👀
nori-discord post --text "Extra update" --reply-to <message-id>
nori-discord post --text-file ./summary.md # long text is split into Discord-sized messages
nori-discord upload --file ./report.pdf --comment "Q3 report"
nori-discord download --message <message-id> --attachment <attachment-id> --output ./report.pdf
```

- When a thread was started from a message, that opening message lives in the parent channel and shares the thread's id; `history` already includes it, so use `channel-history` for what came before it. A forum post or a channel that is not a thread has no parent to read; `history` says so in its tips.
- `channel-history` refused with `parent_not_readable` means the bot lacks access to that channel; tell the user rather than retrying.
- `history` lists each message's attachments by `id`; pass that id and the message id to `download`. Do not fetch Discord CDN links directly; they expire.
- To mention someone, write `<@USER_ID>` with an id from `history` or `participants`. Posts never ping `@everyone`, `@here`, or roles.
- For a custom emoji, pass `name:id` (for example `jiro:123456789012345678`). Use only emoji already shown in the thread or that someone named.
- Uploads go up to 10 MB, the limit of a server without boosts.
- A `503` means Discord is not connected to Nori right now; tell the user rather than retrying in a loop. Do not ask the user for a Discord bot token.
