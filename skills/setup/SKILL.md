---
name: setup
description: Configure Englint, the English check at the start of every reply. Turns it on or off, and sets the user's native language, target English level (CEFR, IELTS, TOEFL, TOEIC, or words like "advanced" or "native"), grammar explanations, prompt tips, grammar and clarity scores, and prompt logging. Use when the user runs /englint:setup, or asks to pause, turn off, turn on, or change the English check.
argument-hint: "[on | off | status | language <name> | level <level> | explanations on|off | tips on|off | scores on|off | log on|off]"
---

# Englint setup

Settings live in `~/.claude/englint/config.json` (expand `~` to the user's home directory). The file may not exist yet; these are the defaults:

```json
{
  "enabled": true,
  "native_language": "",
  "target_level": "C1",
  "explanations": true,
  "prompt_tips": true,
  "scores": true,
  "log": true
}
```

| Key | Meaning |
|---|---|
| `enabled` | `false` stops the check and the logging completely, so no extra tokens are used |
| `native_language` | The user's first language, in English (`"Indonesian"`, `"Japanese"`) |
| `target_level` | The level the Advanced line is written at, stored as CEFR (see the table below) |
| `explanations` | Show the **Why** line with the grammar rules |
| `prompt_tips` | Show the **Prompt tip** line about writing clearer prompts |
| `scores` | Show the Grammar and Clarity scores (1–10) in the check's heading |
| `log` | Save each prompt locally so `/englint:report` can analyze it |

## Steps

1. Read the config file if it exists.
2. **Arguments given** (`$ARGUMENTS`): apply only that change. Examples: `off`, `on`, `level IELTS 7`, `language Indonesian`, `explanations off`, `tips off`, `scores off`, `log off`. `status` only shows the current settings and changes nothing.
3. **No arguments**: ask three questions in a single round, showing the current values: native language, target level, and which extras to show (grammar explanations, prompt tips, scores; several can be chosen). Use AskUserQuestion if it's available. Leave `enabled` and `log` as they are.
4. Convert the level with the table below and store it as CEFR, keeping the user's original wording in brackets when it's different, e.g. `"C1 (IELTS 7.5)"`.
5. Write the whole file back as JSON, creating `~/.claude/englint/` if needed. Keep any keys you didn't change.
6. Confirm in 1–3 lines: what changed, and that it applies from the next prompt. When logging is on, mention once that prompts are stored only on this computer, in `~/.claude/englint/log.jsonl`.

## Level conversion

| The user says | Store |
|---|---|
| A1, beginner, IELTS 1–2.5, TOEFL 1–1.5 | `A1` |
| A2, elementary, IELTS 3–3.5, TOEFL 2–2.5 | `A2` |
| B1, intermediate, IELTS 4–5, TOEFL 3–3.5 (old 42–71), TOEIC 550–780 | `B1` |
| B2, upper-intermediate, IELTS 5.5–6.5, TOEFL 4–4.5 (old 72–94), TOEIC 785–940 | `B2` |
| C1, advanced, IELTS 7–8, TOEFL 5–5.5 (old 95–113), TOEIC 945+ | `C1` |
| C2, proficient, IELTS 8.5–9, TOEFL 6 (old 114–120) | `C2` |
| native, native-like, "like a native speaker" | `Native` |

TOEFL scores on the 1–6 scale (from January 2026) map directly, and older 0–120 scores use the ranges in brackets. If the user's answer is unclear ("good", "better"), ask once which level they mean.
