# Contributing

Thanks for helping improve Civ6-mod. Keep changes focused and make it easy for maintainers to see what changed, why it changed, and how it was checked.

## General Guidelines

- Keep changes narrowly scoped and avoid broad JSON formatting churn.
- Prefer original Civilization VI mechanics unless a difference is intentional.
- Preserve contributor and art attribution in `Credits.txt`.
- Preserve nearby file style and Unciv unique syntax.
- Update contributor docs when changing contributor-facing behavior.

## Common Checks

- Run the most specific validation for the files you changed.
- For policy cards, civic unlocks, or obsolete-card behavior, run `scripts/check-policy-obsolescence.py`.
- If a built Unciv desktop jar is available, run Unciv's `mod-ci` validator.
- Note known pre-existing warnings in the PR instead of burying them.

See [Validation](validation.md) for command details.

## Policy Cards

When adding or changing obsolete policy-card behavior, update both the card gate and the civic removal trigger. Also check any effect-level cutoff conditions.

See [Policy card obsolescence](policy-card-obsolescence.md) for the full checklist.

## AI-Assisted Edits

AI-assisted changes should follow the top-level `AGENTS.md` file and the longer [AI contributor guidance](ai-contributors.md).

