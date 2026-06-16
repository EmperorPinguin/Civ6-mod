# Civ6-mod FAQ Draft

Last updated: 2026-06-16

This is a first draft pulled from repeated GitHub issue questions. It should be edited as the mod and Unciv engine support change.

## Districts

### Why can I not build another district?

District capacity is city-based. Current data gives each city district capacity at population thresholds like 1, 4, 7, 10, 13, 16, 19, 22, and 25.

Districts consume that capacity through `requiredResource: "Districts"`. Older data also subtracted Districts manually, which caused double-counting. That was fixed by [PR #105](https://github.com/EmperorPinguin/Civ6-mod/pull/105). See [issue #100](https://github.com/EmperorPinguin/Civ6-mod/issues/100).

### How do districts finish construction?

Districts are built by city production, not by Workers. When a district asks for a tile, select the tile and let the city finish the district building.

Avoid sending Workers to interact with the selected district tile while the city is still building it. A known Unciv-side automation issue can orphan district construction markers; the upstream fix is tracked in [yairm210/Unciv#14996](https://github.com/yairm210/Unciv/pull/14996). See [issue #53](https://github.com/EmperorPinguin/Civ6-mod/issues/53).

### Why did my district production disappear?

This may be the same district marker/worker automation issue tracked in [issue #53](https://github.com/EmperorPinguin/Civ6-mod/issues/53) and possibly [issue #13](https://github.com/EmperorPinguin/Civ6-mod/issues/13). Update Unciv after the upstream fix lands, then retest with a save file if it still happens.

## Policies And Governments

### How do policies work in this mod?

Policies and governments are modeled as buildings, usually purchased in the capital. This is a workaround for Civ VI-style policy cards inside Unciv's existing systems.

The usual flow is:

1. Unlock a government or policy through the civics tree.
2. Buy or build the government/policy building in the capital.
3. If a policy does not appear immediately, advance a turn and check again.

See [issue #50](https://github.com/EmperorPinguin/Civ6-mod/issues/50).

### Can I change policies?

Yes. You should be able to sell the existing policy building and then purchase a different one, as discussed in [issue #73](https://github.com/EmperorPinguin/Civ6-mod/issues/73).

Some policy behavior has changed over time as Unciv added more support for adopting and unadopting policies, so old comments may be stale.

### Why does Ilkum disappear at Feudalism?

That is intended. Ilkum is available after Craftsmanship and before Feudalism. Feudalism removes Ilkum from the capital. See [issue #48](https://github.com/EmperorPinguin/Civ6-mod/issues/48).

## Envoys And City-States

### How do I send an Envoy?

Move the Envoy unit into city-state territory, open the unit's extra actions, and choose the gift action. Current data grants 20 Influence for gifting an Envoy to a city-state.

Related: [issue #12](https://github.com/EmperorPinguin/Civ6-mod/issues/12).

## Religion

### Why can I only build one worship building?

This is intentional and Civ VI-like. In Civ VI, the worship belief limits the religion to one worship building type. The mod approximates that behavior by limiting the available worship building choice. See [issue #7](https://github.com/EmperorPinguin/Civ6-mod/issues/7).

### Why can Great Prophets not keep spreading religion?

The maintainer previously answered that Great Prophets are not intended to be purchased repeatedly after founding or strengthening a religion. If this is still confusing in-game, it may need Civilopedia text rather than a mechanics change. See [issue #67](https://github.com/EmperorPinguin/Civ6-mod/issues/67).

### Does Religious Victory exist?

Yes, the ruleset has a Religious Victory entry using `Become the world religion`, but it is hidden from the victory screen. It needs playtesting before being advertised as fully supported. See [issue #12](https://github.com/EmperorPinguin/Civ6-mod/issues/12).

## Units And Combat

### How are Civ VI strength bonuses converted to Unciv percentages?

The mod approximates Civ VI strength deltas with Unciv percentage modifiers. The maintainer's rule of thumb from [issue #52](https://github.com/EmperorPinguin/Civ6-mod/issues/52):

- +10 Civ VI strength is about +67% in Unciv.
- +30 Civ VI strength is about +200% in Unciv.

### Do melee units get bonuses against anti-cavalry?

Yes, the bonus is modeled in the unit type data, but it may not be obvious in Civilopedia. See [issue #49](https://github.com/EmperorPinguin/Civ6-mod/issues/49).

### Are circular promotion warnings expected?

Old Unciv versions could warn about Civ6-mod's web-style promotion trees. Upstream Unciv PR [yairm210/Unciv#14995](https://github.com/yairm210/Unciv/pull/14995) fixed the validator so alternative promotion prerequisite paths are handled correctly.

If you still see circular promotion warnings, update Unciv first. See [issue #97](https://github.com/EmperorPinguin/Civ6-mod/issues/97).

## Validation Warnings

### Is every yellow warning a game-breaking problem?

No. Some yellow warnings are historical or cosmetic, and some were caused by older Unciv validator behavior. Recent fixes include:

- City-state unique warnings fixed by [PR #107](https://github.com/EmperorPinguin/Civ6-mod/pull/107).
- District capacity double-counting fixed by [PR #105](https://github.com/EmperorPinguin/Civ6-mod/pull/105).
- Promotion circular-reference validation fixed upstream by [yairm210/Unciv#14995](https://github.com/yairm210/Unciv/pull/14995).

Current unit upgrade/obsolete warnings should still be tracked separately in [issue #20](https://github.com/EmperorPinguin/Civ6-mod/issues/20) until a current mod-ci validator run confirms they are gone.

## Graphics

### Why are some Natural Wonders black tiles?

Those Natural Wonders do not have sprites in this mod yet, so Unciv has nothing to display. This is an art backlog, not necessarily a rules bug.

The maintainer suggested using Civ6 Tileset for many Natural Wonder images or contributing new sprites through a PR. See [issue #54](https://github.com/EmperorPinguin/Civ6-mod/issues/54).

### Why is a unit missing an image?

Some unit art has been added over time. For example, Man-At-Arms and Garde Imperiale assets are now present in the repo. If a unit still renders without art in-game, open a focused issue with the unit name, tileset/unitset, Unciv version, and screenshot.

Related: [issue #90](https://github.com/EmperorPinguin/Civ6-mod/issues/90), [issue #96](https://github.com/EmperorPinguin/Civ6-mod/issues/96).

## Translations

### How do I contribute a translation?

Translation files live in `jsons/translations/`. Use `Template.properties` as the source key list. Keep the left side of each `key = value` line unchanged and translate only the right side.

Good translation PRs should:

- Fill blank entries in the target language file.
- Preserve placeholders, brackets, and game terms used by Unciv.
- Avoid translating internal keys differently across the file.
- Mention whether the translation was machine-assisted, native-reviewed, or both.

Related: Indonesian [issue #8](https://github.com/EmperorPinguin/Civ6-mod/issues/8), Russian [issue #19](https://github.com/EmperorPinguin/Civ6-mod/issues/19).

### AI prompt for generating missing translations

```text
You are helping translate the Civ6-mod Unciv mod.

Target language: <language>

Rules:
- Preserve the left side of every "key = value" line exactly.
- Translate only the right side.
- Preserve bracketed game syntax, placeholders, numbers, punctuation, and capitalization where they are part of game data.
- If a term is a proper noun from Civilization VI, prefer the official localized Civ VI term when known.
- Leave uncertain entries blank and add a short review note after the output.

Input:
<paste blank or partially translated .properties lines here>
```

### AI prompt for reviewing a translation

```text
Review this Civ6-mod translation file against Template.properties.

Check for:
- Missing keys.
- Blank values.
- English text left untranslated.
- Broken bracket syntax.
- Inconsistent translations of the same game term.
- Values that accidentally changed the left-side key.

Return:
- A summary count.
- A list of high-risk lines to review manually.
- Suggested corrected values for obvious issues.
```

## Missing Civs, Leaders, And Future Content

### Why are some later Civ VI civs or leaders missing?

Some later Civ VI civs and leaders rely on specialized mechanics that are difficult to represent cleanly in Unciv. The maintainer has described Vietnam, Babylon, Portugal, and some leader abilities as future-project territory rather than simple data entry.

Related: [issue #16](https://github.com/EmperorPinguin/Civ6-mod/issues/16), [issue #45](https://github.com/EmperorPinguin/Civ6-mod/issues/45), [issue #46](https://github.com/EmperorPinguin/Civ6-mod/issues/46).

### Are district trade route yields implemented?

Not fully. A proof of concept exists using Unciv's current connected-city trade route yields, but the maintainer preferred waiting for better BNW trade route support rather than adding a temporary approximation. See [issue #104](https://github.com/EmperorPinguin/Civ6-mod/issues/104).
