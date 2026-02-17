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
  - What was learned/accomplished (with diff-based code insights)
  - Components & features worked on (functions created, libraries integrated)
  - Bugs fixed & solutions
  - Code changes summary (with file type breakdown)
  - Technologies & tools used (detected from imports, package.json, requirements.txt)
  - Patterns & best practices (detected from actual code: async/await, hooks, error handling, etc.)
  - Areas for improvement (diff-aware: untested functions, async without error handling)
  - Next learning goals
- Markdown notes saved to `notes/` directory (in the project root, version-controllable)

## Notes Location

Notes are saved to `<project-root>/notes/` (next to `learning-agent-local.py`).

If you have older notes in `~/.learning-agent-local/notes/`, they will be automatically migrated on first run.

## Features

- **Git diff analysis** — reads actual code changes (imports, functions, patterns) instead of just filenames
- **Multi-language detection** — detects all languages in a repo, ordered by prevalence
- **Tech stack detection** — reads `package.json`, `requirements.txt`, `Cargo.toml`, etc.
- **Progress tracking** — loads recent notes to show coding streaks, language trends, and recurring focus areas
- **No API required** — works entirely offline with local pattern recognition
