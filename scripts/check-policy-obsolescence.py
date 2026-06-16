#!/usr/bin/env python3
"""Validate Civ6 policy card obsolescence gates.

This catches policy cards that are still selectable after their effect has
expired, missing capital-removal triggers, and civic gate combinations that can
never be satisfied.
"""

from __future__ import annotations

import re
import sys
import argparse
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


POLICY_SLOT_RESOURCES = {
    "Military Policy Slots",
    "Economic Policy Slots",
    "Diplomatic Policy Slots",
    "Wildcard Policy Slots",
}

SMOKE_CHECKS = [
    {
        "civic": "Theology",
        "unavailable": ["God King"],
        "available": ["Scripture"],
        "removed": [("God King", "Theology")],
    },
    {
        "civic": "Exploration",
        "unavailable": ["Maritime Industries"],
        "available": ["Press Gangs"],
        "removed": [("Maritime Industries", "Exploration")],
    },
    {
        "civic": "Colonialism",
        "unavailable": ["Survey", "Discipline"],
        "available": ["Native Conquest"],
        "removed": [("Survey", "Colonialism"), ("Discipline", "Colonialism")],
    },
    {
        "civic": "The Enlightenment",
        "unavailable": ["Urban Planning"],
        "available": ["Free Market", "Rationalism"],
        "removed": [("Urban Planning", "The Enlightenment")],
    },
    {
        "civic": "Urbanization",
        "unavailable": ["Professional Army"],
        "available": ["Force Modernization"],
        "removed": [("Professional Army", "Urbanization")],
    },
    {
        "civic": "Totalitarianism",
        "unavailable": ["Limes"],
        "available": ["Lightning Warfare"],
        "removed": [("Limes", "Totalitarianism")],
    },
    {
        "civic": "Class Struggle",
        "unavailable": ["Craftsmen", "Natural Philosophy"],
        "available": ["Five-Year Plan"],
        "removed": [
            ("Craftsmen", "Class Struggle"),
            ("Natural Philosophy", "Class Struggle"),
        ],
    },
    {
        "civic": "Suffrage",
        "unavailable": ["Town Charters", "Naval Infrastructure"],
        "available": ["Economic Union", "Their Finest Hour"],
        "removed": [
            ("Town Charters", "Suffrage"),
            ("Naval Infrastructure", "Suffrage"),
        ],
    },
    {
        "civic": "Professional Sports",
        "extra_adopted": ["Opera and Ballet"],
        "unavailable": ["Aesthetics"],
        "available": ["Sports Media", "Grand Opera"],
        "removed": [("Aesthetics", "Professional Sports")],
    },
    {
        "civic": "Globalization",
        "unavailable": ["Their Finest Hour"],
        "available": ["Ecommerce"],
        "removed": [("Their Finest Hour", "Globalization")],
    },
]


@dataclass
class PolicyCard:
    name: str
    afters: set[str]
    befores: set[str]
    effect_befores: set[str]
    comments: list[str]


def strip_comments(text: str) -> str:
    """Strip // and /* */ comments while preserving quoted strings."""
    out: list[str] = []
    in_string = False
    escaped = False
    i = 0
    while i < len(text):
        char = text[i]
        if in_string:
            out.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            i += 1
            continue

        if char == '"':
            in_string = True
            out.append(char)
            i += 1
            continue

        if char == "/" and i + 1 < len(text) and text[i + 1] == "/":
            while i < len(text) and text[i] != "\n":
                i += 1
            continue

        if char == "/" and i + 1 < len(text) and text[i + 1] == "*":
            i += 2
            while i + 1 < len(text) and not (text[i] == "*" and text[i + 1] == "/"):
                i += 1
            i += 2
            continue

        out.append(char)
        i += 1

    return "".join(out)


def parse_civics(policies_text: str) -> dict[str, list[str]]:
    civics: dict[str, list[str]] = {}
    # Civic entries are nested inside the Civic Tree object and indented 3+ tabs.
    pattern = re.compile(
        r'\n[ \t]{3,}\{\s*\n[ \t]*"name":\s*"([^"]+)"(?P<body>.*?)(?=\n[ \t]{3,}\},)',
        re.S,
    )
    for match in pattern.finditer(policies_text):
        name = match.group(1)
        body = match.group("body")
        requires_match = re.search(r'"requires":\s*\[([^\]]*)\]', body, re.S)
        civics[name] = (
            re.findall(r'"([^"]+)"', requires_match.group(1))
            if requires_match
            else []
        )
    return civics


def parse_policy_cards(buildings_text: str) -> dict[str, PolicyCard]:
    cards: dict[str, PolicyCard] = {}
    for entry in re.split(r'\n\s*\{\n\s*"name": ', buildings_text)[1:]:
        name_match = re.match(r'"([^"]+)"', entry)
        if not name_match:
            continue
        name = name_match.group(1)

        resource_match = re.search(r'"requiredResource":\s*"([^"]+)"', entry)
        if not resource_match or resource_match.group(1) not in POLICY_SLOT_RESOURCES:
            continue

        afters = set(re.findall(r'Only available <after adopting \[([^\]]+)\]>', entry))
        befores = set(re.findall(r'Only available <before adopting \[([^\]]+)\]>', entry))
        comments = re.findall(r'Comment \[([^\]]+)\]', entry)
        effect_befores = {
            match
            for line in entry.splitlines()
            if '"Only available ' not in line
            for match in re.findall(r'<before adopting \[([^\]]+)\]>', line)
        }

        cards[name] = PolicyCard(name, afters, befores, effect_befores, comments)

    return cards


def parse_removals(policies_text: str) -> set[tuple[str, str]]:
    return set(
        re.findall(
            r'"Remove \[([^\]]+)\] \[in capital\] <upon turn start> <after adopting \[([^\]]+)\]>"',
            policies_text,
        )
    )


def ancestors_for(civic: str, civics: dict[str, list[str]], cache: dict[str, set[str]]) -> set[str]:
    if civic in cache:
        return cache[civic]

    seen: set[str] = set()
    stack = list(civics.get(civic, []))
    while stack:
        current = stack.pop()
        if current in seen:
            continue
        seen.add(current)
        stack.extend(civics.get(current, []))

    cache[civic] = seen
    return seen


def is_available(card: PolicyCard, adopted: set[str]) -> bool:
    return card.afters.issubset(adopted) and card.befores.isdisjoint(adopted)


def validate(civics: dict[str, list[str]], cards: dict[str, PolicyCard], removals: set[tuple[str, str]]) -> list[str]:
    errors: list[str] = []
    ancestor_cache: dict[str, set[str]] = {}

    if "Craftsmanship" not in civics or "Code of Laws" not in civics:
        errors.append("Could not parse the civic tree correctly.")

    for card in cards.values():
        for civic in sorted(card.afters | card.befores | card.effect_befores):
            if civic not in civics:
                errors.append(f"{card.name}: unknown civic gate [{civic}]")

        for after in sorted(card.afters):
            for before in sorted(card.befores):
                if before == after or before in ancestors_for(after, civics, ancestor_cache):
                    errors.append(
                        f"{card.name}: impossible gate after [{after}] before [{before}]"
                    )

        for before in sorted(card.befores):
            if (card.name, before) not in removals:
                errors.append(
                    f"{card.name}: missing removal trigger after adopting [{before}]"
                )

        for effect_before in sorted(card.effect_befores - card.befores):
            errors.append(
                f"{card.name}: effect expires before adopting [{effect_before}] "
                "but the card itself does not"
            )

        for comment in card.comments:
            if comment.startswith("Obsoletes:") and " and " in comment:
                errors.append(
                    f"{card.name}: use comma-style obsolete comment wording, got [{comment}]"
                )

    for card_name, civic in sorted(removals):
        card = cards.get(card_name)
        if card is not None and civic not in card.befores:
            errors.append(
                f"{card_name}: removal after [{civic}] has no matching before gate"
            )

    for check in SMOKE_CHECKS:
        civic = check["civic"]
        if civic not in civics:
            errors.append(f"smoke {civic}: unknown civic")
            continue

        adopted = ancestors_for(civic, civics, ancestor_cache) | {civic}
        adopted.update(check.get("extra_adopted", []))

        for card_name in check["available"]:
            card = cards.get(card_name)
            if card is None:
                errors.append(f"smoke {civic}: missing card [{card_name}]")
            elif not is_available(card, adopted):
                errors.append(f"smoke {civic}: expected [{card_name}] to be available")

        for card_name in check["unavailable"]:
            card = cards.get(card_name)
            if card is None:
                errors.append(f"smoke {civic}: missing card [{card_name}]")
            elif is_available(card, adopted):
                errors.append(f"smoke {civic}: expected [{card_name}] to be unavailable")

        for removal in check["removed"]:
            if removal not in removals:
                errors.append(
                    f"smoke {civic}: missing removal trigger [{removal[0]}] after [{removal[1]}]"
                )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate policy card obsolete gates, removal triggers, and smoke "
            "checks for the Civ6-mod policy data."
        )
    )
    parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    policies_text = strip_comments((repo_root / "jsons" / "Policies.json").read_text())
    buildings_text = strip_comments((repo_root / "jsons" / "Buildings.json").read_text())

    civics = parse_civics(policies_text)
    cards = parse_policy_cards(buildings_text)
    removals = parse_removals(policies_text)
    errors = validate(civics, cards, removals)

    if errors:
        print("Policy obsolescence validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(
        "Policy obsolescence validation passed "
        f"({len(cards)} policy cards, {len(civics)} civics, {len(SMOKE_CHECKS)} smoke checks)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
