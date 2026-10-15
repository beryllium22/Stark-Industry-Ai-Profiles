#!/usr/bin/env python3
"""Audit text-only release files and maintain SHA-256 inventory. No network access.

Pattern matching is a release check, not proof that every possible secret is absent.
Reports show rule names and locations, never the matched credential value.
"""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path, PurePosixPath
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
INDEX = 'CHECKSUMS.sha256'
SKIP_DIRS = {'.git', '__pycache__', '.pytest_cache', '.venv'}
ROOT_FILES = {'.gitignore', '.gitattributes', 'README.md', 'LICENSE', 'CHANGELOG.md', 'catalog.json',
              'manage.py', INDEX, 'requirements-dev.txt'}
TOP_DIRS = {'personas', 'templates', 'tools', 'tests', 'docs', 'profiles', 'grok-bot', '.github'}
TEXT_SUFFIXES = {'.md', '.txt', '.py', '.json', '.yaml', '.yml', '.sha256'}
PRIVATE_NAMES = {'auth.json', 'credentials.json', 'token.json', 'tokens.json', 'secrets.json',
                 '.netrc', '.npmrc', '.pypirc', '.git-credentials', 'id_rsa', 'id_ed25519',
                 'cookies.json', 'cookies.txt', '.op.env', 'mcp.json', 'profile.yaml'}
PRIVATE_DIRS = {'memories', 'sessions', 'logs', 'workspace', 'backups', 'state-snapshots',
                'vault', 'mcp-tokens', 'proxy', 'platforms', '.ssh', '.aws', '.azure',
                '.kube', '.gnupg', '.config', 'browser-data', 'local'}
PATTERNS = {
    'github-token': re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})\b'),
    'provider-token': re.compile(r'\b(?:sk-(?:proj-|ant-)?|xai-)[A-Za-z0-9_-]{24,}\b'),
    'cloud-access-id': re.compile(r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'),
    'private-key': re.compile(r'-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----'),
    'jwt': re.compile(r'\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b'),
    'credential-in-url': re.compile(r'https?://[^\s/@:]+:[^\s/@]+@', re.I),
    'assigned-secret': re.compile(r'''(?im)^\s*["']?(?:api[_-]?key|access[_-]?token|client[_-]?secret|password|bot[_-]?token)["']?\s*[:=]\s*["']?([A-Za-z0-9_./+!@#$%=-]{12,})'''),
}


def private_path(rel: str) -> bool:
    parts = PurePosixPath(rel).parts
    low = [v.lower() for v in parts]
    name = low[-1] if low else ''
    return (any(v in PRIVATE_DIRS for v in low) or name in PRIVATE_NAMES
            or name == '.env' or name.startswith('.env.')
            or name.startswith('auth.json.') or name.startswith('state.db')
            or Path(name).suffix in {'.pem', '.key', '.p12', '.pfx', '.sqlite', '.db', '.zip', '.gz'})


def files(root: Path = ROOT) -> list[Path]:
    if root.is_symlink() or not root.is_dir():
        raise ValueError('Release root must be a real directory')
    result = []
    def visit(folder: Path) -> None:
        for p in sorted(folder.iterdir()):
            rel = p.relative_to(root).as_posix()
            if p.is_symlink():
                raise ValueError(f'Symlink refused: {rel}')
            if p.is_dir() and p.name in SKIP_DIRS:
                continue
            if private_path(rel):
                raise ValueError(f'Private/runtime path refused: {rel}')
            top = PurePosixPath(rel).parts[0]
            if p.is_dir():
                if top not in TOP_DIRS:
                    raise ValueError(f'Unexpected release directory: {rel}')
                visit(p)
            elif p.is_file():
                if '/' not in rel and rel not in ROOT_FILES:
                    raise ValueError(f'Unexpected release file: {rel}')
                if '/' in rel and (top not in TOP_DIRS or p.suffix not in TEXT_SUFFIXES):
                    raise ValueError(f'Unexpected release file type: {rel}')
                if p.stat().st_size > 1_000_000:
                    raise ValueError(f'Oversized release file: {rel}')
                result.append(p)
            else:
                raise ValueError(f'Nonregular file refused: {rel}')
    visit(root)
    return sorted(result)


def scan_text(text: str) -> list[tuple[str, int]]:
    findings = []
    for rule, pattern in PATTERNS.items():
        for m in pattern.finditer(text):
            findings.append((rule, text.count('\n', 0, m.start()) + 1))
    return findings


def scan(root: Path = ROOT) -> tuple[int, list[str]]:
    candidates = files(root)
    findings = []
    for p in candidates:
        rel = p.relative_to(root).as_posix()
        try:
            text = p.read_text(encoding='utf-8')
        except UnicodeError:
            findings.append(f'{rel}: non-UTF-8 content')
            continue
        if '\x00' in text:
            findings.append(f'{rel}: binary content')
        findings.extend(f'{rel}:{line}: {rule}' for rule, line in scan_text(text))
    return len(candidates), findings


def digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def write_checksums(root: Path = ROOT) -> None:
    candidates = files(root)
    entries = [f'{digest(p)}  {p.relative_to(root).as_posix()}' for p in candidates if p.relative_to(root).as_posix() != INDEX]
    (root / INDEX).write_bytes(('\n'.join(entries) + '\n').encode('utf-8'))


def verify_checksums(root: Path = ROOT) -> None:
    p = root / INDEX
    if p.is_symlink() or not p.is_file():
        raise ValueError('Missing or unsafe checksum inventory')
    expected = {}
    for line in p.read_text(encoding='utf-8').splitlines():
        if not line:
            continue
        match = re.fullmatch(r'([0-9a-f]{64})  (.+)', line)
        if not match:
            raise ValueError('Malformed checksum record')
        h, rel = match.groups()
        parts = PurePosixPath(rel)
        if parts.is_absolute() or '..' in parts.parts or '\\' in rel or rel != parts.as_posix():
            raise ValueError('Unsafe checksum path')
        if rel == INDEX or rel in expected:
            raise ValueError('Duplicate or self-referential checksum record')
        expected[rel] = h
    actual = {p.relative_to(root).as_posix(): digest(p) for p in files(root) if p.relative_to(root).as_posix() != INDEX}
    if set(actual) != set(expected):
        raise ValueError('Checksum inventory does not match release file set')
    changed = [rel for rel in expected if actual[rel] != expected[rel]]
    if changed:
        raise ValueError('Checksum mismatch: ' + ', '.join(changed))


def verify(root: Path = ROOT) -> int:
    count, findings = scan(root)
    if findings:
        raise ValueError('Potential secret findings (values redacted):\n' + '\n'.join(findings))
    verify_checksums(root)
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-checksums', action='store_true', help='Maintainer action after reviewing changed files')
    args = parser.parse_args()
    try:
        count, findings = scan()
        if findings:
            raise ValueError('\n'.join(findings))
        if args.write_checksums:
            write_checksums()
        count = verify()
    except (OSError, ValueError) as e:
        print(f'Release check failed: {e}', file=sys.stderr)
        return 1
    print(f'PASS: {count} text files; no secret-pattern candidates; checksum inventory verified.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
