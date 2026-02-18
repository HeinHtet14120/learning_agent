# Learning Agent - Local Edition Commands

## Usage

```
learning-agent-local <command> [options]
```

## Commands

| Command   | Description                        |
| --------- | ---------------------------------- |
| `setup`   | Configure project directories      |
| `analyze` | Analyze git activity and generate learning notes |
| `help`    | Show usage information             |

## Options

| Option          | Description                              | Default |
| --------------- | ---------------------------------------- | ------- |
| `--all`         | Scan all configured project directories  | Off (current repo only) |
| `--hours <N>`   | Look back N hours for git activity       | 24      |

## Examples

```bash
# Run interactive setup to add project directories
learning-agent-local setup

# Analyze current repository (last 24 hours)
learning-agent-local analyze

# Analyze all configured projects
learning-agent-local analyze --all

# Analyze last 48 hours of activity
learning-agent-local analyze --hours 48

# Combine options
learning-agent-local analyze --all --hours 72
```

## Setup

Running `setup` will prompt you to configure:

- **Project directories** - folders to scan for git repos (e.g. `~/projects`, `~/work`)
- **Learning repos** - repos classified as learning/study
- **Work repos** - repos classified as work/production

Config is stored at `~/.learning-agent-local/config.json`.

## Output

The `analyze` command generates:

- A terminal summary of git activity across repos
- Per-repo analysis covering:
  - Progress & trends (streak, language trends, recurring focus areas)
  - **Concepts Learned** — maps code changes to learning concepts (classes, async/await, error handling, etc.) with difficulty level and description
  - **Code Examples** — real code snippets from your changes illustrating each concept
  - **Journey Progress** — your current level, mastered/practicing/new concepts, and next milestone
  - Components & features worked on (functions created, libraries integrated)
  - Code changes summary (with file type breakdown)
  - Technologies & tools used (detected from imports, package.json, requirements.txt)
  - Patterns & best practices (detected from actual code: async/await, hooks, error handling, etc.)
  - Areas for improvement (diff-aware: untested functions, async without error handling)
  - **Next Steps** — concept-graph-based suggestions for what to learn next, based on today's work
- Markdown notes saved to `notes/` directory (in the project root, version-controllable)
- Per-language journey files (see below)

## Notes Location

Notes are saved to `<project-root>/notes/` (next to `learning-agent-local.py`).

If you have older notes in `~/.learning-agent-local/notes/`, they will be automatically migrated on first run.

## Journey Files

Each language you work with gets persistent journey tracking files in `notes/`:

- `journey-python.json` — structured data: sessions, concept tracker with times seen and mastery status
- `journey-python.md` — human-readable summary: level, concept table, session log

Journey files are updated automatically after each analysis. Concepts progress through three mastery stages:

| Status | Criteria |
|--------|----------|
| **Introduced** | Seen 1 time |
| **Practicing** | Seen 2 times |
| **Mastered** | Seen 3+ times |

Supported languages with concept maps: **Python**, **TypeScript**, **JavaScript**, **React Native**. Other languages still get full analysis but without concept tracking.

## Concept Tracking

The agent maps your code changes to ~10-16 learning concepts per language using three signal types:

1. **Pattern detection** — async/await, error handling, decorators, React Hooks, etc.
2. **Import analysis** — modules like `asyncio`, `pytest`, `react`, `express`
3. **Code regex** — matches on added diff lines (e.g. `class Foo`, `@decorator`, `yield`)

Each concept includes:
- Difficulty level (Beginner / Intermediate / Advanced)
- Description of the concept
- Suggested next concepts to learn
- A learning path showing progression order

## Features

- **Concept-aware analysis** — identifies what you're learning from actual code, not just function names
- **Per-language journey tracking** — persistent progress across sessions with mastery levels
- **Intelligent next steps** — suggests concepts based on your learning graph, not generic advice
- **Code snippet extraction** — shows real examples from your work for each concept
- **Git diff analysis** — reads actual code changes (imports, functions, patterns) instead of just filenames
- **Multi-language detection** — detects all languages in a repo, ordered by prevalence
- **Tech stack detection** — reads `package.json`, `requirements.txt`, `Cargo.toml`, etc.
- **Progress tracking** — loads recent notes to show coding streaks, language trends, and recurring focus areas
- **No API required** — works entirely offline with local pattern recognition
