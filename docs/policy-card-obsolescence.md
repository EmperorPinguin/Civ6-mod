# Policy Card Obsolescence

Policy cards are represented as capital-only buildings that consume policy-slot resources. When a card becomes obsolete, the UI gate and the active-card removal trigger need to agree.

## Required Pieces

For each obsolete policy card, keep these pieces in sync:

- the card's `Only available <before adopting [...]>` gate in `jsons/Buildings.json`
- the corresponding `Remove [Card] [in capital] <upon turn start> <after adopting [...]>` trigger in `jsons/Policies.json`
- any card effect conditions that also use `<before adopting [...]>`

If one piece changes without the others, the card can remain visible after it cannot be used, or an already active card can keep bonuses after the intended obsolete civic.

## Replacement Comments

Replacement cards can include a visible note that names the cards they obsolete:

```json
"Comment [Obsoletes: Survey, Discipline]"
```

Use comma-style wording for multiple cards, not sentence-style wording with `and`, so Civilopedia output stays consistent and easy to validate.

## Adding Or Changing An Obsolete Card

1. Confirm the original Civilization VI obsolete civic when possible.
2. Add or update the card-level `Only available <before adopting [...]>` gate.
3. Add or update the civic-level removal trigger in `jsons/Policies.json`.
4. Align any effect-level cutoff conditions with the same civic.
5. Add or update a replacement-card `Comment [Obsoletes: ...]` when a newer card clearly replaces an older one.
6. Run `scripts/check-policy-obsolescence.py`.

## Intent

This mod should follow original Civilization VI mechanics for obsolete policy cards unless a difference is deliberate and documented.

