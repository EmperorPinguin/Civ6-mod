# AI Contributor Instructions

These instructions apply to the entire repository. Use them when making AI-assisted changes to Civ6-mod.

For the longer reference, see `docs/ai-contributors.md`.

## Project Intent

- This is a work-in-progress Unciv base ruleset that aims to recreate Civilization VI mechanics.
- Prefer original Civilization VI behavior unless a difference is clearly intentional.
- Preserve legacy attribution, including `Red11 (3.12.11)` in `README.md` and credits in `Credits.txt`.

## Editing Guidelines

- Keep changes narrowly scoped.
- Avoid broad JSON reformatting or unrelated cleanup.
- Do not remove existing art, credits, generated atlas files, or metadata unless the task explicitly calls for it.
- When adding generated or external assets, place them deliberately and document attribution or generation notes where appropriate.
- Preserve existing Unciv unique syntax and nearby file style.

## Policy Card Changes

Policy cards are represented as capital-only buildings that consume policy-slot resources. Before editing obsolete policy cards, read `docs/policy-card-obsolescence.md`.

Keep these pieces aligned:

- `Only available <before adopting [...]>` on the card in `jsons/Buildings.json`
- `Remove [Card] [in capital] <upon turn start> <after adopting [...]>` on the civic in `jsons/Policies.json`
- any effect-level `<before adopting [...]>` conditions on the card

Replacement cards may include visible comma-style comments:

```json
"Comment [Obsoletes: Survey, Discipline]"
```

## Validation

Run this after touching policy cards, civic unlocks, obsolete-card behavior, or the validation script:

```sh
scripts/check-policy-obsolescence.py
```

If a built Unciv desktop jar is available, also run:

```sh
java -jar /path/to/Unciv/desktop/build/libs/Unciv.jar mod-ci
```

Existing `mod-ci` warnings about colors, duplicate names, atlas generation, or placeholder uniques may be pre-existing. New errors should be treated as blockers.

## Documentation

- Keep `README.md` as the contributor-facing front door.
- Put longer contributor knowledge in `docs/`.
- Keep AI-facing conventions here so future AI-assisted edits stay consistent.
- Keep general contributor workflow in `docs/contributing.md`.

## Issue Triage Docs

- Treat `docs/IssueTriage.md` and `docs/FAQ.md` as human-curated project notes.
- Treat `docs/IssueTriageSnapshot.md` as generated output.
- Update the generated snapshot with `scripts/generate_issue_triage.py` instead of hand-editing it.
- The scheduled issue-triage workflow should open a PR when the generated snapshot changes.
