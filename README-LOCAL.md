# 🎯 Learning Agent - Local Edition

**NO API KEYS REQUIRED! CEO-Approved! 😄**

Works 100% offline using smart pattern recognition to analyze your git commits.

## ✨ Why This Version?

- ✅ **No API keys needed** - Works completely offline
- ✅ **No costs** - 100% free
- ✅ **Privacy** - Your code never leaves your machine
- ✅ **Fast** - Instant analysis, no network calls
- ✅ **Smart** - Uses pattern recognition to give you insights

## 🚀 Quick Start

### Step 1: Install

```bash
# Make installer executable
chmod +x install-local.sh

# Run installer
./install-local.sh
```

### Step 2: Setup

```bash
learning-agent-local setup
```

Add your project directories:
```
/Users/yourname/projects
/Users/yourname/work
/Users/yourname/learning
```

### Step 3: Analyze!

```bash
# Analyze ALL your projects
learning-agent-local analyze --all

# Or just current repo
cd ~/your-project
learning-agent-local analyze
```

## 📊 What It Analyzes

The agent reads your **actual code changes** (not just commit messages) to analyze:

### 1. Progress & Trends
- Coding streak tracking across sessions
- Language trends from recent notes
- Volume comparison with your average

### 2. Concepts Learned
- Maps code changes to **learning concepts** (classes, async/await, error handling, etc.)
- Shows difficulty level (Beginner / Intermediate / Advanced)
- Includes real code snippets from your work
- Supported languages: **Python, TypeScript, JavaScript, React Native**

### 3. Code Examples
- Extracts actual code snippets from your diff for each concept
- Formatted with syntax highlighting

### 4. Journey Progress
- Tracks your level per language across sessions
- Shows mastered, practicing, and newly introduced concepts
- Suggests next milestone based on learning path gaps

### 5. Components & Features
- Detects functions, classes, React components from diff
- Lists libraries integrated from imports
- Shows what you created

### 6. Code Changes Summary
- Lines added/deleted, file types changed
- Functions created/removed, imports added
- Config files modified

### 7. Technologies & Tools Used
- Detected from actual imports in your diff
- Cross-referenced with package.json, requirements.txt, etc.

### 8. Patterns & Best Practices
- Identifies async/await, React Hooks, error handling, decorators, testing, etc.
- Detected from actual code, not just commit messages

### 9. Areas for Improvement
- New functions without tests
- Async without error handling
- Dependency bloat warnings
- Commit message quality

### 10. Next Steps
- **Concept-graph-based** suggestions for what to learn next
- Based on what you coded today, suggests the logical next topics
- Deduplicates against concepts you've already practiced

## 📝 Example Output

```
📖 LEARNING ANALYSIS
------------------------------------------------------------

## Concepts Learned

### Object-Oriented Programming (Intermediate)
Building classes with __init__, methods, inheritance, and encapsulation.
  ```python
  class LocalLearningAgent:
      def __init__(self):
          self.config_dir = Path.home() / ".learning-agent-local"
  ```

### File I/O & JSON (Intermediate)
Reading and writing files, working with JSON, CSV, and pathlib.

### Error Handling (Intermediate)
Using try/except/finally blocks and raising custom exceptions.

## Code Examples

**Object-Oriented Programming:**
  ```python
  class LocalLearningAgent:
      def __init__(self):
          self.config_dir = Path.home() / ".learning-agent-local"
  ```

## Journey Progress

Level: Intermediate (8 concepts across 3 sessions)
Mastered: variables, functions
Practicing: classes, file I/O
New today: error handling
Next milestone (Advanced): Decorators, Generators

## Next Steps

Based on today's work:
• Decorators — Functions that wrap other functions to extend behavior.
• Type Hints — Annotating function signatures for clarity.
• Context Managers — Using 'with' statements for resource management.
```

## 🎯 How It Works (No AI Magic!)

The local agent uses **smart pattern matching and concept mapping**:

1. **Reads your git diff** - Actual added/removed lines, not just commit messages
2. **Concept extraction** - Maps code patterns to learning concepts (classes, async, decorators, etc.)
3. **Code snippet capture** - Extracts real examples from your changes
4. **Journey tracking** - Persistent per-language progress across sessions
5. **Smart next steps** - Suggests follow-up concepts based on a learning graph
6. **Creates notes** - Structured markdown + journey files

**No API calls. No network. Just smart local analysis!**

## 📁 File Locations

```
~/.learning-agent-local/
└── config.json              # Your settings

<project-root>/notes/        # All generated files
├── 2026-02-17_myapp_Python_learning.md     # Daily notes
├── journey-python.json      # Journey data (persistent)
├── journey-python.md        # Journey summary (human-readable)
├── journey-typescript.json
├── journey-typescript.md
└── ...
```

## 💡 Usage Examples

### Daily Review
```bash
# At end of your coding day
learning-agent-local analyze --all
```

### Single Project Deep Dive
```bash
cd ~/projects/my-app
learning-agent-local analyze --hours 48
```

### Weekly Review
```bash
learning-agent-local analyze --all --hours 168
```

## 🎨 Features

### ✅ Concept-Aware Analysis
- Maps your code changes to **learning concepts** (not just function names)
- Shows difficulty level, description, and real code snippets
- Supported: Python, TypeScript, JavaScript, React Native (~10-16 concepts each)

### ✅ Per-Language Journey Tracking
- Persistent progress across sessions
- Mastery stages: Introduced -> Practicing -> Mastered
- Concept tracker table and session log
- Journey files in `notes/journey-{language}.md`

### ✅ Intelligent Next Steps
- Suggests concepts based on your **learning graph**, not generic advice
- Deduplicates against what you've already practiced
- Follows a structured learning path per language

### ✅ Git Diff Analysis
- Reads actual code changes (imports, functions, patterns)
- Extracts code snippets for each concept
- Detects frameworks from real imports

### ✅ Multi-Project Support
- Scan all your repos at once
- See your entire day's work
- Journey tracking works across all repos

### ✅ Smart Classification
- Auto-detects learning vs work
- Identifies all programming languages
- Categorizes by activity type

### ✅ Local Storage
- All notes saved as markdown
- Journey data in JSON (machine-readable) + MD (human-readable)
- Version control friendly

## 🔧 Configuration

### View Config
```bash
cat ~/.learning-agent-local/config.json
```

### Example Config
```json
{
  "project_directories": [
    "/Users/heinhtet/projects",
    "/Users/heinhtet/work"
  ],
  "learning_repos": [
    "/Users/heinhtet/projects/react-native-tutorial"
  ],
  "work_repos": [
    "/Users/heinhtet/work/returning-ai"
  ]
}
```

### Edit Config
```bash
nano ~/.learning-agent-local/config.json
```

Or just run setup again:
```bash
learning-agent-local setup
```

## 🆚 Local vs API Version

| Feature | Local Edition | API Version |
|---------|--------------|-------------|
| API Key Required | ❌ No | ✅ Yes |
| Cost | Free | Paid |
| Privacy | 100% Local | Sends to API |
| Speed | Instant | 2-5 seconds |
| Analysis Quality | Pattern-based | AI-powered |
| Offline Work | ✅ Yes | ❌ No |
| CEO Approval | ✅ Safe | ⚠️ Risky |

## 🎓 Tips

### 1. Write Good Commit Messages
The better your commits, the better the analysis!

```bash
# Good commits
git commit -m "Learning: Implement custom React Native drawer"
git commit -m "Fix: Navigation params not passing correctly"
git commit -m "Feature: Add user authentication with JWT"

# Better than
git commit -m "updates"
git commit -m "fix"
```

### 2. Use Keywords
Help the agent understand:
- Learning: "learning", "tutorial", "practice", "study"
- Work: "feature", "fix", "bug", "prod", "deploy"

### 3. Run Daily
```bash
# Add to your end-of-day routine
alias eod="learning-agent-local analyze --all"
```

### 4. Review Your Notes
```bash
# View recent notes
ls -lt ~/.learning-agent-local/notes/ | head -10

# Read a note
cat ~/.learning-agent-local/notes/2026-02-16_*.md
```

## 🐛 Troubleshooting

### "No repositories found"
```bash
learning-agent-local setup
# Add your project directories
```

### "Command not found"
```bash
# Run directly
./learning-agent-local.py analyze --all

# Or reinstall
./install-local.sh
```

### "No git activity"
```bash
# Check your commits
git log --since="24 hours ago"

# Try longer time period
learning-agent-local analyze --hours 48
```

## 🚀 Advantages of Local Edition

1. **No API costs** - Completely free forever
2. **Privacy** - Code never leaves your machine
3. **Fast** - Instant analysis
4. **Offline** - Works without internet
5. **CEO-safe** - No API keys to worry about! 😄
6. **Simple** - Just Python, no dependencies

## 📚 What You Get

Every analysis includes:
- ✅ **Concepts Learned** — with difficulty level, description, and code snippets
- ✅ **Code Examples** — real snippets from your changes
- ✅ **Journey Progress** — level, mastered/practicing concepts, next milestone
- ✅ Components and features created
- ✅ Code change statistics
- ✅ Technologies used (from actual imports)
- ✅ Patterns and best practices (from actual code)
- ✅ Areas for improvement (diff-aware)
- ✅ **Intelligent Next Steps** — concept-graph-based suggestions

Plus persistent journey files per language:
- `journey-python.md` — human-readable progress summary
- `journey-python.json` — structured data for tracking

## 🎉 Perfect For

- Developers learning new languages and wanting to track concept mastery
- Working on many projects and wanting a unified learning journey
- Anyone who wants intelligent, concept-aware study notes from their code
- Need offline tools that respect privacy
- Don't want API costs
- Have strict company policies (no external APIs!)

---

**Track your learning journey. See real progress. No API keys needed. 😄**

**Made with ❤️ for developers who want privacy and freedom!**
