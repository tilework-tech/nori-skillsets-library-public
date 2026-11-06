# nori-skillsets-library-public

Nori's public skillsets in the [nori-skillsets v2](https://github.com/tilework-tech/nori-skillsets-v2)
repository format. When an org has the `skillsets-v2` flag on, Nori Sessions layers
`sessions-platform` from this repository at `$HOME`.

The repository is private for now and will be made public later.

## Where the content comes from

This repository is published by CI. Do not edit `skillsets/` by hand.

| Skillset | Source folder in `nori-sessions` | Same version as v1 package |
|---|---|---|
| `sessions-platform` | `broker/server/skillset-seeds/skillset-template-platform/` | `public/sessions-platform` |
| `sessions-template` | `broker/server/skillset-seeds/skillset-template-org/` | `public/sessions-template` |
| `sessions-onboarding` | `broker/server/skillset-seeds/skillset-onboarding/` | `public/sessions-onboarding` |
| `sessions-coordinator` | `broker/server/skillset-seeds/skillset-coordinator/` | `public/sessions-coordinator` |
| `none` | `broker/server/skillset-seeds/skillset-none/` | `public/none` |

The `nori-sessions` publish job uploads each seed folder to the v1 registry (noriskillsets.dev),
then publishes the same folder here with the version v1 just assigned. Shared skills a seed
depends on, such as `creating-skills`, are fetched from the v1 registry and included in the
skillset's own `skills/`. Release tags (`skillsets/<name>@<version>`) are never moved or deleted.

## Added by hand

These skillsets are not published by CI. Each was added by pull request and released by its own tag.

| Skillset | Notes |
|---|---|
| `high-autonomy` | Converted from v1 `public/high-autonomy` 2.0.11 |
| `selberg-conversation-alpha` | Experimental. Spoken ElevenLabs clips for the agent's questions in Slack. Inert without `ELEVENLABS_API_KEY` and `SELBERG_CONVERSATION_MODE=on` |
| `high-autonomy-selberg` | `high-autonomy` plus the `stating-claims` skill: big answers open with a numbered 🟢/🟠/❓/💥 claims list; reply `check 2, 4` to verify |

## Sync and parity

`scripts/skillsets-library/sync.sh` in `nori-sessions` does the publishing. For each skillset it:

1. converts the seed folder to a v2 skillset (v2 `nori.json`; `AGENTS.md` and `skills/` unchanged);
2. compiles it with both the v1 and v2 clients and requires the same skills, byte for byte, and
   the same instructions; anything else fails the run and publishes nothing;
3. commits, pushes `main`, and pushes a release tag for each new version.

Each client's own additions are not compared: v1's `nori-info` skill and generated skills index,
and v2's `nori-skillsets` skill.
