# Learning Agent - Installation Guide

A smart terminal agent that tracks your coding activity, distinguishes between work and learning, and saves structured notes to Notion.

## Features

🎯 **Smart Activity Detection**
- Automatically analyzes your git commits
- Distinguishes between **work** and **learning** activities
- Detects programming language automatically

🤖 **AI-Powered Analysis**
- Uses Claude AI as your senior developer mentor
- Provides structured feedback on what you learned
- Identifies bugs fixed and areas for improvement
- Suggests next learning goals

📝 **Automatic Note-Taking**
- Saves structured notes to **Notion**
- Also saves markdown backup locally
- Language-specific note structures (React Native, Python, JavaScript, etc.)

## Installation

### Step 1: Install Python Dependencies

```bash
pip install anthropic requests --break-system-packages
```

### Step 2: Make the Script Executable

```bash
chmod +x learning-agent.py
```

### Step 3: Create a System-Wide Command (Optional but Recommended)

```bash
# Option A: Create a symlink in /usr/local/bin (requires sudo)
sudo ln -s $(pwd)/learning-agent.py /usr/local/bin/learning-agent

# Option B: Add to your PATH in ~/.bashrc or ~/.zshrc
echo "export PATH=\$PATH:$(pwd)" >> ~/.bashrc
source ~/.bashrc
```

### Step 4: Run Setup

```bash
learning-agent setup
```

This will guide you through:
1. Setting up your Anthropic API key
2. Configuring Notion integration
3. Classifying your repositories (learning vs work)

## Notion Setup Guide

### 1. Create a Notion Integration

1. Go to https://www.notion.so/my-integrations
2. Click **"New integration"**
3. Give it a name: "Learning Agent"
4. Copy the **"Internal Integration Token"** (starts with `secret_`)

### 2. Create a Database in Notion

1. Create a new page in Notion
2. Add a **Database - Full page**
3. Name it "Learning Journal" or "Code Learning Notes"

### 3. Add Required Properties

Your database should have these properties:
- **Name** (Title) - auto-created
- **Type** (Select) - add options: "Learning", "Work", "Mixed"
- **Language** (Select) - add options: "React Native", "JavaScript", "Python", etc.
- **Repository** (Text)
- **Date** (Date)

### 4. Share Database with Integration

1. Click "Share" in the top-right of your database
2. Search for your integration name ("Learning Agent")
3. Click "Invite"

### 5. Get Database ID

Copy the database ID from the URL:
```
https://notion.so/YOUR_DATABASE_ID?v=...
                ^^^^ This part (32 characters)
```

## Usage

### Analyze Your Daily Activity

```bash
# Analyze last 24 hours (default)
learning-agent analyze

# Analyze last 48 hours
learning-agent analyze --hours 48

# Analyze last week
learning-agent analyze --hours 168
```

### What It Does

1. **Scans your git commits** from the specified time period
2. **Detects activity type** (learning vs work) based on:
   - Repository classification (if you configured it)
   - Commit message keywords
   - Context clues

3. **Analyzes with Claude AI**:
   - What you learned today
   - Components/features you built
   - Bugs you fixed and how
   - Best practices you applied
   - What to improve next
   - Your next learning goals

4. **Saves to Notion** with structured notes

5. **Creates local markdown backup** in `~/.learning-agent/notes/`

## Example Workflow

### End of Your Coding Day:

```bash
# Navigate to your project directory
cd ~/projects/my-react-native-app

# Run the agent
learning-agent analyze
```

**Output:**
```
🔍 Analyzing your activity from the last 24 hours...

📊 Found 8 commits in my-react-native-app
🏷️  Activity Type: learning
💻 Language: React Native

🤖 Analyzing with Claude...

============================================================
📖 LEARNING ANALYSIS
============================================================

## Components Learned/Built
Today you worked on implementing a custom drawer navigator...

## Bugs Fixed & Solutions
You encountered an issue with navigation params not being passed...

## Next Learning Goals
Focus on mastering React Navigation hooks...

✅ Saved to Notion successfully!
📝 Saved to: ~/.learning-agent/notes/2026-02-16_React-Native_learning.md

✨ Analysis complete!
```

## Tips

### 1. Classify Your Repositories

During setup, tell the agent which repos are for learning vs work:

- **Learning repos**: Tutorial projects, personal practice, study repos
- **Work repos**: Company projects, freelance work, production code

This helps the agent provide more accurate analysis.

### 2. Write Descriptive Commit Messages

Good commit messages help the agent understand your work:

```bash
# Good commits for learning
git commit -m "Learning: Implement custom drawer navigation with createDrawerNavigator"
git commit -m "Fix: Navigation params issue - switched to route.params"
git commit -m "Study: useFocusEffect hook for screen refresh"

# Good commits for work
git commit -m "Feature: Add user authentication flow"
git commit -m "Bug fix: Resolve crash on profile screen"
```

### 3. Run Daily

Make it a habit to run `learning-agent analyze` at the end of each coding session.

### 4. Review Your Progress

Open your Notion database to see:
- Learning trends over time
- Most-used languages
- Skills you've improved
- Areas that need more practice

## Troubleshooting

### "No git activity found"

Make sure you're in a git repository with recent commits:
```bash
git log --since="24 hours ago"
```

### "Anthropic API key not configured"

Run `learning-agent setup` again to configure your API key.

### "Notion API error"

1. Check your integration token is correct
2. Make sure you've shared the database with your integration
3. Verify the database ID is correct

### View Your Configuration

```bash
cat ~/.learning-agent/config.json
```

## File Locations

- **Configuration**: `~/.learning-agent/config.json`
- **Local notes backup**: `~/.learning-agent/notes/`
- **Script location**: wherever you saved `learning-agent.py`

## Advanced: Auto-Run on Git Push

Add this to your `.git/hooks/post-commit`:

```bash
#!/bin/bash
learning-agent analyze --hours 1
```

Make it executable:
```bash
chmod +x .git/hooks/post-commit
```

Now the agent runs automatically after each commit!

## Need Help?

- Check your configuration: `cat ~/.learning-agent/config.json`
- View recent notes: `ls ~/.learning-agent/notes/`
- Test git activity: `git log --since="24 hours ago"`

---

**Happy Learning! 🚀**
