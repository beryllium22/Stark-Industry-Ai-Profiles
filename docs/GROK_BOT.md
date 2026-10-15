# Grok Bot setup and sharing

## Product and supported workflow

This adapter targets the official **Grok Bot app** documented under `docs.x.ai/grok-bot`, not Grok Companions, a Discord bot, or a third-party wrapper named GrokBot.

[Create and manage Bots](https://docs.x.ai/grok-bot/bots) documents Name, Label, Description, Avatar, and app-created shared templates. The reviewed documentation did not establish a public profile-file import schema or native import CLI. These folders are therefore **authoring cards**, not claimed native imports. A model API request is not an app profile installation.

## Create each profile

1. Choose **New** or **Ctrl/Cmd+N**, then **Create new Bot**.
2. Open **Edit Profile** and use Name and Label from `grok-bot/<slug>/PROFILE.md`.
3. Paste all of `DESCRIPTION.txt` into Description. Save and reopen it to verify retention. The descriptions are roughly 2.6 KB; no official field-size limit was verified. If a field rejects the content, shorten optional prose while preserving role and boundaries, then retest. Do not rely on silent truncation.
4. Send `STARTER_TASK.md` as a normal message. Its synthetic inputs require no account credentials. It is a one-time test, not a routine.
5. Attach `PLAYBOOK.md` when an extended working method is useful. It is task context, not an automatically loaded system file. Essential role, approval, and privacy rules already live in Description.

Start with one useful Bot rather than creating a group or another roster as a side effect. Avatars are optional and manual. No actor pictures, franchise logos, or cloned voices are included.

## Official role examples

The official [use-case library](https://docs.x.ai/grok-bot/use-cases) includes Chief of Staff, Product Performance, and Bug Reproduction. This pack follows its operational approach: clear ownership, approved inputs, a concrete deliverable, and explicit boundaries. No unofficial repository is presented as the Grok native contract.

## Shared computer and approvals

The official [computer guide](https://docs.x.ai/grok-bot/computer-and-apps) explains that account Bots share cloud files, browser sessions, and app/CLI logins. Separate conversations or screens are not credential or filesystem isolation. Visible access is not authorization for every task. Confirm whether an action will run in the cloud or on an explicitly approved local computer.

Preserve [Auto Review and approval controls](https://docs.x.ai/grok-bot/approvals-security-and-privacy). Do not add broad allow rules just to make a persona more autonomous. Use secure secret handoff or human takeover for login steps rather than posting passwords or one-time codes in chat.

[Messaging](https://docs.x.ai/grok-bot/chat-and-collaboration) can be asynchronous or administrator-restricted. Keep one owner and verify outcomes; a sent handoff is not completion. Use a one-to-one conversation for sensitive approval/handoff surfaces when required.

## Skills, routines, and actual template links

The official [skills/routines guide](https://docs.x.ai/grok-bot/skills-routines-and-automations) supports refining a one-time task before saving or scheduling it. This pack creates neither. A future skill should define inputs, method, validation, output, and boundaries without secrets. A routine needs explicit scope, owner, schedule/time zone, missing-data behavior, and stop conditions.

After testing, use **Share > Create template**. Inspect **View template details**, choose the intended audience, and copy the actual app-generated link. Do not assume the default audience is private. Review identity, description, skills, routines, and every other shared field; remove secrets, internal URLs, personal history, and customer data.

Create a public template from a clean public-role Bot, not a long-used personal Bot. Add only a verified real template link to this repository afterward. No template IDs, Marketplace imports, or share URLs are fabricated here. A shared-template copy does not grant your logins; a shared Team Bot is a different feature.

## Validation limits

Authoring text is checked against the documented workflow. Live field saving, length acceptance, persistent behavior, messaging, and native shared-template creation remain untested. The optional playbook is not guaranteed to persist merely because it was attached once. TEST_PROMPTS.md supplies the remaining acceptance tests.
