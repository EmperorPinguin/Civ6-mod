# Issue Triage Draft

Last scanned: 2026-06-16

Scope: all open and closed GitHub issues visible in the repository issue list. This is an issue-thread and static-data scan, not a full in-game retest. Statuses below should be treated as cleanup guidance before closing or splitting issues.

## Summary

- Scanned 32 issues: 19 open and 13 closed.
- Several open issues look stale because a fix was merged or the maintainer answered the question.
- The largest cleanup opportunity is to split broad/mixed issues into smaller tickets with one repro or one project per issue.
- The highest-signal active work appears to be district construction/automation, remaining unit upgrade validation warnings, art assets, translation completion, and a few gameplay/design decisions.

## Recommended Cleanup Pass

1. Close confirmed fixed open issues after a quick maintainer check: [#48](https://github.com/EmperorPinguin/Civ6-mod/issues/48), [#52](https://github.com/EmperorPinguin/Civ6-mod/issues/52), [#69](https://github.com/EmperorPinguin/Civ6-mod/issues/69), [#96](https://github.com/EmperorPinguin/Civ6-mod/issues/96), [#97](https://github.com/EmperorPinguin/Civ6-mod/issues/97), and [#100](https://github.com/EmperorPinguin/Civ6-mod/issues/100).
2. Split umbrella/mixed issues into focused tickets: [#7](https://github.com/EmperorPinguin/Civ6-mod/issues/7) and [#67](https://github.com/EmperorPinguin/Civ6-mod/issues/67).
3. Keep current limitation/design issues open only if they have an agreed target; otherwise convert them to a project backlog note: [#12](https://github.com/EmperorPinguin/Civ6-mod/issues/12), [#16](https://github.com/EmperorPinguin/Civ6-mod/issues/16), [#45](https://github.com/EmperorPinguin/Civ6-mod/issues/45), [#46](https://github.com/EmperorPinguin/Civ6-mod/issues/46), and [#104](https://github.com/EmperorPinguin/Civ6-mod/issues/104).
4. Add FAQ entries for repeated player questions: districts, policies, envoys, Natural Wonder graphics, validation warnings, promotion strength conversion, and missing later civs/leaders.
5. Track open project buckets separately from bugs: translation, art assets, ruleset validation, district construction, and future Unciv engine support.

## Active Buckets

### Districts And Construction

- [#53](https://github.com/EmperorPinguin/Civ6-mod/issues/53) and possibly [#13](https://github.com/EmperorPinguin/Civ6-mod/issues/13) point at district construction becoming desynchronized from the city queue.
- Upstream Unciv PR [yairm210/Unciv#14996](https://github.com/yairm210/Unciv/pull/14996) is open and approved but not merged as of this scan.
- [#100](https://github.com/EmperorPinguin/Civ6-mod/issues/100) was fixed by merged PR [#105](https://github.com/EmperorPinguin/Civ6-mod/pull/105): district capacity no longer double-counts district slots.

### Validation Warnings

- The city-state unique warnings from [#97](https://github.com/EmperorPinguin/Civ6-mod/issues/97) were fixed by merged PR [#107](https://github.com/EmperorPinguin/Civ6-mod/pull/107).
- Unit promotion circular-reference warnings were resolved upstream by merged Unciv PR [yairm210/Unciv#14995](https://github.com/yairm210/Unciv/pull/14995).
- [#20](https://github.com/EmperorPinguin/Civ6-mod/issues/20) should stay open until the current mod-ci validator is rerun. Static scan still shows suspicious unit upgrade/obsolete pairings such as Catapult to Bombard and Frigate variants to Battleship.

### Translations

- [#8](https://github.com/EmperorPinguin/Civ6-mod/issues/8) is the Indonesian translation issue. The template exists and Indonesian has many filled entries, but it is still incomplete and needs native-speaker review.
- [#19](https://github.com/EmperorPinguin/Civ6-mod/issues/19) is the Russian translation issue. `Russian.properties` exists, but the static count was 264 filled entries and 1015 empty entries out of 1279 total.

### Art Assets

- [#54](https://github.com/EmperorPinguin/Civ6-mod/issues/54) is the main art backlog: resource quality concerns and missing Natural Wonder sprites causing black tiles.
- [#96](https://github.com/EmperorPinguin/Civ6-mod/issues/96) appears stale because `Man-At-Arms.png` exists.
- [#90](https://github.com/EmperorPinguin/Civ6-mod/issues/90) is closed and current assets include Garde Imperiale unit images.

## Issue Inventory

| Issue | State | Triage | Notes / Next Action |
| --- | --- | --- | --- |
| [#6 Bug](https://github.com/EmperorPinguin/Civ6-mod/issues/6) | Closed | Current limitation | District pillage can free the tile while building bonuses remain. Maintainer noted this was limited by available uniques. Keep as future engine/modding limitation unless new support exists. |
| [#7 Couple of issues](https://github.com/EmperorPinguin/Civ6-mod/issues/7) | Open | Split / stale umbrella | Many original bullets are fixed or accepted by design. Split remaining work: roads on districts under construction, map-mode/Natural Wonder icons, Great Person point report, Great Prophet economy, broad balance, post-Renaissance wonders, and Relics. |
| [#8 Can you translate the civ6 mod?](https://github.com/EmperorPinguin/Civ6-mod/issues/8) | Open | Translation backlog | Indonesian file exists and is mostly keyed, but still has many blanks and needs native-speaker review. Preserve/Archaeological Dig warning subtopic is stale. |
| [#10 The Archeological Dig](https://github.com/EmperorPinguin/Civ6-mod/issues/10) | Closed | Resolved | Archaeological Dig and Preserve no-stat warnings were addressed by adding yields. Current data includes yields. |
| [#12 I have some question](https://github.com/EmperorPinguin/Civ6-mod/issues/12) | Open | FAQ / current limitation | Envoy mechanic was answered; Religious Victory exists but is hidden from victory screen; Builder charges remain an Unciv/current-limitation topic. Add FAQ and split Builder charges only if someone wants to pursue it. |
| [#13 Production on districts keeps stopping](https://github.com/EmperorPinguin/Civ6-mod/issues/13) | Open | Needs repro / possible duplicate | User reported district queue dropping while progress remains. Could be related to [#53](https://github.com/EmperorPinguin/Civ6-mod/issues/53) and upstream [yairm210/Unciv#14996](https://github.com/yairm210/Unciv/pull/14996), but not proven. Ask for current Unciv version/save after upstream lands. |
| [#15 Circular dependency between Factory and power plants](https://github.com/EmperorPinguin/Civ6-mod/issues/15) | Closed | Resolved | Current Factory and Electronics Factory require Workshop, not Power. Power plants require Factory. |
| [#16 Other Civs](https://github.com/EmperorPinguin/Civ6-mod/issues/16) | Closed | Future project | Later civs such as Portugal were noted as difficult because mechanics are specialized and the mod was not actively developed. Keep as future expansion backlog. |
| [#19 Hello](https://github.com/EmperorPinguin/Civ6-mod/issues/19) | Open | Translation backlog | Russian translation exists but is incomplete. Static count: 264 filled, 1015 empty, 1279 total. |
| [#20 Mod errors](https://github.com/EmperorPinguin/Civ6-mod/issues/20) | Open | Needs validator rerun | Maintainer said an update should fix unit upgrade warnings. Static scan still shows possible upgrade/obsolete mismatches for siege and naval ranged lines. Keep open until mod-ci confirms. |
| [#39 Mod errors](https://github.com/EmperorPinguin/Civ6-mod/issues/39) | Closed | Stale validator report | Reporter found the cause and planned a PR. Treat as historical unless current validator reproduces the same messages. |
| [#43 Issue with Macedonia encampment district](https://github.com/EmperorPinguin/Civ6-mod/issues/43) | Closed | Resolved / install issue | Reinstall/update resolved the crash report. Likely stale local data rather than current mod data. |
| [#45 Question](https://github.com/EmperorPinguin/Civ6-mod/issues/45) | Closed | Current limitation | John Curtin/Australia leader ability was omitted because it was not implementable cleanly with current mechanics. |
| [#46 Question](https://github.com/EmperorPinguin/Civ6-mod/issues/46) | Closed | Future project | Vietnam/Babylon and future nations need specialized mechanics. Could become a larger expansion project. |
| [#47 Error in game](https://github.com/EmperorPinguin/Civ6-mod/issues/47) | Closed | Resolved | Road/Railroad missing tech crash was fixed by Road unlocking at Wheel; user confirmed. |
| [#48 Question](https://github.com/EmperorPinguin/Civ6-mod/issues/48) | Open | Close candidate | Ilkum typo appears fixed. Current data makes Ilkum available before Feudalism and removes it on Feudalism. |
| [#49 Question](https://github.com/EmperorPinguin/Civ6-mod/issues/49) | Open | FAQ / docs | Melee vs anti-cavalry bonuses are modeled in unit type data, but Civilopedia clarity is still useful. Add FAQ/Civilopedia note. |
| [#50 Policies](https://github.com/EmperorPinguin/Civ6-mod/issues/50) | Open | FAQ / needs repro | Policies are modeled as capital buildings. FAQ should explain buying government and policy cards, then retest on current Unciv if players still cannot buy policies. |
| [#52 Question](https://github.com/EmperorPinguin/Civ6-mod/issues/52) | Open | Close candidate / FAQ | Maintainer answered strength conversion: about +10 Civ VI strength maps to +67% in Unciv, +30 maps to about +200%. |
| [#53 districs problems](https://github.com/EmperorPinguin/Civ6-mod/issues/53) | Open | Upstream dependency | Districts are built through city construction, not workers. Later investigation found worker automation can orphan `CreatesOneImprovement` markers; upstream [yairm210/Unciv#14996](https://github.com/yairm210/Unciv/pull/14996) is the likely fix path. |
| [#54 Change the tiles graphics](https://github.com/EmperorPinguin/Civ6-mod/issues/54) | Open | Art backlog | Resource sprites and missing Natural Wonder sprites. Maintainer can merge art PRs; Civ6 Tileset covers many Natural Wonders separately. |
| [#58 tilefilter errors](https://github.com/EmperorPinguin/Civ6-mod/issues/58) | Closed | Stale validator report | Yellow warnings were from deprecated uniques in Unciv 4.10.03/4.11.18. Treat as historical unless current validator reproduces them. |
| [#65 Bug: Japan cannot get electricity resources](https://github.com/EmperorPinguin/Civ6-mod/issues/65) | Closed | Resolved | Maintainer removed the unexplained requirement. Current Electronics Factory does not require Power. |
| [#67 isssue](https://github.com/EmperorPinguin/Civ6-mod/issues/67) | Open | Split mixed issue | Six unrelated reports. Bomber to Jet Bomber appears fixed. Districts are now irremovable. Light Cavalry still appears to use Heavy Cavalry prerequisite names. Catapult path, Great Prophet behavior, and Lumber mill/Reclaimed Forest should become separate tickets if still desired. |
| [#69 error downloading the mod](https://github.com/EmperorPinguin/Civ6-mod/issues/69) | Open | Close candidate | Maintainer fixed the download issue and reporter confirmed redownloading worked. |
| [#73 Changing Policies](https://github.com/EmperorPinguin/Civ6-mod/issues/73) | Closed | Resolved / FAQ | Policy switching can be handled by selling policy buildings and buying new ones. A later PR/comment said this should be resolved. Keep player-facing FAQ. |
| [#90 Garde Imperial](https://github.com/EmperorPinguin/Civ6-mod/issues/90) | Closed | Resolved art asset | Current assets include Garde Imperiale unit images. |
| [#96 No image for Man-At-Arms](https://github.com/EmperorPinguin/Civ6-mod/issues/96) | Open | Close candidate | Current assets include `Man-At-Arms.png`. Confirm in-game rendering before closing if desired. |
| [#97 Problem with the mod](https://github.com/EmperorPinguin/Civ6-mod/issues/97) | Open | Close candidate | Promotion circular warnings are resolved upstream by [yairm210/Unciv#14995](https://github.com/yairm210/Unciv/pull/14995). The three city-state validation warnings were fixed by merged PR [#107](https://github.com/EmperorPinguin/Civ6-mod/pull/107). |
| [#100 Districts and population](https://github.com/EmperorPinguin/Civ6-mod/issues/100) | Open | Close candidate | Fixed by merged PR [#105](https://github.com/EmperorPinguin/Civ6-mod/pull/105). District capacity now uses city-based thresholds and no longer double-consumes district slots. |
| [#101 Desert folklore, Dance of Aurora in the holy site of the Khmer](https://github.com/EmperorPinguin/Civ6-mod/issues/101) | Open | Active design/data question | Khmer food-from-Faith-adjacency appears to include pantheon-added Holy Site adjacency. Needs decision: intended approximation or bug to exclude belief adjacency from food conversion. |
| [#104 Question: preferred approach for district trade route yields?](https://github.com/EmperorPinguin/Civ6-mod/issues/104) | Open | Current limitation / future design | Maintainer prefers not to mainline a temporary connected-city route approximation while waiting for BNW trade route support in Unciv. Keep as design backlog unless a temporary approximation is explicitly wanted. |

## Candidate New Issues

- District queue desync after worker automation: track upstream [yairm210/Unciv#14996](https://github.com/yairm210/Unciv/pull/14996), then retest Civ6-mod [#13](https://github.com/EmperorPinguin/Civ6-mod/issues/13) and [#53](https://github.com/EmperorPinguin/Civ6-mod/issues/53).
- Unit upgrade/obsolete validation warnings: retest [#20](https://github.com/EmperorPinguin/Civ6-mod/issues/20) with current mod-ci and fix remaining siege/naval lines.
- Light Cavalry promotion prerequisites: split from [#67](https://github.com/EmperorPinguin/Civ6-mod/issues/67).
- Khmer Holy Site adjacency conversion: resolve [#101](https://github.com/EmperorPinguin/Civ6-mod/issues/101) with a design decision and targeted data change if needed.
- Natural Wonder and resource sprite backlog: split [#54](https://github.com/EmperorPinguin/Civ6-mod/issues/54) into asset checklist issues.
- Translation completion checklists: split Indonesian [#8](https://github.com/EmperorPinguin/Civ6-mod/issues/8) and Russian [#19](https://github.com/EmperorPinguin/Civ6-mod/issues/19) into language-specific contribution tasks.
