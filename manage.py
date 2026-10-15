#!/usr/bin/env python3
"""Review/install the Hermes profiles; Grok Bot uses the documented app workflow.

Uses only native Hermes CLI commands. Never copies credentials, sets the active
profile, installs packages, enables routines, or edits Hermes state directly.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from tools import build, release

ROOT = Path(__file__).resolve().parent


def selection(args: argparse.Namespace) -> list[dict]:
    agents = build.catalog(ROOT)['agents']
    by_slug = {a['slug']: a for a in agents}
    if args.all and args.profiles:
        raise ValueError('Use profile names or --all, not both')
    names = list(by_slug) if args.all else args.profiles
    if not names:
        raise ValueError('Choose profile names or --all; use list to see choices')
    unknown = sorted(set(names) - set(by_slug))
    if unknown:
        raise ValueError('Unknown profile: ' + ', '.join(unknown))
    return [by_slug[s] for s in dict.fromkeys(names)]


def run(command: list[str], capture: bool = False) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(command, shell=False, check=False, text=True,
                              capture_output=capture, timeout=300)
    except FileNotFoundError as e:
        raise ValueError(f'Executable not found: {command[0]}') from e
    except subprocess.TimeoutExpired as e:
        raise ValueError('Hermes timed out; inspect its state before retrying. Completion is unknown.') from e


def require_cli(binary: str, action: str, describe: bool = False) -> None:
    if not shutil.which(binary) and not Path(binary).is_file():
        raise ValueError('Hermes is not installed/on PATH; use --hermes-bin with its executable path')
    proc = run([binary, 'profile', action, '--help'], capture=True)
    if proc.returncode or '--yes' not in (proc.stdout or ''):
        raise ValueError(f'Hermes does not expose the required profile {action} CLI; inspect its version/help')
    if describe:
        proc = run([binary, 'profile', 'describe', '--help'], capture=True)
        if proc.returncode or '--text' not in (proc.stdout or ''):
            raise ValueError('This Hermes version does not support profile describe --text; omit --describe')


def command_for(args: argparse.Namespace, a: dict) -> list[str]:
    cmd = [args.hermes_bin, 'profile', args.command]
    if args.command == 'install':
        cmd += [str(ROOT / 'profiles' / a['slug']), '--name', a['slug']]
        if args.alias:
            cmd.append('--alias')
        if args.force:
            cmd.append('--force')
    else:
        cmd.append(a['slug'])
        if args.force_config:
            cmd.append('--force-config')
    # Collection-level confirmation covers these exact displayed operations.
    cmd.append('--yes')
    return cmd


def act(args: argparse.Namespace) -> int:
    rows = selection(args)
    count = release.verify(ROOT)
    drift = build.build(ROOT, check=True)
    if drift:
        raise ValueError('Generated files differ from reviewed sources: ' + ', '.join(drift))
    print(f'Verified local release: {count} text files.')
    if args.command == 'update':
        print('UPDATE uses the source recorded by Hermes, not necessarily this checkout.\n'
              'This local release check does NOT scan or hash the payload fetched by native update.\n'
              'Review each origin first with: hermes profile info <name>.\n'
              '--all selects all six known names; missing installations will fail, not be created.')
    if getattr(args, 'force', False) or getattr(args, 'force_config', False):
        print('WARNING: explicit force option may replace your local distributed configuration. Back it up first.')
    for a in rows:
        if args.command == 'install':
            payload = sorted((ROOT / 'profiles' / a['slug']).rglob('*'))
            h = hashlib.sha256()
            for p in payload:
                if p.is_file():
                    h.update(p.relative_to(ROOT / 'profiles' / a['slug']).as_posix().encode() + b'\0' + p.read_bytes() + b'\0')
            print(a['slug'] + ' payload SHA-256: ' + h.hexdigest())
        print('ARGV ' + json.dumps(command_for(args, a)))
        if args.command == 'install' and args.describe:
            print('ARGV ' + json.dumps([args.hermes_bin, 'profile', 'describe', a['slug'], '--text', a['description']]))
    if args.dry_run:
        print('Dry run: no Hermes process started and no profile state changed.')
        return 0
    require_cli(args.hermes_bin, args.command, getattr(args, 'describe', False))
    if not args.yes:
        if not sys.stdin.isatty():
            raise ValueError('Noninteractive changes require --yes after reviewing the dry run')
        if input('Proceed with these operations? [y/N] ').strip().lower() not in {'y', 'yes'}:
            print('Cancelled; nothing installed or updated.')
            return 1
    failures = []
    for a in rows:
        if run(command_for(args, a)).returncode:
            failures.append(a['slug'])
            continue
        if args.command == 'install' and args.describe:
            cmd = [args.hermes_bin, 'profile', 'describe', a['slug'], '--text', a['description']]
            if run(cmd).returncode:
                failures.append(a['slug'] + ' (installed; description step failed)')
    if failures:
        print('Failed/partial: ' + ', '.join(failures), file=sys.stderr)
        return 1
    print('Native commands completed. Configure each new profile as needed and start a new session.\n'
          'No live model or personality evaluation was performed by this installer.')
    return 0


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    sub.add_parser('list')
    sub.add_parser('verify')
    for action in ('install', 'update'):
        s = sub.add_parser(action)
        s.add_argument('profiles', nargs='*')
        s.add_argument('--all', action='store_true')
        s.add_argument('--dry-run', action='store_true')
        s.add_argument('--yes', '-y', action='store_true')
        s.add_argument('--hermes-bin', default=os.environ.get('HERMES_BIN', 'hermes'))
        if action == 'install':
            s.add_argument('--alias', action='store_true')
            s.add_argument('--describe', action='store_true')
            s.add_argument('--force', action='store_true', help='Explicitly replace an existing distributed config; back up first')
        else:
            s.add_argument('--force-config', action='store_true')
    return p


def main() -> int:
    args = parser().parse_args()
    try:
        if args.command == 'list':
            for a in build.catalog(ROOT)['agents']:
                print(f"{a['slug']:<15} {a['name']:<12} {a['label']}")
            return 0
        if args.command == 'verify':
            count = release.verify(ROOT)
            drift = build.build(ROOT, check=True)
            if drift:
                raise ValueError('Generated files differ: ' + ', '.join(drift))
            print(f'PASS: {count} release files; all six platform pairs match the authoring sources.')
            return 0
        return act(args)
    except (OSError, ValueError, KeyError, TypeError) as e:
        print(f'Error: {e}', file=sys.stderr)
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
