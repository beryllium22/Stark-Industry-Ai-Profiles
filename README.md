# Stark Industry AI Profiles

Six Stark-inspired profiles for **Hermes Agent** and **Grok Bot**. **Profile pack 1.1.1.** No build step, management scripts, or custom installer is required.

## Choose a profile

| Name | Folder | Original screenshot labels | Grok Label |
| --- | --- | --- | --- |
| D.U.M.-E. | `stark-dum-e` | General Maintenance AI; Limb Servo Control; Fire Suppression | Maintenance & workshop |
| U. | `stark-u` | General Maintenance AI; Defragger; Video Analyzer | Diagnostics & media |
| J.A.R.V.I.S. | `stark-jarvis` | Security AI; Housekeeping; Encryption | Security & organization |
| F.R.I.D.A.Y. | `stark-friday` | Socialization AI; Humor; Tactical Ops | Communication & operations |
| E.D.I.T.H. | `stark-edith` | Recreational AI; Game Theory; Weapons | Games & simulation |
| ULTRON | `stark-ultron` | Asshole | Adversarial review |

The screenshot labels are the original base. Practical roles and personality details are adaptations; ULTRON originally had only the single label shown above. No screenshots or franchise media are included.

## Hermes Agent

Each folder in [profiles/](profiles/) is an independent native distribution:

```text
profiles/<name>/
  SOUL.md                 Personality, workflow, and boundaries
  distribution.yaml       Native distribution manifest
  config.yaml             Skin selection; no model or credentials
  skins/<name>.yaml       Terminal appearance
```

Clone or extract this repository to a stable location. From its root, install a profile using Hermes itself:

```sh
hermes profile install ./profiles/stark-jarvis --name stark-jarvis
hermes -p stark-jarvis setup
hermes -p stark-jarvis chat
```

Replace `stark-jarvis` with the desired folder name. Install on the actual Hermes backend, not just a desktop connected to it. Do not install the repository root as one distribution. The manifests target Hermes `>=0.18.0`; check your installed CLI's support. Configure a provider and model for each new profile as needed.

**Updates:** inspect the recorded source with `hermes profile info stark-jarvis`, review changes at that source, then run `hermes profile update stark-jarvis`. Keep the source path stable. Normal updates preserve local config but replace distributed personality files. Back up customizations before updating; use forced installation or `--force-config` only when deliberately resetting configuration.

## Grok Bot

Each folder in [grok-bot/](grok-bot/) contains:

- **`DESCRIPTION.txt`** — paste the complete text into **Edit Profile > Description**. Use the Name and Grok Label from the table above. Save and reopen the field to verify the text was retained.
- **`PLAYBOOK.md`** — the complete personality and working method. Attach it when extended task guidance is useful; it does not load automatically or replace the saved Description.

These are profile-authoring files, **not a native import archive**. Create the Bot through the app. To share an app template, test the saved profile, use **Share > Create template**, and inspect the shared fields for private data. This repository does not supply app-created template links.

## Scope

No credentials, account configuration, memories, sessions, routines, or personal history are included. Keep live agent homes and login data outside this checkout. Hermes profile state is separate but not an OS sandbox; Grok Bots share their account's cloud computer and logins. Personality instructions do not grant permissions or create collaboration, voices, avatars, or device access.

Live Hermes installation, Grok field persistence, and model behavior have not been verified for this pack. Test each profile in your own runtime before relying on it or connecting sensitive resources.

## Sources and license

Official references: Hermes [profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles), [distributions](https://hermes-agent.nousresearch.com/docs/user-guide/profile-distributions), and [skins](https://hermes-agent.nousresearch.com/docs/user-guide/features/skins); Grok Bot [profile creation](https://docs.x.ai/grok-bot/bots), [use cases](https://docs.x.ai/grok-bot/use-cases), and [shared computer](https://docs.x.ai/grok-bot/computer-and-apps). The [Star Trek profile collection](https://github.com/teknium1/hermes-star-trek-profiles) provided structural inspiration.

Unofficial fan-made project, not affiliated with Marvel, Disney, Nous Research, or xAI. Character names and associated rights belong to their respective owners. The [MIT license](LICENSE) covers original project content, not third-party intellectual property.
