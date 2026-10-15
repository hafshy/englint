---
name: report
description: Give the user an English progress report and feedback based on the prompts Englint logged during a time range (today, yesterday, this week, last week, this month, last 7 days, a date range, or all time). Covers average grammar and clarity scores, their most common mistakes, the grammar rules behind them, what they did well, and what to practice next. Use when the user runs /englint:report or asks how their English is improving.
argument-hint: "[today | yesterday | week | last week | month | last month | 7d | 2026-10-01..2026-10-15 | all]"
---

# Englint report

## 1. Get the prompts

Run `report.py` from this skill's folder (the folder this SKILL.md is in) with the range from `$ARGUMENTS`. With no arguments, use `week`:

```bash
python3 "${CLAUDE_SKILL_DIR}/report.py" week
```

It prints the user's settings, the range, and one logged prompt per line. If it says nothing is logged, tell the user that logging may be off (`/englint:setup log on`) or that there are no prompts in that range yet, and stop.

## 2. Analyze

- Read every prompt. Ignore code, file paths, commands, and pasted content; judge only the user's own sentences.
- Group mistakes into patterns (for example: missing articles, verb tense after "will", plural nouns, word order in questions, uncountable nouns like "feedback"). Count how many prompts show each pattern; these counts are your estimate, so present them as approximate.
- When the native language is set, explain which patterns come from it.
- If the range covers several days, compare the earlier prompts with the later ones and say what improved or what keeps coming back.
- Score every prompt with the Grammar and Clarity rubric below, then give the averages (one decimal). When the range covers several days, give the averages for the first and the second half too.
- Estimate the level the user is writing at now, in CEFR, and compare it with their target level.

Rubric (the same one the English check uses):
- Grammar: 10 no mistakes · 8–9 small slips (capitals, punctuation) · 6–7 a few mistakes, meaning still clear · 4–5 frequent mistakes · 1–3 hard to read.
- Clarity: how easily an assistant can tell what is wanted, regardless of grammar. 10 clear goal, context and details · 7–9 clear goal, a detail missing · 4–6 needs guessing · 1–3 unclear what is asked.

## 3. Write the report

Use this structure. Be honest, specific and encouraging, and quote the user's real sentences.

```markdown
## 📊 English report · <range>

**Prompts:** <n> · **Without mistakes:** <n> (<%>) · **Writing level now:** <CEFR, e.g. B1+> · **Target:** <target>
**Grammar:** <avg>/10 · **Clarity:** <avg>/10 (<first half> → <second half> when the range covers several days)

### Most common mistakes
| Pattern | Times | Your sentence → better | Rule |
|---|---|---|---|
(3–5 rows, most frequent first)

### What you did well
(2–3 bullets with real examples)

### Progress
(Only when the range covers more than one day: how the scores moved and what changed from the start of the range to the end.)

### Focus for next time
(The 1–2 patterns that would help most, each with one short rule and 2 practice sentences for the user to fix. Put the answers in a separate "Answers" line under the practice sentences.)

### Phrases to try
(3 phrases at the target level that fit the kind of work in these prompts, each with an example sentence.)
```

Keep the whole report on one screen where possible. Don't list every single mistake.
