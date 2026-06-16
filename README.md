![Civilization 6 Mod for Unciv banner](.github/assets/readme-banner.jpg)

# Civilization 6 Mod for Unciv

A work-in-progress Unciv base ruleset that aims to recreate Civilization VI mechanics, content, and pacing inside Unciv.

Original README attribution: Red11 (3.12.11). Current repository metadata lists EmperorPinguin as maintainer.

## Status

This mod is actively evolving and should be treated as incomplete. Expect ongoing gaps, balance differences, and mechanics that need Unciv-specific approximations.

Current focus areas include:

- Civ VI-style civics, policies, governments, and policy cards
- Districts, buildings, wonders, improvements, resources, and terrain
- Civilization and leader data
- Unit lines, promotions, and icon coverage
- Validation around ruleset data that is easy to regress

## Repository Layout

- `jsons/` - ruleset data loaded by Unciv
- `jsons/ModOptions.json` - mod metadata and base ruleset settings
- `jsons/translations/` - translation files
- `Images/` - icons, unit art, improvements, resources, policy icons, and related art
- `scripts/` - local validation helpers for contributors
- `AGENTS.md` - AI-assisted contribution guidance
- `Credits.txt` - art and contributor credits

## Validation

Run these checks before opening a PR or after touching policy/card data.

```sh
scripts/check-policy-obsolescence.py
```

This checks policy card availability gates, obsolete-card removal triggers, effect cutoff conditions, comment wording, and smoke scenarios around key civics.

The same check runs in GitHub Actions for pull requests that touch policy data or the validation script.

If you have a built Unciv desktop jar, also run Unciv's mod validator from the mod root:

```sh
java -jar /path/to/Unciv/desktop/build/libs/Unciv.jar mod-ci
```

`mod-ci` may report existing warnings for colors, duplicate names, image atlas generation, or placeholder uniques. New errors should be treated as blockers.

## Policy Card Obsolescence

Policy cards are represented as capital-only buildings that consume policy-slot resources. For obsolete cards, keep these three pieces in sync:

- the card's `Only available <before adopting [...]>` gate in `jsons/Buildings.json`
- the corresponding `Remove [Card] [in capital] <upon turn start> <after adopting [...]>` trigger in `jsons/Policies.json`
- any card effect conditions that also use `<before adopting [...]>`

Replacement cards can include a visible note such as:

```json
"Comment [Obsoletes: Survey, Discipline]"
```

Use comma-style wording for multi-card comments so the Civilopedia output stays consistent.

## Contributing Notes

- Keep changes narrowly scoped and avoid broad JSON formatting churn.
- Prefer matching original Civilization VI mechanics unless a difference is intentional.
- When adding a new obsolete policy interaction, update both the card gate and the civic removal trigger.
- Run the policy obsolescence script when changing policy cards or civic unlocks.
- For AI-assisted changes, follow `AGENTS.md`.
- Preserve contributor and art attribution in `Credits.txt`.

## Credits

Original mod by Red11, with art by Red11, LynxRo, GeneralWadaling, Caballero Arepa, and credited Noun Project artists.

The README banner is a generated original asset for this repository.

See `Credits.txt` for the full attribution list.
