# Englint

A linter for your English. Learn English while you prompt Claude Code.

Every reply starts with a short English check of what you just wrote: a grammar score and a clarity score, a corrected version, a more advanced way to say it, the grammar rule behind each fix, and a tip for writing clearer prompts. Then Claude does the actual task as usual.

> **📝 English check** · Grammar 5/10 · Clarity 7/10
> - **You wrote:** "i want to make a global skills, the response will always started with correction"
> - **Corrected:** "I want to make a global skill. Every response should start with a correction."
> - **Advanced:** "I'd like to set up a global skill so that every response opens with a correction of my prompt."
> - **Why:** *a* takes a singular noun (*a skill*). After *will* or *should*, use the base verb (*start*, not *started*).
> - **Prompt tip:** Say where the correction should appear and what it should include, so Claude doesn't have to guess.

## Install

```
/plugin marketplace add hafshy/englint
/plugin install englint@englint
```

Then run the setup once:

```
/englint:setup
```

Requires `python3` (already installed on macOS with Xcode Command Line Tools, and on most Linux systems).

## Commands

| Command | What it does |
|---|---|
| `/englint:setup` | Asks for your native language, target level, and which lines to show |
| `/englint:setup off` | Pauses the check and logging; no extra tokens are used |
| `/englint:setup on` | Turns it back on |
| `/englint:setup level IELTS 7` | Changes one setting (`language`, `level`, `explanations`, `tips`, `scores`, `log`) |
| `/englint:setup status` | Shows your current settings |
| `/englint:report` | Your progress report for this week |
| `/englint:report today` | Also: `yesterday`, `last week`, `month`, `last month`, `7d`, `2026-10-01..2026-10-15`, `all` |

## Settings

| Setting | Default | Notes |
|---|---|---|
| On/off | on | Off means the plugin adds nothing to your prompts |
| Native language | not set | Explanations point out mistakes that come from your first language |
| Target level | C1 | Accepts CEFR (A1–C2), IELTS, TOEFL, TOEIC, or words like "advanced" and "native" |
| Grammar explanations | on | The **Why** line |
| Prompt tips | on | The **Prompt tip** line |
| Scores | on | Grammar and Clarity scores (1–10) for each prompt |
| Logging | on | Needed for reports |

## Reports

The report reads the prompts you wrote during a time range and gives you:

- your average grammar and clarity scores, and how they changed
- your most common mistakes, with your own sentences and the rule behind each one
- what you did well
- how your writing changed over the range
- 1–2 things to focus on, with practice sentences
- a few phrases to try at your target level

## Your data

Everything stays on your computer, in `~/.claude/englint/`:

- `config.json`: your settings
- `log.jsonl`: one line per prompt (time and text), used only by the report

Slash commands aren't logged. To stop logging, run `/englint:setup log off`. To delete your history, delete `log.jsonl`.

## Token cost

The check adds about 600 tokens of instructions to each prompt, plus the check itself in each reply. Turn it off with `/englint:setup off` when you need to save tokens.

## How it works

A `UserPromptSubmit` hook (`hooks/coach.py`) runs on every prompt. It reads your settings, logs the prompt, and adds the rules in `hooks/coach.md` to Claude's context. Because it runs on every prompt, the check doesn't drop out in long sessions the way an instruction in `CLAUDE.md` can.

## Development

```
claude --plugin-dir .
python3 tests/test_plugin.py
```

## License

MIT
