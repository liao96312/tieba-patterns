#!/usr/bin/env python3
"""Match Tieba comments to an existing Markdown pattern library."""

from __future__ import annotations

import argparse
import difflib
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

HEADING = re.compile(r"^###\s+\d+(?:-\d+)?\.\s+(.+?)\s*$")
PATTERN = re.compile(r"^\*\*Pattern\*\*:\s*(.+?)\s*$")
EXAMPLE = re.compile(r"^-\s+(?:原句|拓展)：\s*(.+?)\s*$")
URL = re.compile(r"https?://\S+|www\.\S+", re.I)
SPACE = re.compile(r"\s+")
REPLY_PREFIX = re.compile(r"^回复\s+[^:：]{1,40}\s*[:：]\s*")
SLOT = re.compile(r"\[[^\]]+\]|[XY…]+|\.{2,}")
PUNCT = re.compile(r"[\W_]+", re.UNICODE)


def normalize(value: object) -> str:
    text = unicodedata.normalize("NFKC", str(value or ""))
    text = URL.sub("", text)
    text = REPLY_PREFIX.sub("", text)
    return SPACE.sub(" ", text).strip()


def compact(text: str) -> str:
    return PUNCT.sub("", SLOT.sub("", normalize(text))).casefold()


def bigrams(text: str) -> set[str]:
    return {text[i : i + 2] for i in range(max(0, len(text) - 1))}


def similarity(left: str, right: str) -> float:
    left, right = compact(left), compact(right)
    if not left or not right:
        return 0.0
    ratio = difflib.SequenceMatcher(None, left, right).ratio()
    a, b = bigrams(left), bigrams(right)
    jaccard = len(a & b) / len(a | b) if a and b else 0.0
    containment = min(len(left), len(right)) / max(len(left), len(right))
    return 0.6 * ratio + 0.3 * jaccard + 0.1 * containment


def load_patterns(path: Path) -> dict[str, dict[str, list[str]]]:
    patterns: dict[str, dict[str, list[str]]] = defaultdict(
        lambda: {"templates": [], "examples": []}
    )
    section = ""
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if match := HEADING.match(line):
            section = match.group(1)
        elif section and (match := PATTERN.match(line)):
            patterns[section]["templates"].append(match.group(1))
        elif section and (match := EXAMPLE.match(line)):
            patterns[section]["examples"].append(match.group(1))
    return dict(patterns)


def anchors(template: str) -> list[str]:
    pieces = re.split(
        r"\[[^\]]+\]|[XY…]+|\.{2,}|[+，,。？?!！:：/（）()]",
        normalize(template),
    )
    return [value for piece in pieces if len(value := compact(piece)) >= 3]


def read_jsonl(paths: list[Path]):
    for path in paths:
        with path.open(encoding="utf-8-sig") as source:
            for line in source:
                if line.strip():
                    yield json.loads(line)


def match_comments(
    pattern_map: dict[str, dict[str, list[str]]],
    posts: list[dict],
    comments: list[dict],
    threshold: float,
    per_pattern: int,
) -> list[dict]:
    post_map = {str(row.get("note_id", "")): row for row in posts}
    frequencies = Counter(
        compact(normalize(row.get("content")))
        for row in comments
        if compact(normalize(row.get("content")))
    )
    seen_ids: set[str] = set()
    seen_text: set[str] = set()
    buckets: dict[str, list[dict]] = defaultdict(list)

    for row in comments:
        comment_id = str(row.get("comment_id", ""))
        content = normalize(row.get("content"))
        key = compact(content)
        if (
            not key
            or len(content) < 3
            or len(content) > 180
            or comment_id in seen_ids
            or key in seen_text
        ):
            continue
        seen_ids.add(comment_id)
        seen_text.add(key)

        best_name, best_score = "", 0.0
        for name, spec in pattern_map.items():
            candidates = spec["templates"] + spec["examples"]
            score = max((similarity(content, item) for item in candidates), default=0.0)
            fixed = [
                anchor
                for template in spec["templates"]
                for anchor in anchors(template)
            ]
            if not any(anchor in key for anchor in fixed) and score < 0.55:
                continue
            if score > best_score:
                best_name, best_score = name, score
        if best_score < threshold:
            continue

        note_id = str(row.get("note_id", ""))
        post = post_map.get(note_id, {})
        buckets[best_name].append(
            {
                "pattern": best_name,
                "score": round(best_score, 4),
                "tieba_name": row.get("tieba_name") or post.get("tieba_name", ""),
                "note_id": note_id,
                "note_title": normalize(post.get("title") or post.get("desc")),
                "comment_id": comment_id,
                "parent_comment_id": str(row.get("parent_comment_id", "")),
                "publish_time": row.get("publish_time", ""),
                "sub_comment_count": row.get("sub_comment_count", 0),
                "frequency": frequencies[key],
                "content": content,
            }
        )

    selected: list[dict] = []
    for rows in buckets.values():
        selected.extend(sorted(rows, key=lambda item: item["score"], reverse=True)[:per_pattern])
    return sorted(selected, key=lambda item: (item["pattern"], -item["score"]))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--patterns", required=True, type=Path)
    parser.add_argument("--posts", required=True, nargs="+", type=Path)
    parser.add_argument("--comments", required=True, nargs="+", type=Path)
    parser.add_argument("--threshold", type=float, default=0.32)
    parser.add_argument("--per-pattern", type=int, default=25)
    parser.add_argument("-o", "--output", required=True, type=Path)
    args = parser.parse_args()

    patterns = load_patterns(args.patterns)
    posts = list(read_jsonl(args.posts))
    comments = list(read_jsonl(args.comments))
    matched = match_comments(
        patterns, posts, comments, args.threshold, args.per_pattern
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as output:
        for row in matched:
            output.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(
        f"{len(patterns)} patterns, {len(comments)} comments, "
        f"{len(matched)} matched -> {args.output}"
    )


if __name__ == "__main__":
    main()
