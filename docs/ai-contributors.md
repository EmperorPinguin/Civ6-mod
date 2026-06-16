# AI Contributor Guidance

These notes help AI-assisted edits stay consistent with the project. The top-level `AGENTS.md` is the entry point many AI tools auto-read; this page holds the longer reference.

## Project Intent

- This is a work-in-progress Unciv base ruleset that aims to recreate Civilization VI mechanics.
- Prefer original Civilization VI behavior unless a difference is clearly intentional.
- Preserve legacy attribution, including `Red11 (3.12.11)` in `README.md` and credits in `Credits.txt`.

## Editing Guidelines

- Keep changes narrowly scoped.
- Avoid broad JSON reformatting or unrelated cleanup.
- Preserve existing Unciv unique syntax and nearby file style.
- Do not remove existing art, credits, generated atlas files, or metadata unless the task explicitly calls for it.
- When adding generated or external assets, place them deliberately and document attribution or generation notes where appropriate.

## Policy Card Changes

Before changing policy cards, read [Policy card obsolescence](policy-card-obsolescence.md).

When editing obsolete policy cards, keep these aligned:

- `Only available <before adopting [...]>` on the card in `jsons/Buildings.json`
- `Remove [Card] [in capital] <upon turn start> <after adopting [...]>` on the civic in `jsons/Policies.json`
- any effect-level `<before adopting [...]>` conditions on the card

## Validation

After touching policy cards, civic unlocks, obsolete-card behavior, or validation code, run:

```sh
scripts/check-policy-obsolescence.py
```

If a built Unciv desktop jar is available, also run:

```sh
java -jar /path/to/Unciv/desktop/build/libs/Unciv.jar mod-ci
```

## Documentation

- Keep `README.md` as the contributor-facing front door.
- Put longer contributor knowledge in `docs/`.
- Keep `AGENTS.md` short enough that AI tools can quickly find the right deeper page.

