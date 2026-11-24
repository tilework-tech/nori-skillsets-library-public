---
name: nori-discord
description: Use when acting in the Discord thread that started a Nori session beyond the automatic reply - reading earlier messages, reacting, uploading or downloading files, or looking up who is in the thread.
---

- `nori-discord` (pre-installed at `~/.local/bin/`) reaches only the Discord thread this session serves, through a Nori proxy. The bot token never reaches this machine. Its token and endpoint are in `~/.nori/env.d/discord-conversation.sh`, which shells load on start; if a command says there is no token, run `source ~/.nori/env.d/discord-conversation.sh` in the same command. The file exists only in sessions started from Discord.
- Your final reply posts itself into the thread. Use `nori-discord` only for anything extra, and do not repeat in the final reply what you already posted or uploaded.
- Every command prints one JSON line. When a response leaves something out (an older page, an attachment, people beyond the scanned messages), its `tips` array gives the exact command that gets it; run that instead of guessing flags. Run `nori-discord` alone for the command list and `--help` on any command for its options.

```bash
nori-discord history --limit 50            # oldest first, 1-100; page back with --before <oldest-id> (see tips)
nori-discord participants                  # people who wrote in the latest 100 thread messages
nori-discord react --message <message-id> --emoji 👀
nori-discord post --text "Extra update" --reply-to <message-id>
nori-discord post --text-file ./summary.md # long text is split into Discord-sized messages
nori-discord upload --file ./report.pdf --comment "Q3 report"
nori-discord download --message <message-id> --attachment <attachment-id> --output ./report.pdf
```

- `history` lists each message's attachments by `id`; pass that id and the message id to `download`. Do not fetch Discord CDN links directly; they expire.
- To mention someone, write `<@USER_ID>` with an id from `history` or `participants`. Posts never ping `@everyone`, `@here`, or roles.
- For a custom emoji, pass `name:id` (for example `jiro:123456789012345678`). Use only emoji already shown in the thread or that someone named.
- Uploads go up to 10 MB, the limit of a server without boosts.
- A `503` means Discord is not connected to Nori right now; tell the user rather than retrying in a loop. Do not ask the user for a Discord bot token.
