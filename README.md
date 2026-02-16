# 🎯 Learning Agent - Multi-Project Edition

**Your AI-powered terminal companion that tracks ALL your coding projects and saves structured notes to Notion**

## 🚀 What's New: Multi-Project Support!

The agent now scans **ALL your projects** across your Mac, not just one repository!

```bash
# Analyze ALL your projects at once
learning-agent analyze --all

# See everything you've worked on today
# Across multiple repos, languages, and projects
```

## What Problem Does This Solve?

You're coding 24/7 on **multiple projects**:
- 📚 Learning React Native tutorial
- 💼 Working on company project  
- 🎨 Building side project
- 🧪 Experimenting with new tech

At the end of the day, you want to know **across ALL projects**:
- What did I learn today?
- What bugs did I fix?
- What should I improve?
- What's next?

**This agent tracks EVERYTHING automatically.**

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│  YOUR CODING DAY (Multiple Projects)                        │
│                                                             │
│  ~/projects/react-native-app    → Learning                 │
│  ~/work/company-backend         → Work                     │
│  ~/learning/python-tutorial     → Learning                 │
│  ~/side-projects/portfolio      → Mixed                    │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  TERMINAL COMMAND                                           │
│                                                             │
│  $ learning-agent analyze --all                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  🔍 SCANS ALL YOUR PROJECTS                                 │
│                                                             │
│  ✓ Found 4 repositories with activity                      │
│  ✓ 23 commits across all projects                          │
│  ✓ Detected: React Native, Python, JavaScript              │
│  ✓ Classified: 2 learning, 1 work, 1 mixed                │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  🤖 CLAUDE AI ANALYZES EVERYTHING                           │
│                                                             │
│  Provides comprehensive analysis of your entire day:       │
│  • Combined learning across all projects                   │
│  • All bugs fixed and solutions                            │
│  • Cross-project patterns                                  │
│  • Holistic improvement suggestions                        │
│  • Unified next learning goals                             │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  💾 SAVES TO NOTION                                         │
│                                                             │
│  One comprehensive note OR separate notes per project      │
└─────────────────────────────────────────────────────────────┘
```

## ✨ Key Features

### 🌐 Multi-Project Support (NEW!)
- **Scan all your projects** with one command
- Automatically finds all git repos in configured directories
- See your entire day's work across multiple codebases

### 🎯 Smart Activity Detection
- Automatically knows if you're **learning** or **working**
- Detects programming language from your files
- Analyzes commit patterns across repos

### 🤖 AI-Powered Analysis
- Claude AI reviews ALL your work like a senior developer
- Language-specific feedback per project
- Holistic view of your progress

### 📝 Flexible Note-Taking
- Analyze all projects **combined** (one big note)
- Analyze each project **separately** (individual notes)
- **Choose specific projects** to analyze
- Saves to Notion + local markdown backup

### 💡 Insightful Multi-Project Analysis
- Cross-project learning patterns
- Skills applied across different codebases
- Unified improvement suggestions
- Comprehensive next learning goals

## Installation

### Quick Install

```bash
# 1. Run installer
./install.sh

# 2. Setup (one-time configuration)
learning-agent setup
```

During setup, you'll configure:
1. Anthropic API key
2. Notion integration
3. **Project directories** (NEW!) - Tell it where your projects live

### Project Directories Setup

When you run `learning-agent setup`, add directories like:
```
~/projects
~/work
~/learning
~/code
~/Documents/coding
```

The agent will **scan these directories** and find all git repositories automatically!

## Usage

### 🌟 Analyze All Your Projects

```bash
# Analyze ALL projects (last 24 hours)
learning-agent analyze --all

# Analyze ALL projects (last week)
learning-agent analyze --all --hours 168
```

### 📁 Analyze Current Project Only

```bash
# In a specific project directory
cd ~/projects/my-app
learning-agent analyze
```

### 🕐 Custom Time Ranges

```bash
# Last 48 hours, all projects
learning-agent analyze --all --hours 48

# Last 12 hours, current project
learning-agent analyze --hours 12
```

## Example Workflow

### End of Your Coding Day:

```bash
learning-agent analyze --all
```

**Output:**
```
🔍 Analyzing your activity from the last 24 hours...

📁 Scanning: /Users/you/projects
📁 Scanning: /Users/you/work
📁 Scanning: /Users/you/learning

✅ Found 4 repositories

============================================================
📊 ACTIVITY SUMMARY
============================================================

✅ Found activity in 4 repositories
📝 Total commits: 23

📚 react-native-todo-app
   └─ 8 commits | React Native | learning

💼 company-backend-api
   └─ 12 commits | Python | work

📚 python-data-analysis
   └─ 2 commits | Python | learning

🔀 personal-portfolio
   └─ 1 commit | JavaScript | mixed

============================================================

Options:
1. Analyze all repositories together
2. Analyze each repository separately
3. Select specific repositories

Choose option (1/2/3): 1

🤖 Analyzing all repositories together...

============================================================
📖 LEARNING ANALYSIS
============================================================

## Components Learned/Built
Across your React Native and web projects today, you've worked 
on several UI components...

## Skills Applied Across Projects
You consistently applied async/await patterns in both your 
Python backend and JavaScript frontend...

## Bugs Fixed & Solutions
React Native navigation issue: Fixed params not passing...
Python backend: Resolved database connection pooling...

## Cross-Project Patterns
You're showing strong understanding of REST API design, 
applying similar patterns in both backend and frontend...

## Next Learning Goals
1. Deepen React Native navigation (deep linking)
2. Explore Python async frameworks
3. Study API authentication best practices

✅ Saved to Notion successfully!
📝 Saved to: ~/.learning-agent/notes/2026-02-16_Mixed_mixed.md

✨ Analysis complete!
```

## Analysis Options

When you run `learning-agent analyze --all` with multiple repos, you get options:

### Option 1: Combined Analysis (Recommended)
- Analyzes **all projects together**
- One comprehensive learning note
- Shows cross-project patterns
- Unified insights and goals

### Option 2: Separate Analysis
- Analyzes **each project individually**
- Separate note for each repository
- Detailed per-project feedback
- Good for focused learning

### Option 3: Selected Projects
- **Pick specific repos** to analyze
- Mix and match as needed
- Example: Only analyze learning projects, skip work

## Configuration

### View Your Config
```bash
cat ~/.learning-agent/config.json
```

### Example Config
```json
{
  "anthropic_api_key": "sk-ant-...",
  "notion_token": "secret_...",
  "notion_database_id": "abc123...",
  "project_directories": [
    "/Users/you/projects",
    "/Users/you/work",
    "/Users/you/learning"
  ],
  "learning_repos": [
    "/Users/you/projects/react-native-tutorial",
    "/Users/you/learning/python-practice"
  ],
  "work_repos": [
    "/Users/you/work/company-app"
  ]
}
```

### Add More Project Directories
Edit the config file directly or run `learning-agent setup` again.

## File Locations

```
~/.learning-agent/
├── config.json          # Your configuration (API keys, directories)
└── notes/              # Local markdown backups
    ├── 2026-02-16_Mixed_combined.md
    ├── 2026-02-16_React-Native_learning.md
    └── ...
```

## Tips & Best Practices

### 1. Configure Project Directories
Tell the agent where ALL your code lives:
```
~/projects       → Side projects
~/work          → Company work
~/learning      → Tutorials and practice
~/code          → Experiments
```

### 2. Write Descriptive Commits
```bash
# Good commits help the agent understand
git commit -m "Learning: Implement custom React Native drawer"
git commit -m "Fix: Production bug in payment processing"
git commit -m "Experiment: Testing new Python library"
```

### 3. Daily Habit
```bash
# At end of day, analyze everything
alias eod="learning-agent analyze --all"
```

### 4. Weekly Review
```bash
# Review entire week across all projects
learning-agent analyze --all --hours 168
```

### 5. Project-Specific Deep Dives
```bash
# Sometimes analyze just one project
cd ~/projects/important-project
learning-agent analyze --hours 48
```

## Use Cases

### Scenario 1: Full-Time Learner
```bash
# You're learning multiple technologies
# Track progress across all tutorials
learning-agent analyze --all
```

### Scenario 2: Professional Developer
```bash
# Work on company project + side projects
# See everything you accomplished
learning-agent analyze --all
```

### Scenario 3: Freelancer
```bash
# Multiple client projects
# Track what you did for each
learning-agent analyze --all
# Then choose Option 2 (separate analysis)
```

### Scenario 4: Student
```bash
# Class projects + personal learning
# Get comprehensive feedback
learning-agent analyze --all
```

## Comparison: Single vs Multi-Project

| Feature | Single Project | Multi-Project (--all) |
|---------|---------------|----------------------|
| Scope | Current directory only | All configured projects |
| Setup | None needed | Configure directories once |
| Commits Analyzed | One repo | All repos with activity |
| Analysis Type | Single project focus | Cross-project insights |
| Best For | Deep dive on one project | Daily overview |

## Troubleshooting

### No Repositories Found
```bash
# Run setup to configure project directories
learning-agent setup

# Verify your config
cat ~/.learning-agent/config.json
```

### Projects Not Detected
Make sure:
1. Directories exist and contain git repos
2. Repos have `.git` folders
3. Paths in config are absolute (e.g., `/Users/you/projects`)

### Analyze Specific Directory
```bash
# Temporarily analyze a different location
cd /path/to/other/projects
learning-agent analyze
```

## Advanced Usage

### Scan Specific Time Periods
```bash
# Morning work (6am-12pm)
learning-agent analyze --hours 6

# Full week review
learning-agent analyze --all --hours 168

# Yesterday only
learning-agent analyze --all --hours 24
```

### Focus on Learning Projects Only
```bash
# Option 3: Select specific repositories
learning-agent analyze --all
# Then select only learning repos
```

### Combine with Other Tools
```bash
# Run at end of day as part of routine
echo "learning-agent analyze --all" >> ~/bin/end-of-day.sh
```

## Why Multi-Project Support?

✅ **See the big picture** - All your work in one view  
✅ **Cross-project learning** - Patterns you use everywhere  
✅ **Time awareness** - Know where your time goes  
✅ **Comprehensive feedback** - Holistic improvement suggestions  
✅ **Better planning** - Unified next learning goals  
✅ **One command** - No need to cd into each project  

## Requirements

- Python 3.7+
- Git
- Anthropic API key
- Notion account (optional)
- Multiple project directories (recommended)

## What's Next?

Future improvements coming:
- Code diff analysis (actual code changes, not just commits)
- Learning streaks & gamification
- Weekly automated reports
- Smart reminders for concept review
- And more!

---

**Track ALL your coding. Learn faster. Improve consistently.** 🚀

**Made with ❤️ for developers who work on multiple projects**
