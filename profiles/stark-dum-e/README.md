# D.U.M.-E. - Hermes

Safe repair planning, reversible maintenance, and workshop troubleshooting. Owns the repair sequence; U. owns independent diagnosis and verification.

Install this directory with the native Hermes distribution command, or use the reviewed collection manager from the repository root.

```sh
python manage.py install stark-dum-e --describe
hermes -p stark-dum-e setup
hermes -p stark-dum-e chat
```

New profiles need their own provider setup where not already available. No model, provider, credentials, sessions, or memory are shipped. The skin is cosmetic, not a voice or an avatar. See ../../docs/HERMES.md for updates and Bot Mode.
