# Sources and compatibility record

Reference review: 2026-10-15 UTC. These links establish the platform behavior, not the truth of fictional biographies or a certification of this fan pack.

## Hermes: official documentation and implementation

- [Profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles): separate profile state; profile homes versus host/tool access.
- [Profile distributions](https://hermes-agent.nousresearch.com/docs/user-guide/profile-distributions): local-directory and Git installation, manifest, ownership, user data exclusions, config preservation.
- [Profile commands](https://hermes-agent.nousresearch.com/docs/reference/profile-commands): install/update flags, describe `--text`, explicit `-p` selection.
- [Skins](https://hermes-agent.nousresearch.com/docs/user-guide/features/skins): documented colors, spinner, branding, default inheritance.
- [Bot Mode](https://hermes-agent.nousresearch.com/docs/user-guide/bot-mode): conditional messaging/canonical-chat behavior; a distribution alone does not create the runtime surface.
- [Official manifest implementation at the reviewed commit](https://github.com/NousResearch/hermes-agent/blob/7bda2a3368024f7ae1c70cef16583e7c2c891674/hermes_cli/profile_distribution.py): `DistributionManifest`, `read_manifest`, requirement checks, and distribution ownership parsing. This source was read, not installed as a full runtime in the build environment.

The [teknium1 Star Trek profiles](https://github.com/teknium1/hermes-star-trek-profiles) collection is the user-supplied structural/persona-design reference: separate character distributions, provider neutrality, and native-install delegation. It is a reference project, not a substitute for the current Hermes contract. This release uses original implementation and personality prose, not copied Star Trek material. Its historical caveats about old Hermes releases are not assumed to describe current Hermes unchanged.

## Grok Bot: official app docs and example roles

- [Overview](https://docs.x.ai/grok-bot/overview)
- [Create/manage/share Bots](https://docs.x.ai/grok-bot/bots)
- [Official use-case examples](https://docs.x.ai/grok-bot/use-cases): Chief of Staff, Product Performance, Bug Reproduction, and other bounded role examples.
- [Computer and apps](https://docs.x.ai/grok-bot/computer-and-apps)
- [Approvals/security/privacy](https://docs.x.ai/grok-bot/approvals-security-and-privacy)
- [Messaging and collaboration](https://docs.x.ai/grok-bot/chat-and-collaboration)
- [Skills and routines](https://docs.x.ai/grok-bot/skills-routines-and-automations)

The reviewed creation docs describe editable profile fields and app-created template links. No official standalone Grok profile repository, public profile-file import schema, or native import CLI was established by this review. The Grok files are consequently labeled authoring cards. A live app check is required to verify saved-field limits, persistence, and sharing. No third-party “GrokBot” wrapper is represented as official.

## Original source cards

The six screenshots supplied by the user are the sole source of the baseline labels in BASELINE.md. They are not redistributed. Any practical specialty, workflow, humor style, or collaboration role beyond those labels is explicitly this pack's creative adaptation. In particular, ULTRON originally has only one label: Asshole.

## CI dependency

The optional GitHub workflow uses official `actions/checkout` pinned to the verified v4.2.2 commit `11bd71901bbe5b1630ceea73d27597364c9af683`, read-only repository permission, and no persisted checkout credential. It does not use a project credential or a live model. PyYAML is pinned in requirements-dev.txt for schema tests only.
