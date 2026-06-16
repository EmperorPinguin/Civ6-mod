#!/usr/bin/env python3
"""Generate a deterministic GitHub issue triage snapshot.

This script is intentionally heuristic. It creates a current issue inventory and
points maintainers at likely stale/fixed issues, but it does not replace the
human-edited triage notes in docs/IssueTriage.md or FAQ in docs/FAQ.md.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import textwrap
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from typing import Any


API_ROOT = "https://api.github.com"


@dataclass
class Comment:
    body: str
    author: str
    author_association: str
    created_at: str


@dataclass
class Issue:
    number: int
    title: str
    state: str
    url: str
    body: str
    created_at: str
    updated_at: str
    closed_at: str | None
    labels: list[str]
    comments_count: int
    comments: list[Comment] = field(default_factory=list)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo",
        default=os.environ.get("GITHUB_REPOSITORY", "EmperorPinguin/Civ6-mod"),
        help="Repository in owner/name form. Defaults to GITHUB_REPOSITORY.",
    )
    parser.add_argument(
        "--output",
        default="docs/IssueTriageSnapshot.md",
        help="Markdown file to write.",
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN"),
        help="GitHub token. Defaults to GITHUB_TOKEN or GH_TOKEN.",
    )
    parser.add_argument(
        "--today",
        default=dt.datetime.now(dt.timezone.utc).date().isoformat(),
        help="Date to use in generated output, mainly for tests.",
    )
    return parser.parse_args()


class GitHubClient:
    def __init__(self, token: str | None) -> None:
        self.token = token

    def get_json(self, path: str, params: dict[str, str] | None = None) -> Any:
        query = f"?{urllib.parse.urlencode(params)}" if params else ""
        url = f"{API_ROOT}{path}{query}"
        request = urllib.request.Request(url)
        request.add_header("Accept", "application/vnd.github+json")
        request.add_header("X-GitHub-Api-Version", "2022-11-28")
        request.add_header("User-Agent", "Civ6-mod issue triage snapshot")
        if self.token:
            request.add_header("Authorization", f"Bearer {self.token}")

        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            details = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"GitHub API request failed: {exc.code} {url}\n{details}") from exc

    def get_all_pages(self, path: str, params: dict[str, str] | None = None) -> list[Any]:
        params = dict(params or {})
        params.setdefault("per_page", "100")
        page = 1
        results: list[Any] = []

        while True:
            params["page"] = str(page)
            batch = self.get_json(path, params)
            if not batch:
                return results
            results.extend(batch)
            if len(batch) < int(params["per_page"]):
                return results
            page += 1

    def get_json_or_none(self, path: str, params: dict[str, str] | None = None) -> Any | None:
        try:
            return self.get_json(path, params)
        except RuntimeError as exc:
            # Linked PR checks are best-effort. A repo-scoped Actions token may
            # not be allowed to read public PRs in another repository, and that
            # should not fail the whole issue snapshot refresh.
            if "GitHub API request failed: 403" in str(exc) or "GitHub API request failed: 404" in str(exc):
                return None
            raise


def fetch_issues(client: GitHubClient, repo: str) -> list[Issue]:
    # GitHub's issues endpoint also returns pull requests, so this pass builds
    # a normalized issue-only model and fetches comments for each issue.
    raw_issues = client.get_all_pages(
        f"/repos/{repo}/issues",
        {
            "state": "all",
            "sort": "created",
            "direction": "asc",
        },
    )

    issues: list[Issue] = []
    for raw_issue in raw_issues:
        # Pull requests have their own workflow and should not be mixed into
        # issue-cleanup counts or stale-issue heuristics.
        if "pull_request" in raw_issue:
            continue

        number = raw_issue["number"]
        raw_comments = client.get_all_pages(f"/repos/{repo}/issues/{number}/comments")
        comments = [
            Comment(
                body=comment.get("body") or "",
                author=(comment.get("user") or {}).get("login") or "",
                author_association=comment.get("author_association") or "",
                created_at=comment.get("created_at") or "",
            )
            for comment in raw_comments
        ]

        issues.append(
            Issue(
                number=number,
                title=raw_issue["title"],
                state=raw_issue["state"],
                url=raw_issue["html_url"],
                body=raw_issue.get("body") or "",
                created_at=raw_issue["created_at"],
                updated_at=raw_issue["updated_at"],
                closed_at=raw_issue.get("closed_at"),
                labels=[label["name"] for label in raw_issue.get("labels", [])],
                comments_count=raw_issue.get("comments", len(comments)),
                comments=comments,
            )
        )

    return sorted(issues, key=lambda issue: issue.number)


def markdown_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def date_only(timestamp: str | None) -> str:
    if not timestamp:
        return ""
    return timestamp[:10]


def days_since(timestamp: str, today: dt.date) -> int:
    updated = dt.datetime.fromisoformat(timestamp.replace("Z", "+00:00")).date()
    return (today - updated).days


def plain_summary(markdown: str, limit: int = 150) -> str:
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", markdown)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"#+\s*", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "..."


def issue_markdown(issue: Issue) -> str:
    comments = "\n".join(comment.body for comment in issue.comments)
    return f"{issue.title}\n{issue.body}\n{comments}"


def issue_text(issue: Issue) -> str:
    return issue_markdown(issue).lower()


def owner_text(issue: Issue) -> str:
    # Maintainer/collaborator comments carry more signal for "fixed" wording
    # than reporter comments such as "is this fixed yet?".
    relevant_comments = [
        comment.body
        for comment in issue.comments
        if comment.author_association in {"OWNER", "MEMBER", "COLLABORATOR"}
    ]
    return "\n".join(relevant_comments).lower()


def linked_pull_requests(issue: Issue, default_repo: str) -> list[tuple[str, int]]:
    text = issue_markdown(issue)
    refs: set[tuple[str, int]] = set()

    for owner, name, number in re.findall(r"https://github\.com/([^/\s]+)/([^/\s]+)/pull/(\d+)", text, re.IGNORECASE):
        refs.add((f"{owner}/{name}", int(number)))
    for repo, number in re.findall(r"\b([a-z0-9_.-]+/[a-z0-9_.-]+)#(\d+)\b", text, re.IGNORECASE):
        refs.add((repo, int(number)))
    for number in re.findall(r"(?<![\w/])#(\d+)\b", text):
        refs.add((default_repo, int(number)))

    return sorted(refs)


def merged_pull_requests(client: GitHubClient, issue: Issue, default_repo: str) -> list[tuple[str, int]]:
    merged: list[tuple[str, int]] = []
    for repo, number in linked_pull_requests(issue, default_repo):
        pull_request = client.get_json_or_none(f"/repos/{repo}/pulls/{number}")
        if pull_request and pull_request.get("merged_at"):
            merged.append((repo, number))
    return merged


def close_candidate_reason(client: GitHubClient, repo: str, issue: Issue) -> str | None:
    # This is intentionally conservative and explainable. The script points at
    # issues that deserve human review; it never closes or labels anything.
    text = issue_text(issue)
    maintainer_text = owner_text(issue)

    if re.search(r"\b(can|should)\s+be\s+closed\b|\bcan\s+close\b|\bi think this can be closed\b", text):
        return "Comment suggests it can be closed"
    if re.search(r"\b(no longer an issue|resolved|fixed it|fixed this|should now be fixed)\b", maintainer_text):
        return "Maintainer/comment thread says fixed or resolved"
    if re.search(r"\bdownloading the mod again should solve\b|\bredownloading\b", maintainer_text):
        return "Maintainer says redownload/update resolves it"
    if re.search(r"\b(fixed|resolve|resolves|should resolve|pr)\b", text):
        merged = merged_pull_requests(client, issue, repo)
        if merged:
            references = ", ".join(f"{ref_repo}#{number}" for ref_repo, number in merged)
            return f"Linked merged PR: {references}"
    return None


TOPIC_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    # Topic buckets are broad by design. They help decide where FAQ entries or
    # focused follow-up issues may be useful, not whether an issue is valid.
    ("Districts / construction", re.compile(r"\bdistrict|createsoneimprovement|construction queue|under construction")),
    ("Policies / governments", re.compile(r"\bpolic|government|civic|ilkum|feudalism")),
    ("Validation warnings", re.compile(r"\berror|warning|validator|mod-ci|obsolete|upgrade")),
    ("Translations", re.compile(r"\btranslat|language|russian|indonesian|properties")),
    ("Art / graphics", re.compile(r"\bimage|graphic|sprite|tileset|icon|black tile|natural wonder")),
    ("Religion", re.compile(r"\breligio|prophet|holy site|pantheon|belief|envoy")),
    ("Civs / leaders", re.compile(r"\bciv\b|leader|portugal|babylon|vietnam|australia|john curtin")),
    ("Trade routes", re.compile(r"\btrade route|bnw")),
]


def topic_matches(issues: list[Issue]) -> list[tuple[str, list[Issue]]]:
    matches: list[tuple[str, list[Issue]]] = []
    for topic, pattern in TOPIC_PATTERNS:
        topic_issues = [issue for issue in issues if pattern.search(issue_text(issue))]
        if topic_issues:
            matches.append((topic, topic_issues))
    return matches


def issue_link(issue: Issue) -> str:
    return f"[#{issue.number}]({issue.url})"


def render_issue_table(issues: list[Issue], include_state: bool = True) -> list[str]:
    header = "| Issue | State | Updated | Comments | Summary |" if include_state else "| Issue | Updated | Comments | Summary |"
    separator = "| --- | --- | --- | --- | --- |" if include_state else "| --- | --- | --- | --- |"
    lines = [header, separator]
    for issue in issues:
        summary = markdown_escape(plain_summary(issue.body or issue.title))
        title = markdown_escape(issue.title)
        if include_state:
            lines.append(
                f"| {issue_link(issue)} {title} | {issue.state} | {date_only(issue.updated_at)} | {issue.comments_count} | {summary} |"
            )
        else:
            lines.append(
                f"| {issue_link(issue)} {title} | {date_only(issue.updated_at)} | {issue.comments_count} | {summary} |"
            )
    return lines


def render_snapshot(client: GitHubClient, repo: str, issues: list[Issue], today_text: str) -> str:
    # Keep date math internal to stale-bucket decisions. The rendered snapshot
    # avoids "generated at" timestamps or "N days ago" text so scheduled runs do
    # not create PRs unless issue data actually changed.
    today = dt.date.fromisoformat(today_text)
    open_issues = [issue for issue in issues if issue.state == "open"]
    closed_issues = [issue for issue in issues if issue.state == "closed"]
    close_candidates = [
        (issue, reason)
        for issue in open_issues
        if (reason := close_candidate_reason(client, repo, issue)) is not None
    ]
    stale_open = [
        issue
        for issue in open_issues
        if days_since(issue.updated_at, today) >= 180 and issue not in [candidate for candidate, _ in close_candidates]
    ]
    recently_updated = sorted(open_issues, key=lambda issue: issue.updated_at, reverse=True)[:10]

    latest_issue_update = max((date_only(issue.updated_at) for issue in issues), default="")
    lines = [
        "# Generated Issue Triage Snapshot",
        "",
        f"Repository: [{repo}](https://github.com/{repo})",
        f"Latest issue update: {latest_issue_update}",
        "",
        "> This file is generated by `scripts/generate_issue_triage.py`. Edit `docs/IssueTriage.md` and `docs/FAQ.md` for human-curated triage and support guidance.",
        "",
        "## Summary",
        "",
        f"- Total issues: {len(issues)}",
        f"- Open issues: {len(open_issues)}",
        f"- Closed issues: {len(closed_issues)}",
        f"- Heuristic close candidates: {len(close_candidates)}",
        f"- Open issues not updated in 180+ days: {len(stale_open)}",
        "",
    ]

    lines.extend(
        [
            "## Heuristic Close Candidates",
            "",
            "These are not automatic close decisions. They are issues whose thread text looks resolved or references a merged PR.",
            "",
        ]
    )
    if close_candidates:
        lines.extend(["| Issue | Updated | Reason |", "| --- | --- | --- |"])
        for issue, reason in close_candidates:
            lines.append(
                f"| {issue_link(issue)} {markdown_escape(issue.title)} | {date_only(issue.updated_at)} | {markdown_escape(reason)} |"
            )
    else:
        lines.append("No close candidates detected.")
    lines.append("")

    lines.extend(["## FAQ / Topic Candidates", ""])
    for topic, topic_issues in topic_matches(open_issues):
        links = ", ".join(issue_link(issue) for issue in topic_issues)
        lines.append(f"- {topic}: {links}")
    lines.append("")

    lines.extend(["## Recently Updated Open Issues", ""])
    if recently_updated:
        lines.extend(render_issue_table(recently_updated, include_state=False))
    else:
        lines.append("No open issues.")
    lines.append("")

    lines.extend(["## Stale Open Issues", ""])
    if stale_open:
        lines.extend(render_issue_table(stale_open, include_state=False))
    else:
        lines.append("No open issues older than 180 days outside the close-candidate list.")
    lines.append("")

    lines.extend(["## Open Issue Inventory", ""])
    if open_issues:
        lines.extend(render_issue_table(open_issues, include_state=False))
    else:
        lines.append("No open issues.")
    lines.append("")

    lines.extend(["## Closed Issue Inventory", ""])
    if closed_issues:
        lines.extend(render_issue_table(closed_issues, include_state=False))
    else:
        lines.append("No closed issues.")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    if "/" not in args.repo:
        print("--repo must be in owner/name form", file=sys.stderr)
        return 2

    # Main workflow: fetch issue data, render a deterministic Markdown snapshot,
    # then write it to disk for GitHub Actions to PR if it changed.
    client = GitHubClient(args.token)
    issues = fetch_issues(client, args.repo)
    snapshot = render_snapshot(client, args.repo, issues, args.today)

    output_path = args.output
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as output:
        output.write(snapshot.rstrip())
        output.write("\n")

    print(
        textwrap.dedent(
            f"""\
            Wrote {output_path}
            Issues scanned: {len(issues)}
            Open: {sum(1 for issue in issues if issue.state == "open")}
            Closed: {sum(1 for issue in issues if issue.state == "closed")}
            """
        ).strip()
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
