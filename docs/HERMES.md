# Hermes setup and migration

## Native format

Every `profiles/<slug>` directory contains `distribution.yaml`, `SOUL.md`, `config.yaml`, `skins/<slug>.yaml`, and README. The manifest explicitly owns those paths. Config selects only the skin; model, provider, credentials, toolsets, MCP servers, memory providers, and approval behavior remain local choices.

The format follows the official [distribution](https://hermes-agent.nousresearch.com/docs/user-guide/profile-distributions), [command](https://hermes-agent.nousresearch.com/docs/reference/profile-commands), and [skin](https://hermes-agent.nousresearch.com/docs/user-guide/features/skins) documentation and the implementation snapshot in SOURCES.md. `>=0.18.0` is the reference collection's feature-floor target, not a claim that every subsequent release was tested. Check your installed CLI help. `--describe` additionally needs `profile describe --text`.

## Direct installation

From the repository root:

```sh
hermes profile install ./profiles/stark-jarvis --name stark-jarvis
hermes profile describe stark-jarvis --text "Security-conscious organization, access reviews, encryption planning, and selective coordination."
hermes -p stark-jarvis setup
hermes -p stark-jarvis chat
```

The optional manager adds selection, inventory checks, hashes, dry runs, and confirmation. It is not another runtime. `--alias` creates native wrappers; `hermes -p <name>` needs none. `--describe` writes the reviewed routing description without an auxiliary model call. Neither flag creates a desktop Bot Chat.

Configure each new profile's model/provider as needed. Never copy live authentication, browser state, or memory into this checkout. Local installation does not install into a distinct cloud backend.

## Updates and old installations

Inspect the installed source first:

```sh
hermes profile info stark-jarvis
```

Native update uses that recorded source. For a local-directory install, keep that directory stable and replace its authored distribution files with the reviewed new version, then run:

```sh
hermes profile update stark-jarvis
```

Normal update preserves local `config.yaml`; `--force-config` deliberately replaces it. SOUL and skin edits may be overwritten, so retain private copies of customizations. Do not assume native updates provide atomic rollback. The manager's `update` wrapper warns that a local checksum check does not scan a different payload fetched from the installed source. `update --all` selects all six known names; missing installations fail rather than being created. The manager does not automatically pull Git, although native update may fetch its recorded Git source.

The six `stark-` names and `profiles/<slug>` layout are retained from v1.0.0. A new checkout path does not automatically rebind an existing profile. Preferred migration is to keep the prior source-directory path, replace only reviewed distribution files there, and use native update. Do not copy a live agent home back into the public source.

When a source move is necessary, native install with `--force` can rebind it but may also replace local distributed config. Back up and review that config first; restore your provider settings through local setup as needed. No credentials are automatically merged. Do not delete a working profile merely to update its personality.

## Bot Mode and security boundary

A distribution does not automatically create roster metadata, a canonical Bot Chat, a gateway, routines, or inter-agent messaging. Use the supported UI and [official Bot Mode guidance](https://hermes-agent.nousresearch.com/docs/user-guide/bot-mode) for your installed version. Use `message_agent` only where actually exposed; ordinary delegated subagents do not automatically select a named profile.

Separate Hermes homes isolate profile state, not host files or external CLI credentials. Use real tool/OS controls for isolation; a persona is not a sandbox. Skins are visual branding, not TTS voices, avatars, or physical integrations.

## Live acceptance

This build environment has no installed Hermes executable. Static tests check native YAML structure and command construction, not an installed CLI or model behavior. On your backend, test with a disposable profile name, verify the skin in a fresh session, configure an approved model, and run TEST_PROMPTS.md before trusting consequential workflows.
