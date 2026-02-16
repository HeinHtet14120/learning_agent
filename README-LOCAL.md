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

The agent uses **smart pattern recognition** to analyze:

### 1. What You Learned/Built
- Extracts from commit messages
- Identifies features, components, fixes
- Categorizes your work

### 2. Components & Features
- Detects React components, Python modules, etc.
- Lists files you worked on
- Shows what you created

### 3. Bugs Fixed & Solutions
- Finds all "fix", "bug", "issue" commits
- Lists what you fixed today
- Tracks your problem-solving

### 4. Code Changes Summary
- Lines added/deleted
- Files modified
- Type of work (new features vs refactoring)

### 5. Technologies & Tools Used
- Detects: React Native, Python, Node.js, etc.
- Identifies APIs, databases, testing tools
- Shows your tech stack

### 6. Patterns & Best Practices
- Identifies async/await usage
- Detects testing practices
- Notes refactoring efforts
- TypeScript/type annotation usage

### 7. Areas for Improvement
- Checks commit message quality
- Suggests adding tests
- Language-specific tips
- General best practices

### 8. Next Learning Goals
- Suggests what to learn next
- Recommends practice projects
- Gives language-specific goals

## 📝 Example Output

```
🔍 Analyzing your activity from the last 24 hours...

📁 Scanning: /Users/heinhtet/projects
✅ Found 2 repositories

============================================================
📊 ACTIVITY SUMMARY
============================================================

✅ Repositories with activity: 2
📝 Total commits: 12
📈 Total changes: +487 -123

📚 react-native-todo-app
   └─ 8 commits | React Native | learning

💼 returning-ai
   └─ 4 commits | Python | work

============================================================

Analyzing 1/2: react-native-todo-app
============================================================

📖 LEARNING ANALYSIS
------------------------------------------------------------

## What You Learned Today

Today's React Native learning session covered:
• Implement custom drawer navigation
• Add user authentication flow
• Fix navigation params issue
• Create reusable button component

## Components & Features

React components: DrawerNavigator.jsx, LoginScreen.jsx, Button.jsx
• Create reusable button component
• Add user authentication flow

## Bugs Fixed & Solutions

Today's bug fixes:
• Fix navigation params not passing correctly
• Resolve AsyncStorage initialization error

## Code Changes Summary

Modified 12 files with 245 additions and 67 deletions.

Primarily adding new functionality and features.

## Technologies & Tools Used

React Native, React, JavaScript, API, Testing

## Patterns & Best Practices

• Using asynchronous programming patterns
• Building reusable component architecture
• Writing tests for code reliability

## Areas for Improvement

• Consider adding tests for new features and bug fixes
• Write more descriptive commit messages explaining 'why' not just 'what'

## Next Learning Goals

• Continue deepening React Native knowledge with more complex examples
• Build a small project to apply what you've learned
• Explore React Native performance optimization techniques

📝 Saved to: ~/.learning-agent-local/notes/2026-02-16_react-native-todo-app_React-Native_learning.md

============================================================
```

## 🎯 How It Works (No AI Magic!)

The local agent uses **smart pattern matching**:

1. **Reads your git commits** - Messages, file changes, stats
2. **Pattern recognition** - Looks for keywords like "fix", "feature", "bug"
3. **Code analysis** - Analyzes file types, changes, additions/deletions
4. **Smart categorization** - Learning vs work, by language
5. **Generates insights** - Based on patterns in your commits
6. **Creates notes** - Structured markdown files

**No API calls. No network. Just smart local analysis!**

## 📁 File Locations

```
~/.learning-agent-local/
├── config.json          # Your settings
└── notes/              # All your learning notes
    ├── 2026-02-16_project1_ReactNative_learning.md
    ├── 2026-02-16_project2_Python_work.md
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

### ✅ Multi-Project Support
- Scan all your repos at once
- See your entire day's work
- Cross-project insights

### ✅ Smart Classification
- Auto-detects learning vs work
- Identifies programming languages
- Categorizes by activity type

### ✅ Detailed Analysis
- What you learned
- Bugs you fixed
- Code statistics
- Technologies used
- Improvement suggestions
- Next learning goals

### ✅ Local Storage
- All notes saved as markdown
- Easy to read and search
- No database needed
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
- ✅ Summary of what you learned/built
- ✅ Components and features created
- ✅ Bugs fixed with solutions
- ✅ Code change statistics
- ✅ Technologies used
- ✅ Patterns and best practices
- ✅ Areas for improvement
- ✅ Next learning goals

All in nice markdown files you can:
- Read anytime
- Search easily
- Version control
- Share with team

## 🎉 Perfect For

- Developers who code 24/7
- Learning multiple technologies
- Working on many projects
- Want to track progress
- Need offline tools
- Value privacy
- Don't want API costs
- Have strict company policies (no external APIs!)

---

**Track your learning. No API keys. No CEO scolding. 😄**

**Made with ❤️ for developers who want privacy and freedom!**
