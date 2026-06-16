# Validation

Run relevant checks before opening a PR, especially after changing policy cards, civic unlocks, or ruleset data.

## Policy Obsolescence Check

```sh
scripts/check-policy-obsolescence.py
```

This script checks that obsolete policy-card data stays synchronized across:

- card-level availability gates in `jsons/Buildings.json`
- civic removal triggers in `jsons/Policies.json`
- effect-level cutoff conditions
- visible `Comment [Obsoletes: ...]` wording
- smoke scenarios around known obsolete-policy civics

The same check runs in GitHub Actions for pull requests that touch policy data, the script, or the workflow.

## Unciv Mod Validation

If you have a built Unciv desktop jar, run Unciv's mod validator from the mod root:

```sh
java -jar /path/to/Unciv/desktop/build/libs/Unciv.jar mod-ci
```

`mod-ci` may report existing warnings for colors, duplicate names, image atlas generation, or placeholder uniques. New errors should be treated as blockers.

## Before Pushing

- Run the most specific validation for the files you changed.
- Note any known pre-existing warnings in the PR.
- If a validation script fails because it intentionally depends on another PR, call that out in the PR description.
