---
name: nori-sessions-upload
description: Use after editing the org sessions skillset when changes need to be uploaded to the org's private registry so future Nori sessions receive them.
---

<required>
- After editing anything in the org sessions skillset, run `nori-sessions-upload.sh` to publish to the org's private registry. The current session already uses the files on disk; uploading is what makes future sessions receive them.
- Use the wrapper, never `sks upload` directly. It refuses to run when `NORI_ORG` is unset, refuses the public registry, and only accepts simple private org slugs.
</required>

<system-reminder> During first-run onboarding, upload the completed skillset BEFORE running `nori-sessions onboarding complete`. </system-reminder>
