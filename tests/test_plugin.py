#!/usr/bin/env python3
"""Smoke test for the hook and the report script. Run: python3 tests/test_plugin.py"""
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOK = os.path.join(ROOT, "hooks", "coach.py")
REPORT = os.path.join(ROOT, "skills", "report", "report.py")


def run(script, home, stdin="", args=()):
    env = {**os.environ, "HOME": home}
    return subprocess.run([sys.executable, script, *args], input=stdin, env=env,
                          capture_output=True, text=True, check=True).stdout


def hook(home, prompt):
    return run(HOOK, home, json.dumps({"hook_event_name": "UserPromptSubmit", "prompt": prompt}))


with tempfile.TemporaryDirectory() as home:
    data = os.path.join(home, ".claude", "englint")
    log = os.path.join(data, "log.jsonl")

    out = hook(home, "i want fix the bug yesterday")
    assert "English check" in out and "Setup not run yet" in out, out
    assert "target level = C1" in out and "scores = on" in out, out
    assert "i want fix the bug yesterday" in open(log, encoding="utf-8").read()

    assert hook(home, "/englint:setup off") == "", "slash commands are skipped"

    with open(os.path.join(data, "config.json"), "w", encoding="utf-8") as f:
        json.dump({"native_language": "Indonesian", "target_level": "B2 (IELTS 6)", "explanations": False}, f)
    out = hook(home, "how to deploy it")
    assert "native language = Indonesian" in out and "explanations = off" in out, out
    assert "Setup not run yet" not in out, out

    with open(os.path.join(data, "config.json"), "w", encoding="utf-8") as f:
        json.dump({"enabled": False}, f)
    assert hook(home, "this should not log") == "", "disabled means silent"
    assert "this should not log" not in open(log, encoding="utf-8").read()

    report = run(REPORT, home, args=["today"])
    assert "2 prompts" in report and "how to deploy it" in report, report
    assert "1 prompts" not in run(REPORT, home, args=["this", "week"])
    assert "0 prompts" in run(REPORT, home, args=["2020-01-01..2020-01-31"])

print("ok")
