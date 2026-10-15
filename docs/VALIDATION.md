# Validation report - v1.1.0

## Executed locally

On 2026-10-15 UTC, **49 automated tests passed** in Python 3 on Linux with PyYAML 6.0.3. All **55 generated files** matched their authoring sources. The complete **84-file text release** passed inventory and SHA-256 checks with **zero secret-pattern candidates**. Install and update dry runs started no Hermes process.

The tests cover exact screenshot labels, six role names, native YAML fields, manifest ownership, provider neutrality, skin format, shared personality source, platform-specific adapters, Grok durable descriptions, deterministic rendering, source drift, private/runtime paths, synthetic credential patterns, redacted findings, symlink rejection, inventory tampering, selection, native command arguments, confirmation, partial errors, and zero-process dry runs.

## Not executed

- Real Hermes installation/update, actual skin rendering, provider authentication, or model/personality evaluation. The build environment has no installed Hermes executable.
- Grok app field saving, field-size acceptance, persistent behavior, actual messaging, native template creation, or Marketplace import.
- Hosted CI merely because a workflow file exists. Consult the repository's actual Actions run for its separate result.

Offline tests establish file/command integrity and consistency with the documented format, not end-to-end platform correctness or guaranteed model behavior. Use TEST_PROMPTS.md for the remaining acceptance tests. All test fixtures are synthetic; no live account, home directory, model credential, or private conversation export is part of the release.

## Secret review

The custom scanner checks filenames/directories and several credential patterns; findings contain rule names and locations, not matched values. Manual review additionally excludes personal context, internal account identifiers, private logs, user case histories, and raw screenshots. The original ZIP is not copied wholesale into public history.

A clean scan means no candidates were found by these checks, not proof that no conceivable secret exists. Review and scan each update. Never put real credentials in test fixtures. Any discovered credential must be revoked/rotated; deleting it from the current tree does not remove exposure from history.

The checksum inventory covers every release file except itself and excluded development caches. It detects changed bytes, not publisher identity; it is not a signature or protection against replacement of both content and checksums. LF checkout normalization is specified in `.gitattributes`.

## Reproduce

```sh
python -m pip install -r requirements-dev.txt
python tools/build.py --check
python -m unittest discover -s tests -v
python tools/release.py
python manage.py install --all --dry-run
python manage.py update --all --dry-run
```
