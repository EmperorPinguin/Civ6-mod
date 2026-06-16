# Repository Layout

The mod is an Unciv base ruleset. Most gameplay behavior is represented as JSON data and image assets.

## Main Paths

- `jsons/` - ruleset data loaded by Unciv.
- `jsons/ModOptions.json` - mod metadata and base ruleset settings.
- `jsons/translations/` - translation files.
- `Images/` - icons, unit art, improvements, resources, policy icons, and related art.
- `scripts/` - local validation and automation helpers for contributors.
- `.github/workflows/` - GitHub Actions checks.
- `.github/assets/` - repository presentation assets used by docs.
- `docs/` - contributor knowledge pages.
- `AGENTS.md` - AI-assisted contribution entry point.
- `Credits.txt` - art and contributor credits.

## Editing Notes

- Keep JSON changes narrow and avoid broad formatting churn.
- Preserve nearby file style and Unciv unique syntax.
- Do not remove art, credits, generated atlas files, or metadata unless the task explicitly calls for it.
- When adding generated or external assets, document attribution or generation notes where appropriate.
