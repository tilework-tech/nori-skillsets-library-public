# nori-skillsets-library-public

Nori's public skillsets in the [nori-skillsets v2](https://github.com/tilework-tech/nori-skillsets-v2)
repository format. When an org has the `skillsets-v2` flag on, Nori Sessions layers
`sessions-platform` from this repository at `$HOME`.

The repository is private for now and will be made public later.

## Where the content comes from

This repository is a mirror. Do not edit `skillsets/` by hand.

| Skillset | v1 package (what sessions download today) | Written in |
|---|---|---|
| `sessions-platform` | `public/sessions-platform` on noriskillsets.dev | `nori-sessions`: `broker/server/skillset-seeds/skillset-template-platform/` |
| `sessions-template` | `public/sessions-template` | `skillset-seeds/skillset-template-org/` |
| `sessions-onboarding` | `public/sessions-onboarding` | `skillset-seeds/skillset-onboarding/` |
| `sessions-coordinator` | `public/sessions-coordinator` | `skillset-seeds/skillset-coordinator/` |
| `none` | `public/none` | `skillset-seeds/skillset-none/` |

Each skillset is copied from the v1 package that the public registry serves, not from the seed
folder. A skill only reaches this repository once the v1 registry serves it, so skills awaiting
review on the registry are left out here too. Shared v1 dependencies such as `creating-skills`
are copied into the skillset's own `skills/`.

Versions match v1: `skillsets/<name>@<version>` is the same content as v1 `public/<name>@<version>`.
Release tags are never moved or deleted.

## Sync and parity

`scripts/skillsets-library/sync.sh` in `nori-sessions` does the mirroring. For each skillset it:

1. downloads the v1 package anonymously, as a session does;
2. writes the v2 skillset (v2 `nori.json`; `AGENTS.md` and `skills/` unchanged);
3. compiles it with both clients and requires the same skills, byte for byte, and the same
   instructions; anything else fails the run and publishes nothing;
4. commits, pushes `main`, and pushes a release tag for each new version.

Each client's own additions are not compared: v1's `nori-info` skill and generated skills index,
and v2's `nori-skillsets` skill.
