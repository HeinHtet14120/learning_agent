#!/usr/bin/env python3
"""
Learning Agent - Smart code learning tracker
Analyzes your daily coding activity and saves structured notes to Notion
"""

import os
import sys
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import anthropic
import requests

class LearningAgent:
    def __init__(self):
        self.config_dir = Path.home() / ".learning-agent"
        self.config_file = self.config_dir / "config.json"
        self.config_dir.mkdir(exist_ok=True)
        self.config = self.load_config()
        
    def load_config(self):
        """Load configuration from file"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {
            "notion_token": "",
            "notion_database_id": "",
            "anthropic_api_key": "",
            "learning_repos": [],
            "work_repos": [],
            "project_directories": []  # Directories to scan for projects
        }
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def setup(self):
        """Interactive setup for first-time configuration"""
        print("🎯 Learning Agent Setup\n")
        
        print("1️⃣  Anthropic API Key (required)")
        print("   Get it from: https://console.anthropic.com/")
        api_key = input("   Enter your Anthropic API key: ").strip()
        self.config["anthropic_api_key"] = api_key
        
        print("\n2️⃣  Notion Integration (required)")
        print("   Follow these steps:")
        print("   a) Go to: https://www.notion.so/my-integrations")
        print("   b) Click 'New integration'")
        print("   c) Give it a name (e.g., 'Learning Agent')")
        print("   d) Copy the 'Internal Integration Token'")
        notion_token = input("   Enter your Notion integration token: ").strip()
        self.config["notion_token"] = notion_token
        
        print("\n   e) Create a new database in Notion for your learning notes")
        print("   f) Share the database with your integration")
        print("   g) Copy the database ID from the URL")
        print("      (the part after notion.so/ and before ?v=)")
        database_id = input("   Enter your Notion database ID: ").strip()
        self.config["notion_database_id"] = database_id
        
        print("\n3️⃣  Repository Classification (optional)")
        print("   Help the agent understand which repos are for learning vs work")
        
        add_learning = input("   Add learning repo paths? (y/n): ").lower() == 'y'
        if add_learning:
            print("   Enter repo paths (one per line, empty line to finish):")
            while True:
                repo = input("   > ").strip()
                if not repo:
                    break
                self.config["learning_repos"].append(repo)
        
        add_work = input("   Add work repo paths? (y/n): ").lower() == 'y'
        if add_work:
            print("   Enter repo paths (one per line, empty line to finish):")
            while True:
                repo = input("   > ").strip()
                if not repo:
                    break
                self.config["work_repos"].append(repo)
        
        print("\n4️⃣  Project Directories (recommended)")
        print("   Add directories where you keep your projects")
        print("   Example: ~/projects, ~/code, ~/work, ~/learning")
        
        add_dirs = input("   Add project directories to scan? (y/n): ").lower() == 'y'
        if add_dirs:
            print("   Enter directories (one per line, empty line to finish):")
            print("   Tip: Use full paths like /Users/yourname/projects")
            while True:
                dir_path = input("   > ").strip()
                if not dir_path:
                    break
                # Expand ~ to home directory
                expanded_path = os.path.expanduser(dir_path)
                if os.path.exists(expanded_path):
                    self.config["project_directories"].append(expanded_path)
                    print(f"   ✅ Added: {expanded_path}")
                else:
                    print(f"   ⚠️  Directory not found: {expanded_path}")
        
        self.save_config()
        print("\n✅ Setup complete! Run 'learning-agent analyze' to start tracking.\n")
    
    def find_all_repos(self):
        """Find all git repositories in configured project directories"""
        repos = []
        
        if not self.config.get("project_directories"):
            print("⚠️  No project directories configured.")
            print("   Run 'learning-agent setup' to add project directories")
            print("   Or use 'learning-agent analyze' in a specific repo directory\n")
            return repos
        
        print("🔍 Scanning for git repositories...\n")
        
        for base_dir in self.config["project_directories"]:
            if not os.path.exists(base_dir):
                print(f"⚠️  Directory not found: {base_dir}")
                continue
            
            print(f"📁 Scanning: {base_dir}")
            
            # Walk through directory to find .git folders
            for root, dirs, files in os.walk(base_dir):
                # Skip hidden directories except .git
                dirs[:] = [d for d in dirs if not d.startswith('.') or d == '.git']
                
                if '.git' in dirs:
                    repos.append(root)
                    # Don't scan subdirectories of a git repo
                    dirs[:] = []
        
        print(f"\n✅ Found {len(repos)} repositories\n")
        return repos
    
    def get_git_activity(self, since_hours=24, repo_path=None):
        """Get git commits and changes from the last N hours"""
        since_time = datetime.now() - timedelta(hours=since_hours)
        since_str = since_time.strftime("%Y-%m-%d %H:%M:%S")
        
        if repo_path is None:
            repo_path = os.getcwd()
        
        activity = {
            "commits": [],
            "files_changed": [],
            "repo_path": repo_path,
            "repo_name": os.path.basename(repo_path)
        }
        
        try:
            # Get current git user name for filtering
            git_user = ""
            try:
                user_result = subprocess.run(
                    ["git", "config", "user.name"],
                    capture_output=True, text=True, check=True,
                    cwd=repo_path
                )
                git_user = user_result.stdout.strip()
            except subprocess.CalledProcessError:
                pass

            # Get commits (filtered to current user only)
            cmd = ["git", "log", f"--since={since_str}", "--pretty=format:%H|%an|%ad|%s", "--date=iso"]
            if git_user:
                cmd.append(f"--author={git_user}")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                cwd=repo_path
            )
            
            if result.stdout:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        hash, author, date, message = line.split('|', 3)
                        activity["commits"].append({
                            "hash": hash,
                            "author": author,
                            "date": date,
                            "message": message
                        })
            
            # Get changed files with diff stats
            if activity["commits"]:
                latest_hash = activity["commits"][0]["hash"]
                result = subprocess.run(
                    ["git", "diff", "--stat", f"{latest_hash}^", latest_hash],
                    capture_output=True,
                    text=True,
                    check=True,
                    cwd=repo_path
                )
                activity["files_changed"] = result.stdout
            
            # Get current branch
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                check=True,
                cwd=repo_path
            )
            activity["branch"] = result.stdout.strip()

        except subprocess.CalledProcessError as e:
            print(f"⚠️  Git error in {repo_path}: {e}")
            return None
        
        return activity
    
    def classify_activity(self, activity):
        """Determine if activity is learning or work"""
        repo_path = activity["repo_path"]
        
        # Check if repo is explicitly classified
        for learning_repo in self.config.get("learning_repos", []):
            if learning_repo in repo_path:
                return "learning"
        
        for work_repo in self.config.get("work_repos", []):
            if work_repo in repo_path:
                return "work"
        
        # Use heuristics based on commit messages
        commit_messages = " ".join([c["message"].lower() for c in activity["commits"]])
        
        learning_keywords = ["learn", "tutorial", "practice", "study", "example", "test", "experiment"]
        work_keywords = ["fix", "feature", "bug", "prod", "deploy", "release", "client"]
        
        learning_score = sum(1 for kw in learning_keywords if kw in commit_messages)
        work_score = sum(1 for kw in work_keywords if kw in commit_messages)
        
        if learning_score > work_score:
            return "learning"
        elif work_score > learning_score:
            return "work"
        else:
            return "mixed"
    
    def detect_language(self, activity):
        """Detect primary programming language from file changes"""
        extensions = {
            '.jsx': 'JavaScript',
            '.tsx': 'TypeScript',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.py': 'Python',
            '.dart': 'Flutter/Dart',
            '.java': 'Java',
            '.kt': 'Kotlin',
            '.swift': 'Swift',
            '.go': 'Go',
            '.rs': 'Rust',
        }
        
        files = activity.get("files_changed", "")
        for ext, lang in extensions.items():
            if ext in files:
                return lang
        
        return "Unknown"
    
    def analyze_with_claude(self, activity, activity_type, language):
        """Use Claude to analyze the activity and generate structured notes"""
        
        if not self.config.get("anthropic_api_key"):
            print("❌ Anthropic API key not configured. Run 'learning-agent setup'")
            return None
        
        # Language-specific sections
        sections_map = {
            'React Native': [
                'Components Learned/Built',
                'Styling & Layout',
                'Navigation & Routing',
                'State Management',
                'APIs & Data Fetching',
                'Native Modules & Platform-Specific',
                'Performance Optimizations',
                'Bugs Fixed & Solutions',
                'Best Practices Applied',
                'Areas for Improvement',
                'Next Learning Goals'
            ],
            'JavaScript': [
                'Concepts Learned',
                'ES6+ Features Used',
                'Async Programming',
                'DOM Manipulation',
                'Debugging Techniques',
                'Bugs Fixed & Solutions',
                'Code Quality Improvements',
                'Areas for Improvement',
                'Next Learning Goals'
            ],
            'Python': [
                'Concepts Learned',
                'Libraries/Frameworks Used',
                'Data Structures',
                'Algorithms Implemented',
                'Testing & Debugging',
                'Bugs Fixed & Solutions',
                'Code Optimization',
                'Areas for Improvement',
                'Next Learning Goals'
            ],
            'TypeScript': [
                'Type System Features',
                'Interfaces & Types',
                'Generics Used',
                'Advanced Patterns',
                'Type Safety Improvements',
                'Bugs Fixed & Solutions',
                'Areas for Improvement',
                'Next Learning Goals'
            ],
        }
        
        sections = sections_map.get(language, sections_map['JavaScript'])
        
        # Build context from git activity
        context = f"""
Repository: {activity['repo_name']}
Branch: {activity.get('branch', 'unknown')}
Activity Type: {activity_type}
Language: {language}

Commits ({len(activity['commits'])}):
"""
        for commit in activity['commits']:
            context += f"\n- {commit['message']} (by {commit['author']} at {commit['date']})"
        
        context += f"\n\nFiles Changed:\n{activity.get('files_changed', 'No file changes detected')}"
        
        prompt = f"""You are a senior software developer and learning mentor. Analyze the following coding activity from today.

{context}

This activity is classified as: **{activity_type}**

Please provide a comprehensive analysis in the following sections:
{chr(10).join([f"{i+1}. {section}" for i, section in enumerate(sections)])}

Guidelines:
- For LEARNING activities: Focus on educational value, concepts mastered, understanding depth
- For WORK activities: Focus on problem-solving, production code quality, business impact
- For MIXED activities: Balance both perspectives

Be specific and reference actual commits/files when possible. Provide actionable insights.

Format your response as JSON:
{{
  {','.join([f'"{section}": "your detailed analysis here"' for section in sections])}
}}"""

        try:
            client = anthropic.Anthropic(api_key=self.config["anthropic_api_key"])
            
            print("🤖 Analyzing with Claude...")
            
            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            response_text = message.content[0].text
            
            # Clean up response
            response_text = response_text.replace('```json', '').replace('```', '').strip()
            analysis = json.loads(response_text)
            
            return {
                "activity_type": activity_type,
                "language": language,
                "sections": analysis,
                "metadata": {
                    "repo": activity["repo_name"],
                    "branch": activity.get("branch", "unknown"),
                    "commits_count": len(activity["commits"]),
                    "date": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            print(f"❌ Error analyzing with Claude: {e}")
            return None
    
    def save_to_notion(self, analysis):
        """Save analysis to Notion database"""
        
        if not self.config.get("notion_token") or not self.config.get("notion_database_id"):
            print("❌ Notion not configured. Run 'learning-agent setup'")
            return False
        
        try:
            headers = {
                "Authorization": f"Bearer {self.config['notion_token']}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28"
            }
            
            # Build rich text content for each section
            children = []
            for section, content in analysis["sections"].items():
                # Section heading
                children.append({
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": section}}]
                    }
                })
                
                # Section content
                children.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": content}}]
                    }
                })
            
            # Create page in database
            data = {
                "parent": {"database_id": self.config["notion_database_id"]},
                "properties": {
                    "Name": {
                        "title": [
                            {
                                "text": {
                                    "content": f"{analysis['metadata']['date'][:10]} - {analysis['language']} ({analysis['activity_type']})"
                                }
                            }
                        ]
                    },
                    "Type": {
                        "select": {
                            "name": analysis['activity_type'].capitalize()
                        }
                    },
                    "Language": {
                        "select": {
                            "name": analysis['language']
                        }
                    },
                    "Repository": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": analysis['metadata']['repo']
                                }
                            }
                        ]
                    },
                    "Date": {
                        "date": {
                            "start": analysis['metadata']['date'][:10]
                        }
                    }
                },
                "children": children
            }
            
            response = requests.post(
                "https://api.notion.com/v1/pages",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                print("✅ Saved to Notion successfully!")
                return True
            else:
                print(f"❌ Notion API error: {response.status_code}")
                print(response.text)
                return False
                
        except Exception as e:
            print(f"❌ Error saving to Notion: {e}")
            return False
    
    def save_to_markdown(self, analysis):
        """Save analysis to local markdown file as backup"""
        notes_dir = self.config_dir / "notes"
        notes_dir.mkdir(exist_ok=True)
        
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"{date_str}_{analysis['language']}_{analysis['activity_type']}.md"
        filepath = notes_dir / filename
        
        content = f"""# {analysis['language']} - {analysis['activity_type'].capitalize()}
**Date:** {analysis['metadata']['date']}
**Repository:** {analysis['metadata']['repo']}
**Branch:** {analysis['metadata']['branch']}
**Commits:** {analysis['metadata']['commits_count']}

---

"""
        
        for section, text in analysis['sections'].items():
            content += f"## {section}\n\n{text}\n\n"
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f"📝 Saved to: {filepath}")
        return filepath
    
    def analyze(self, hours=24, all_repos=False):
        """Main analysis function"""
        print(f"🔍 Analyzing your activity from the last {hours} hours...\n")
        
        repos_to_analyze = []
        
        if all_repos:
            # Scan all configured project directories
            repos_to_analyze = self.find_all_repos()
            if not repos_to_analyze:
                print("❌ No repositories found. Add project directories with 'learning-agent setup'")
                return
        else:
            # Analyze current directory only
            if not os.path.exists('.git'):
                print("❌ Current directory is not a git repository.")
                print("   Either:")
                print("   1. Run this command inside a git repository")
                print("   2. Use 'learning-agent analyze --all' to scan all your projects")
                return
            repos_to_analyze = [os.getcwd()]
        
        # Collect activity from all repos
        all_activities = []
        
        for repo_path in repos_to_analyze:
            activity = self.get_git_activity(hours, repo_path)
            if activity and activity["commits"]:
                all_activities.append(activity)
        
        if not all_activities:
            print("❌ No git activity found in any repository.")
            print("   Make sure you have commits in the last {} hours.".format(hours))
            return
        
        # Display summary
        print("="*60)
        print("📊 ACTIVITY SUMMARY")
        print("="*60)
        
        total_commits = sum(len(act["commits"]) for act in all_activities)
        print(f"\n✅ Found activity in {len(all_activities)} repositories")
        print(f"📝 Total commits: {total_commits}\n")
        
        for activity in all_activities:
            activity_type = self.classify_activity(activity)
            language = self.detect_language(activity)
            
            icon = "📚" if activity_type == "learning" else "💼" if activity_type == "work" else "🔀"
            print(f"{icon} {activity['repo_name']}")
            print(f"   └─ {len(activity['commits'])} commits | {language} | {activity_type}")
        
        print("\n" + "="*60 + "\n")
        
        # Ask user if they want to analyze all or pick specific repos
        if len(all_activities) > 1:
            print("Options:")
            print("1. Analyze all repositories together")
            print("2. Analyze each repository separately")
            print("3. Select specific repositories")
            
            choice = input("\nChoose option (1/2/3): ").strip()
            
            if choice == "1":
                self.analyze_combined(all_activities, hours)
            elif choice == "2":
                self.analyze_separate(all_activities, hours)
            elif choice == "3":
                self.analyze_selected(all_activities, hours)
            else:
                print("Invalid choice. Analyzing all together...")
                self.analyze_combined(all_activities, hours)
        else:
            # Only one repo, analyze it
            self.analyze_single(all_activities[0], hours)
    
    def analyze_single(self, activity, hours):
        """Analyze a single repository"""
        activity_type = self.classify_activity(activity)
        language = self.detect_language(activity)
        
        print(f"🔍 Analyzing {activity['repo_name']}...")
        print(f"🏷️  Type: {activity_type} | Language: {language}\n")
        
        analysis = self.analyze_with_claude(activity, activity_type, language)
        
        if analysis:
            self.display_and_save_analysis(analysis)
    
    def analyze_combined(self, all_activities, hours):
        """Analyze all repositories as one combined learning session"""
        print("🤖 Analyzing all repositories together...\n")
        
        # Combine all activities
        combined = {
            "commits": [],
            "files_changed": [],
            "repo_path": "multiple",
            "repo_name": f"{len(all_activities)} repositories",
            "repos": []
        }
        
        for activity in all_activities:
            combined["commits"].extend(activity["commits"])
            combined["files_changed"] += f"\n\n=== {activity['repo_name']} ===\n{activity.get('files_changed', '')}"
            combined["repos"].append({
                "name": activity["repo_name"],
                "path": activity["repo_path"],
                "commits": len(activity["commits"])
            })
        
        # Determine overall type and language
        activity_type = "mixed"
        languages = [self.detect_language(act) for act in all_activities]
        language = max(set(languages), key=languages.count) if languages else "Mixed"
        
        analysis = self.analyze_with_claude(combined, activity_type, language)
        
        if analysis:
            self.display_and_save_analysis(analysis)
    
    def analyze_separate(self, all_activities, hours):
        """Analyze each repository separately"""
        for i, activity in enumerate(all_activities, 1):
            print(f"\n{'='*60}")
            print(f"Analyzing {i}/{len(all_activities)}: {activity['repo_name']}")
            print('='*60 + "\n")
            
            self.analyze_single(activity, hours)
            
            if i < len(all_activities):
                input("\nPress Enter to continue to next repository...")
    
    def analyze_selected(self, all_activities, hours):
        """Let user select which repositories to analyze"""
        print("\nSelect repositories to analyze (comma-separated numbers):")
        for i, activity in enumerate(all_activities, 1):
            print(f"{i}. {activity['repo_name']} ({len(activity['commits'])} commits)")
        
        selection = input("\nEnter numbers (e.g., 1,3,4): ").strip()
        
        try:
            indices = [int(x.strip()) - 1 for x in selection.split(',')]
            selected = [all_activities[i] for i in indices if 0 <= i < len(all_activities)]
            
            if len(selected) == 1:
                self.analyze_single(selected[0], hours)
            else:
                self.analyze_combined(selected, hours)
        except (ValueError, IndexError):
            print("Invalid selection. Analyzing all repositories...")
            self.analyze_combined(all_activities, hours)
    
    def display_and_save_analysis(self, analysis):
        """Display analysis and save to Notion and markdown"""
        print("\n" + "="*60)
        print("📖 LEARNING ANALYSIS")
        print("="*60 + "\n")
        
        for section, content in analysis['sections'].items():
            print(f"## {section}")
            print(content)
            print()
        
        # Save to markdown (always)
        markdown_path = self.save_to_markdown(analysis)
        
        # Save to Notion (if configured)
        if self.config.get("notion_token"):
            self.save_to_notion(analysis)
        else:
            print("\n💡 Tip: Run 'learning-agent setup' to enable Notion integration")
        
        print(f"\n✨ Analysis complete!\n")

def main():
    agent = LearningAgent()
    
    if len(sys.argv) < 2:
        print("""
🎯 Learning Agent - Smart code learning tracker

Usage:
  learning-agent setup     Configure API keys and integrations
  learning-agent analyze   Analyze today's coding activity (current repo)
  learning-agent analyze --all   Analyze all your projects
  learning-agent help      Show this help message

Examples:
  learning-agent analyze              # Analyze current repository (last 24 hours)
  learning-agent analyze --all        # Analyze all your projects
  learning-agent analyze --hours 48   # Analyze last 48 hours
  learning-agent analyze --all --hours 168  # Analyze all projects (last week)
        """)
        return
    
    command = sys.argv[1]
    
    if command == "setup":
        agent.setup()
    elif command == "analyze":
        hours = 24
        all_repos = False
        
        if "--hours" in sys.argv:
            idx = sys.argv.index("--hours")
            if idx + 1 < len(sys.argv):
                try:
                    hours = int(sys.argv[idx + 1])
                    if hours <= 0:
                        print("❌ --hours must be a positive number")
                        return
                except ValueError:
                    print(f"❌ Invalid --hours value: {sys.argv[idx + 1]}")
                    return
        
        if "--all" in sys.argv:
            all_repos = True
        
        agent.analyze(hours, all_repos)
    elif command == "help":
        main()
    else:
        print(f"❌ Unknown command: {command}")
        print("   Run 'learning-agent help' for usage information")

if __name__ == "__main__":
    main()
