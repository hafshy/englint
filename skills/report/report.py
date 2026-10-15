#!/usr/bin/env python3
"""Print the Englint prompts logged in a time range, one per line, for the report skill.

Usage: report.py [today | yesterday | week | last week | month | last month | 7d | all
                  | YYYY-MM-DD | YYYY-MM-DD..YYYY-MM-DD]
"""
import json
import os
import re
import sys
from datetime import date, datetime, time, timedelta

DATA_DIR = os.path.expanduser("~/.claude/englint")
# ponytail: newest 300 prompts only; sample across the range if long reports need older ones too.
MAX_PROMPTS = 300
MAX_CHARS = 400  # long prompts are mostly pasted content


def day_start(d, tz):
    return datetime.combine(d, time.min, tz)


def parse_range(arg, now):
    """Return (start, end) as aware datetimes; start None means 'from the beginning'."""
    tz = now.tzinfo
    today = day_start(now.date(), tz)
    arg = re.sub(r"[\s_]+", "-", arg.strip().lower()).replace("this-", "") or "week"
    if arg == "today":
        return today, now
    if arg == "yesterday":
        return today - timedelta(days=1), today
    if arg == "week":
        return today - timedelta(days=today.weekday()), now
    if arg == "last-week":
        start = today - timedelta(days=today.weekday() + 7)
        return start, start + timedelta(days=7)
    if arg == "month":
        return today.replace(day=1), now
    if arg == "last-month":
        end = today.replace(day=1)
        return (end - timedelta(days=1)).replace(day=1), end
    if arg == "all":
        return None, now
    m = re.fullmatch(r"(?:last-)?(\d+)-?d(?:ays?)?", arg)
    if m:
        return today - timedelta(days=int(m.group(1)) - 1), now
    first, _, last = arg.partition("..")
    start = date.fromisoformat(first)
    end = date.fromisoformat(last) if last else start
    return day_start(start, tz), day_start(end, tz) + timedelta(days=1)


def main():
    now = datetime.now().astimezone()
    try:
        start, end = parse_range(" ".join(sys.argv[1:]), now)
    except ValueError:
        sys.exit(f"Unknown range: {' '.join(sys.argv[1:])!r}. " + __doc__.split("\n\n")[1])

    try:
        with open(os.path.join(DATA_DIR, "config.json"), encoding="utf-8") as f:
            print("Settings:", f.read().strip())
    except OSError:
        print("Settings: defaults (setup not run)")

    rows = []
    try:
        with open(os.path.join(DATA_DIR, "log.jsonl"), encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    ts = datetime.fromisoformat(entry["ts"])
                except (ValueError, KeyError):
                    continue  # skip a damaged line, keep the rest
                if (start is None or ts >= start) and ts < end:
                    rows.append((ts, entry.get("prompt", "")))
    except FileNotFoundError:
        pass

    label = f"{start:%Y-%m-%d %H:%M}" if start else "beginning"
    print(f"Range: {label} → {end:%Y-%m-%d %H:%M} · {len(rows)} prompts", end="")
    if len(rows) > MAX_PROMPTS:
        print(f" (showing the newest {MAX_PROMPTS})", end="")
        rows = rows[-MAX_PROMPTS:]
    print()
    if not rows:
        print("Nothing logged in this range.")
    for ts, prompt in rows:
        text = " / ".join(part.strip() for part in prompt.splitlines() if part.strip())
        if len(text) > MAX_CHARS:
            text = text[:MAX_CHARS] + " …"
        print(f"{ts:%Y-%m-%d %H:%M} | {text}")


if __name__ == "__main__":
    main()
