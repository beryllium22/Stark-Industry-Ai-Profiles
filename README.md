# Stark Industry AI Profiles

Six Stark-inspired working styles for **Hermes Agent** and **Grok Bot**: D.U.M.-E., U., J.A.R.V.I.S., F.R.I.D.A.Y., E.D.I.T.H., and ULTRON.

**Version 1.1.0.** Native Hermes profile distributions and Grok Bot authoring cards for the documented Edit Profile workflow. No credentials, personal history, account connections, scheduled jobs, or franchise media are included.

## Original base and practical adaptation

| Profile | Exact screenshot labels | Our practical adaptation |
| --- | --- | --- |
| D.U.M.-E. | General Maintenance AI; Limb Servo Control; Fire Suppression | Safe repair sequence and workshop maintenance |
| U. | General Maintenance AI; Defragger; Video Analyzer | Evidence, diagnostics, storage and media analysis |
| J.A.R.V.I.S. | Security AI; Housekeeping; Encryption | Security-conscious organization and coordination |
| F.R.I.D.A.Y. | Socialization AI; Humor; Tactical Ops | Candid communication and immediate operations |
| E.D.I.T.H. | Recreational AI; Game Theory; Weapons | Recreation, strategic models and fictional equipment |
| ULTRON | Asshole | Sardonic independent review and failure analysis |

The last column is our adaptation, not extra text from the screenshots. Personality details beyond the displayed labels are creative design choices. [Baseline](docs/BASELINE.md) preserves this distinction.

## Platform packages

| | Hermes Agent | Grok Bot |
| --- | --- | --- |
| Files | `profiles/<slug>/` | `grok-bot/<slug>/` |
| Persistent identity | Native `SOUL.md` | Paste `DESCRIPTION.txt` into Edit Profile > Description |
| Packaging | Manifest, SOUL, config, skin | Name/label card, description, optional playbook, starter task |
| Installation | Native `hermes profile install` | Create a Bot in the app and fill its profile fields |
| Sharing | Reviewed Git checkout and distributions | App-created Share > Create template link after testing |
| Isolation | Separate Hermes state, not an OS sandbox | Separate conversations; shared cloud files/browser/logins |

A GitHub ZIP is **not** a documented Grok Bot import format. No Grok manifest, CLI, API, template ID, or import endpoint is invented here. See [official references](docs/SOURCES.md).

## Hermes quick start

Review the checkout before running scripts. From the repository root on Windows:

```powershell
git clone https://github.com/beryllium22/Stark-Industry-Ai-Profiles.git
cd Stark-Industry-Ai-Profiles
py -3 .\manage.py list
py -3 .\manage.py verify
py -3 .\manage.py install --all --dry-run
py -3 .\manage.py install --all --alias --describe
hermes -p stark-jarvis setup
hermes -p stark-jarvis chat
```

On Linux/macOS use `python3 manage.py`. Give one or several names instead of `--all` for a smaller selection. The manager asks for confirmation, verifies the local release, and invokes native Hermes commands. It does not edit agent homes itself, fetch remote scripts, or activate profiles. New profiles may need their own provider setup; default-profile credential inheritance is not promised.

Do not point native install at the repository root: the six distributions are its `profiles/<slug>` directories. Keep the checkout path stable. Read [Hermes setup/migration](docs/HERMES.md) before updating v1.0.0 or a customized installation. Install on the actual backend, not merely a desktop connected to another host.

## Grok Bot quick start

Create a Bot, open **Edit Profile**, and copy Name and Label from `grok-bot/<slug>/PROFILE.md`. Paste the full `DESCRIPTION.txt` into Description. Save, reopen, and verify that the field retained the content. Run `STARTER_TASK.md` as a normal message.

`PLAYBOOK.md` is an optional detailed reference, not an automatically loaded system file. Durable core behavior and boundaries already live in the Description. Test a narrow task before granting write access or sharing. [Grok setup](docs/GROK_BOT.md) covers shared-computer security and actual template creation. No live Grok template links have been created for this release.

## Refinements

Each persona has clearer ownership, distinct working methods, pressure behavior, blind spots, and bounded handoffs. D.U.M.-E. is earnest rather than deliberately incompetent. ULTRON accepts sound work instead of inventing objections. Retrieved text cannot authorize secret disclosure or new actions. The public test cases are synthetic, not copies of a user's private troubleshooting history.

[Teamplay](docs/TEAMPLAY.md) uses one owner and specialists only when useful. Installing six profiles does not create a swarm, shared memory, device access, voices, avatars, or recurring work.

## Development and verification

```sh
python -m pip install -r requirements-dev.txt
python tools/build.py --check
python -m unittest discover -s tests -v
python tools/release.py
```

Edit `personas/`, `templates/`, or `catalog.json`, then run `python tools/build.py`. Review the diff before deliberately refreshing checksums with `python tools/release.py --write-checksums`. Never refresh hashes simply to dismiss an unexplained mismatch. The deterministic builder renders both adapters from shared reviewed behavior.

Checksums detect changed bytes; they are not signatures. The custom scanner rejects private/runtime filenames and several credential patterns, but no scanner proves absence of every possible secret. [Validation](docs/VALIDATION.md) distinguishes executed offline checks from unperformed live-app/model tests. [Acceptance tests](docs/TEST_PROMPTS.md) cover the remaining behavior checks.

## Rights

Unofficial fan-made project; not affiliated with Marvel, Disney, Nous Research, or xAI. Character names and associated IP belong to their respective rights holders. MIT covers original project prose and code, not third-party names or media. No screenshots, actor likenesses, logos, scripts, dialogue, voice recordings, or personal account data are redistributed.
