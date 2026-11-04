---
name: nori-handroll
description: Use when running, attaching to, or reasoning about the nori-handroll terminal session wrapper, including the start menu, command overlay, prefix key, attach/detach, handoff, login, and remote control.
---

- `nori-handroll` wraps agent CLIs (`nori-handroll claude|codex`) in a TUI proxy: start menu, command overlay, local attach/detach (`attach --latest`), handoff, and hook-aware session metadata. `nori-handroll login` authenticates for remote Nori Sessions operations. Use `--help` for the rest.
- The command overlay (handoff, attach, detach, remote control) opens with the prefix key: `Ctrl-B` unless `NORI_PREFIX_KEY` says otherwise.

<system-note> `--skip-menu-start` is used by session machine startup wrappers for headless launches. `--help` and `--version` pass through without opening the TUI. </system-note>
