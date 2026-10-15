"""Offline regressions; no real account, model, or Hermes runtime is used."""
from contextlib import redirect_stdout, redirect_stderr
import io
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import yaml
import manage
from tools import build, release

ROOT = Path(__file__).resolve().parents[1]
BASELINE = [
    ['General Maintenance AI', 'Limb Servo Control', 'Fire Suppression'],
    ['General Maintenance AI', 'Defragger', 'Video Analyzer'],
    ['Security AI', 'Housekeeping', 'Encryption'],
    ['Socialization AI', 'Humor', 'Tactical Ops'],
    ['Recreational AI', 'Game Theory', 'Weapons'], ['Asshole']]


def args(*values):
    return manage.parser().parse_args(values)


class FormatTests(unittest.TestCase):
    def setUp(self):
        self.agents = build.catalog()['agents']
        self.output = build.rendered()

    def test_exact_roster(self):
        self.assertEqual(tuple(a['slug'] for a in self.agents), build.SLUGS)
        self.assertEqual(len(self.agents), 6)

    def test_exact_original_labels(self):
        self.assertEqual([a['original_labels'] for a in self.agents], BASELINE)

    def test_generation_is_current(self):
        self.assertEqual(build.build(check=True), [])
        self.assertEqual(len(self.output), 55)

    def test_generation_is_deterministic(self):
        self.assertEqual(build.rendered(), self.output)

    def test_native_manifest_fields(self):
        for a in self.agents:
            with self.subTest(a=a['slug']):
                m = yaml.safe_load(self.output[f"profiles/{a['slug']}/distribution.yaml"])
                self.assertEqual(m['name'], a['slug'])
                self.assertEqual(m['version'], '1.1.0')
                self.assertEqual(m['hermes_requires'], '>=0.18.0')
                self.assertEqual(m['license'], 'MIT')
                self.assertNotIn('source', m)
                self.assertNotIn('installed_at', m)
                self.assertNotIn('env_requires', m)

    def test_manifest_owned_paths_exist(self):
        for a in self.agents:
            home = ROOT / 'profiles' / a['slug']
            m = yaml.safe_load((home / 'distribution.yaml').read_text())
            self.assertEqual(set(m['distribution_owned']), {'SOUL.md', 'config.yaml', 'skins/', 'distribution.yaml', 'README.md'})
            for rel in m['distribution_owned']:
                self.assertTrue((home / rel).exists())
                self.assertFalse(release.private_path(rel))

    def test_no_provider_or_permissions_pins(self):
        for a in self.agents:
            cfg = yaml.safe_load(self.output[f"profiles/{a['slug']}/config.yaml"])
            self.assertEqual(cfg, {'display': {'skin': a['slug']}})

    def test_skin_schema_and_name(self):
        for a in self.agents:
            s = yaml.safe_load(self.output[f"profiles/{a['slug']}/skins/{a['slug']}.yaml"])
            self.assertEqual(set(s), {'name', 'description', 'colors', 'spinner', 'branding', 'tool_prefix'})
            self.assertEqual(s['name'], a['slug'])
            self.assertEqual(s['branding']['agent_name'], a['name'])
            for color in s['colors'].values():
                self.assertRegex(color, r'^#[0-9A-Fa-f]{6}$')
            self.assertTrue(all(s['spinner'].values()))

    def test_souls_have_distinct_personas_and_adapter(self):
        bodies = []
        for a in self.agents:
            soul = self.output[f"profiles/{a['slug']}/SOUL.md"]
            persona = (ROOT / 'personas' / f"{a['slug']}.md").read_text().strip()
            self.assertIn(persona, soul)
            self.assertIn('## Hermes runtime adapter', soul)
            self.assertNotIn('## Grok Bot runtime adapter', soul)
            self.assertGreater(len(persona.split()), 400)
            bodies.append(persona)
        self.assertEqual(len(set(bodies)), 6)

    def test_adapters_share_core_not_runtime_assumptions(self):
        for a in self.agents:
            s = a['slug']
            h = self.output[f'profiles/{s}/SOUL.md']
            g = self.output[f'grok-bot/{s}/PLAYBOOK.md']
            self.assertEqual(h.split('## Hermes runtime adapter')[0], g.split('## Grok Bot runtime adapter')[0])
            self.assertNotIn('## Hermes runtime adapter', g)

    def test_grok_descriptions_have_durable_boundaries(self):
        for a in self.agents:
            d = self.output[f"grok-bot/{a['slug']}/DESCRIPTION.txt"]
            for phrase in (a['grok_summary'], 'Auto Review', 'explicit authorization', 'share the cloud computer', 'not a sandbox', 'untrusted data'):
                self.assertIn(phrase, d)
            self.assertLess(len(d), 4000)  # Project budget, not an alleged app limit.

    def test_grok_cards_are_not_claimed_imports(self):
        for a in self.agents:
            card = self.output[f"grok-bot/{a['slug']}/PROFILE.md"]
            self.assertIn('not a native import bundle', card)
            self.assertIn('Edit Profile > Description', card)
            self.assertFalse((ROOT / 'grok-bot' / a['slug'] / 'distribution.yaml').exists())

    def test_starter_tasks_do_not_need_private_inputs(self):
        for a in self.agents:
            t = self.output[f"grok-bot/{a['slug']}/STARTER_TASK.md"]
            self.assertIn(a['starter_task'], t)
            self.assertIn('Do not create a routine', t)
            self.assertNotIn('attached simulated event log', t)

    def test_yaml_emitter_round_trip(self):
        obj = {'name': 'J.A.R.V.I.S.', 'list': ['a: b', 'x # y'], 'nested': {'value': 'quoted "text"'}}
        self.assertEqual(yaml.safe_load(build.yaml_text(obj)), obj)

    def test_yaml_emitter_rejects_unsafe_key(self):
        with self.assertRaises(ValueError):
            build.yaml_text({'bad\nkey': 'value'})


class ManagerTests(unittest.TestCase):
    def setUp(self):
        self.agent = build.catalog()['agents'][0]

    def test_select_all(self):
        self.assertEqual(len(manage.selection(args('install', '--all'))), 6)

    def test_selection_deduplicates(self):
        self.assertEqual(len(manage.selection(args('install', 'stark-u', 'stark-u'))), 1)

    def test_no_implicit_selection(self):
        with self.assertRaises(ValueError):
            manage.selection(args('install'))

    def test_unknown_selection_refused(self):
        with self.assertRaises(ValueError):
            manage.selection(args('install', 'unknown'))

    def test_path_injection_refused(self):
        for target in ('../default', '/tmp/other', 'stark-u; echo bad'):
            with self.subTest(target=target), self.assertRaises(ValueError):
                manage.selection(args('install', target))

    def test_all_and_names_refused(self):
        with self.assertRaises(ValueError):
            manage.selection(args('install', '--all', 'stark-u'))

    def test_native_install_argv(self):
        c = manage.command_for(args('install', '--all'), self.agent)
        self.assertEqual(c, ['hermes', 'profile', 'install', str(ROOT / 'profiles' / 'stark-dum-e'), '--name', 'stark-dum-e', '--yes'])

    def test_force_is_explicit(self):
        self.assertNotIn('--force', manage.command_for(args('install', '--all'), self.agent))
        c = manage.command_for(args('install', '--all', '--force', '--alias'), self.agent)
        self.assertIn('--force', c)
        self.assertIn('--alias', c)

    def test_update_argv(self):
        c = manage.command_for(args('update', '--all', '--force-config'), self.agent)
        self.assertEqual(c, ['hermes', 'profile', 'update', 'stark-dum-e', '--force-config', '--yes'])

    def test_install_dry_run_starts_no_process(self):
        with patch.object(manage, 'run') as run, patch.object(manage, 'require_cli') as preflight, redirect_stdout(io.StringIO()):
            self.assertEqual(manage.act(args('install', '--all', '--dry-run', '--describe')), 0)
            run.assert_not_called()
            preflight.assert_not_called()

    def test_update_dry_run_warns_about_source(self):
        output = io.StringIO()
        with patch.object(manage, 'run') as run, redirect_stdout(output):
            self.assertEqual(manage.act(args('update', '--all', '--dry-run')), 0)
            run.assert_not_called()
        self.assertIn('does NOT scan or hash', output.getvalue())

    def test_bad_checksums_prevent_install(self):
        with patch.object(release, 'verify', side_effect=ValueError('changed')), patch.object(manage, 'run') as run:
            with self.assertRaises(ValueError):
                manage.act(args('install', '--all', '--yes'))
            run.assert_not_called()

    def test_noninteractive_requires_yes(self):
        with patch.object(manage, 'require_cli'), patch.object(manage.sys.stdin, 'isatty', return_value=False), patch.object(manage, 'run') as run, redirect_stdout(io.StringIO()):
            with self.assertRaises(ValueError):
                manage.act(args('install', 'stark-u'))
            run.assert_not_called()

    def test_decline_makes_no_changes(self):
        with patch.object(manage, 'require_cli'), patch.object(manage.sys.stdin, 'isatty', return_value=True), patch('builtins.input', return_value='n'), patch.object(manage, 'run') as run, redirect_stdout(io.StringIO()):
            self.assertEqual(manage.act(args('install', 'stark-u')), 1)
            run.assert_not_called()

    def test_partial_native_failure_is_reported(self):
        with patch.object(manage, 'require_cli'), patch.object(manage, 'run', side_effect=[subprocess.CompletedProcess([], 1), subprocess.CompletedProcess([], 0)]) as run, redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            self.assertEqual(manage.act(args('install', 'stark-u', 'stark-jarvis', '--yes')), 1)
            self.assertEqual(run.call_count, 2)

    def test_describe_failure_is_not_hidden(self):
        output = io.StringIO()
        with patch.object(manage, 'require_cli'), patch.object(manage, 'run', side_effect=[subprocess.CompletedProcess([], 0), subprocess.CompletedProcess([], 1)]), redirect_stdout(io.StringIO()), redirect_stderr(output):
            self.assertEqual(manage.act(args('install', 'stark-u', '--yes', '--describe')), 1)
        self.assertIn('installed; description step failed', output.getvalue())

    def test_missing_cli_is_clear(self):
        with patch.object(shutil, 'which', return_value=None), patch.object(Path, 'is_file', return_value=False):
            with self.assertRaisesRegex(ValueError, 'not installed'):
                manage.require_cli('missing', 'install')

    def test_preflight_rejects_missing_subcommand(self):
        with patch.object(shutil, 'which', return_value='/fake'), patch.object(manage, 'run', return_value=subprocess.CompletedProcess([], 1, stdout='')):
            with self.assertRaises(ValueError):
                manage.require_cli('hermes', 'install')

    def test_preflight_requires_describe_text(self):
        with patch.object(shutil, 'which', return_value='/fake'), patch.object(manage, 'run', side_effect=[subprocess.CompletedProcess([], 0, stdout='--yes'), subprocess.CompletedProcess([], 0, stdout='no option')]):
            with self.assertRaisesRegex(ValueError, '--text'):
                manage.require_cli('hermes', 'install', True)

    def test_subprocess_no_shell_and_bounded(self):
        with patch.object(subprocess, 'run', return_value=subprocess.CompletedProcess([], 0)) as run:
            manage.run(['hermes', 'profile', 'install', 'path with spaces'])
            self.assertFalse(run.call_args.kwargs['shell'])
            self.assertEqual(run.call_args.kwargs['timeout'], 300)
            self.assertEqual(run.call_args.args[0][-1], 'path with spaces')

    def test_timeout_reports_unknown_completion(self):
        with patch.object(subprocess, 'run', side_effect=subprocess.TimeoutExpired('hermes', 300)):
            with self.assertRaisesRegex(ValueError, 'Completion is unknown'):
                manage.run(['hermes'])


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'README.md').write_text('Synthetic release fixture.\n')
        (self.root / 'docs').mkdir()
        (self.root / 'docs' / 'sample.md').write_text('No account data.\n')
        release.write_checksums(self.root)

    def test_actual_release_clean(self):
        self.assertGreater(release.verify(ROOT), 60)

    def test_synthetic_secret_patterns_detected_and_redacted(self):
        cases = ['ghp_' + 'A' * 40, 'xai-' + 'b' * 32, 'sk-proj-' + 'c' * 32,
                 'AKIA' + 'D' * 16, '-----BEGIN ' + 'PRIVATE KEY-----',
                 'eyJ' + 'e' * 20 + '.' + 'f' * 20 + '.' + 'g' * 20,
                 'https://' + 'user:pass@example.invalid', 'password=' + 'h' * 20]
        for value in cases:
            with self.subTest(prefix=value[:4]):
                findings = release.scan_text(value)
                self.assertTrue(findings)
                self.assertNotIn(value, str(findings))

    def test_private_paths_refused(self):
        for value in ('.env', 'profiles/x/.env.bak', 'auth.json', 'docs/token.json', 'memories/MEMORY.md', 'profiles/x/vault/key.txt', 'sessions/log.md', 'file.pem', 'state.db-wal'):
            self.assertTrue(release.private_path(value), value)

    def test_symlink_refused(self):
        link = self.root / 'docs' / 'link.md'
        try:
            link.symlink_to(self.root / 'README.md')
        except OSError:
            self.skipTest('OS does not permit symlink creation')
        with self.assertRaisesRegex(ValueError, 'Symlink'):
            release.scan(self.root)

    def test_unexpected_binary_file_refused(self):
        (self.root / 'docs' / 'image.png').write_bytes(b'not a real image')
        with self.assertRaises(ValueError):
            release.scan(self.root)

    def test_binary_content_detected(self):
        (self.root / 'docs' / 'sample.md').write_bytes(b'bad\x00data')
        self.assertTrue(release.scan(self.root)[1])

    def test_changed_bytes_fail(self):
        (self.root / 'README.md').write_text('Changed.\n')
        with self.assertRaisesRegex(ValueError, 'Checksum mismatch'):
            release.verify_checksums(self.root)

    def test_added_file_fails(self):
        (self.root / 'docs' / 'extra.md').write_text('Extra.\n')
        with self.assertRaisesRegex(ValueError, 'file set'):
            release.verify_checksums(self.root)

    def test_deleted_file_fails(self):
        (self.root / 'docs' / 'sample.md').unlink()
        with self.assertRaisesRegex(ValueError, 'file set'):
            release.verify_checksums(self.root)

    def test_unsafe_inventory_refused(self):
        (self.root / release.INDEX).write_text('0' * 64 + '  ../outside\n')
        with self.assertRaisesRegex(ValueError, 'Unsafe'):
            release.verify_checksums(self.root)

    def test_duplicate_inventory_refused(self):
        p = self.root / release.INDEX
        text = p.read_text()
        p.write_text(text + text.splitlines()[0] + '\n')
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            release.verify_checksums(self.root)

    def test_generation_detects_drift(self):
        for rel in ('catalog.json',):
            shutil.copy2(ROOT / rel, self.root / rel)
        for name in ('personas', 'templates'):
            shutil.copytree(ROOT / name, self.root / name)
        build.build(self.root)
        p = self.root / 'profiles' / 'stark-u' / 'SOUL.md'
        p.write_text(p.read_text() + 'unreviewed change\n')
        self.assertIn('profiles/stark-u/SOUL.md', build.build(self.root, check=True))

    def test_source_symlink_refused(self):
        p = self.root / 'catalog.json'
        try:
            p.symlink_to(ROOT / 'catalog.json')
        except OSError:
            self.skipTest('OS does not permit symlink creation')
        with self.assertRaisesRegex(ValueError, 'Symlink'):
            build.catalog(self.root)


if __name__ == '__main__':
    unittest.main()
