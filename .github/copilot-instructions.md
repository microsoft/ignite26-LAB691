# Microsoft Ignite 2026 repository instructions

This repository is a Microsoft Ignite 2026 session template. Use the **Ignite 2026 repository agent** for setup.

## Workflows

There are two workflows:

- `help me initialize repo` — populate README with session content
- `help me finalize repo` — clean up, validate, and prepare for publication

Plus:

- `help me handle issues` — triage and apply safe fixes to open GitHub issues

## Core rules

- Never fabricate session metadata, links, or content.
- Preserve authored content. Do not overwrite non-placeholder sections without confirmation.
- Use sentence case for Markdown headings.
- Use session-owner language. Announce the section being worked on. Do not narrate patches, diagnostics, or editor internals.
- Track answers within a workflow phase. Do not re-ask questions.
- Do not choose runtimes, install packages, scaffold implementation code, or run project test suites.

## Initialize scope

- Fill in README metadata: session code, title, description, learning outcomes (exactly three), technologies, content owners, delivery links.
- Do NOT run scripts, linters, or shell commands.
- Do NOT delete folders.
- Do NOT remove the "Before you're done" section.
- For workshops/labs: attendee path is always both (guided + self-paced). Do not ask.
- For workshops/labs: do not ask a separate live-demo question.

## Finalize scope

- Remove the "Before you're done" section and template markers.
- Confirm which unused folders to remove.
- Verify the repo is ready to publish by running through an inline checklist (placeholders, required README sections, and relative link targets).
- If any fail: report in plain language, propose fixes, ask permission to apply, then re-check.
- Once all pass: remove template-only tooling (`.github/agents/`, `.github/tests/`, `.github/copilot-instructions.md`, `.github/AGENT-WORKFLOW.md`). Remove `.github/` if empty.
- Report the repo as ready to publish.

## Folder purposes

- `instructions/` — attendee step-by-step guidance
- `docs/` — supporting reference material and architecture/context
- `src/`, `data/`, `infra/`, `.devcontainer/` — session-specific technical folders (optional)

Attendee guidance can remain in `docs/` for intentional MkDocs or docs-site patterns when the root README links clearly to the entry point.

## Session code prefixes

Accept: `BRK`, `WRK`, `LAB`, `ILL`, `LTG`, `THR`, `DEM`, `INV`, `PREL`, `PREB` followed by digits.

## Do not

- Do not close GitHub issues automatically.
- Do not delete authored content without confirmation.
- Do not modify validation scripts during normal workflows.
- Do not use language like "publication blocker", "focused Markdown diagnostics", "initialization readiness", or "local hypothesis". Write for a speaker, not a QA engineer.
