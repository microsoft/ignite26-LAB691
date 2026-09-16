# Microsoft Ignite 2026 repository agent workflow

Use the **Microsoft Ignite 2026 repository agent** in GitHub Copilot Chat to set up and finalize a session repository.

There are two main workflows plus an optional issue-triage workflow.

## Initialize repo

Run this first after creating a repository from the template.

Say `help me initialize repo`.

The agent asks focused questions and populates:

- README.md — session code, title, description, learning outcomes (exactly three), technologies, and content owners

Initialize does not run scripts, delete folders, or remove template scaffolding. It sets up content; Finalize cleans up.

## Finalize repo

Run this when the session content is done and you're ready to publish.

Say `help me finalize repo`.

The agent:

1. Removes the "Before you're done" section and template markers
2. Confirms which unused folders to remove
3. Runs validation checks (Markdown links, publication readiness, Markdown lint)
4. If any checks fail, reports the failure and proposes fixes. You accept and the agent applies them, then re-runs.
5. Once checks pass, removes the template-only tooling from the repo:
   - `.github/agents/`
   - `.github/tests/`
   - `.github/copilot-instructions.md`
   - `.github/AGENT-WORKFLOW.md`
6. Reports the repo as ready to publish

After Finalize, the repo contains only what attendees need.

## Handle issues

Say `help me handle issues`.

The agent groups open issues by risk, applies safe fixes with your permission, and leaves issue closure to you.

## Supported session types

- Breakout (BRK)
- Innovation session (INV)
- Preday breakout (PREB)
- Workshop or lab (WRK, LAB, ILL)
- Preday lab (PREL)
- Lightning or theater (LTG, THR)

For workshops, labs, and preday labs, attendee guidance is always both guided and self-paced. The agent does not ask that as a separate question.

Attendee guidance normally lives in `instructions/`. Repositories intentionally built as MkDocs or other docs sites may keep attendee guidance in `docs/` when the root README links clearly to the entry point.


## Communication style

The agent names the section it is working on before making changes. It uses session-owner language. It does not describe patches, lint internals, or debugging steps.
