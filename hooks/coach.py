#!/usr/bin/env python3
"""UserPromptSubmit hook: logs the prompt and injects the English-check rules into Claude's context."""
import json
import os
import sys
from datetime import datetime

DATA_DIR = os.path.expanduser("~/.claude/englint")
DEFAULTS = {
    "enabled": True,
    "native_language": "",
    "target_level": "C1",
    "explanations": True,
    "prompt_tips": True,
    "scores": True,
    "log": True,
}


def load_config():
    """Return (config, configured). A broken config falls back to defaults so prompts never fail."""
    try:
        with open(os.path.join(DATA_DIR, "config.json"), encoding="utf-8") as f:
            return {**DEFAULTS, **json.load(f)}, True
    except FileNotFoundError:
        return dict(DEFAULTS), False
    except (OSError, ValueError):
        return dict(DEFAULTS), True


def log_prompt(prompt):
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(os.path.join(DATA_DIR, "log.jsonl"), "a", encoding="utf-8") as f:
            ts = datetime.now().astimezone().isoformat(timespec="seconds")
            f.write(json.dumps({"ts": ts, "prompt": prompt}, ensure_ascii=False) + "\n")
    except OSError:
        pass  # a missing log entry is better than a blocked prompt


def main():
    try:
        prompt = json.load(sys.stdin).get("prompt", "")
    except ValueError:
        return
    # Slash commands (like /englint:setup off) aren't the user's English.
    if not prompt.strip() or prompt.lstrip().startswith("/"):
        return
    cfg, configured = load_config()
    if not cfg["enabled"]:
        return
    if cfg["log"]:
        log_prompt(prompt)

    on_off = lambda v: "on" if v else "off"
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "coach.md"), encoding="utf-8") as f:
        print(f.read())
    print(
        f"Settings: native language = {cfg['native_language'] or 'unknown'}; "
        f"target level = {cfg['target_level']}; "
        f"grammar explanations = {on_off(cfg['explanations'])}; "
        f"prompt tips = {on_off(cfg['prompt_tips'])}; "
        f"scores = {on_off(cfg['scores'])}."
    )
    if not configured:
        print(
            "Setup not run yet: once per conversation, at the end of a reply, mention that "
            "/englint:setup sets their native language and target level."
        )


if __name__ == "__main__":
    main()
