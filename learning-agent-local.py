#!/usr/bin/env python3
"""
Learning Agent - Local Edition (No API Required)
Analyzes your daily coding activity and creates structured notes
Works entirely offline with smart pattern recognition
"""

import os
import sys
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter
import re

class LocalLearningAgent:
    def __init__(self):
        self.config_dir = Path.home() / ".learning-agent-local"
        self.config_file = self.config_dir / "config.json"
        self.config_dir.mkdir(exist_ok=True)
        self.config = self.load_config()
        
    def load_config(self):
        """Load configuration from file"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {
            "project_directories": [],
            "learning_repos": [],
            "work_repos": []
        }
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def setup(self):
        """Interactive setup"""
        print("🎯 Learning Agent Setup (Local Edition - No API Required)\n")
        
        print("📁 Project Directories")
        print("   Add directories where you keep your projects")
        print("   Example: ~/projects, ~/work, ~/learning\n")
        
        add_dirs = input("   Add project directories? (y/n): ").lower() == 'y'
        if add_dirs:
            print("   Enter directories (one per line, empty line to finish):")
            while True:
                dir_path = input("   > ").strip()
                if not dir_path:
                    break
                expanded_path = os.path.expanduser(dir_path)
                if os.path.exists(expanded_path):
                    self.config["project_directories"].append(expanded_path)
                    print(f"   ✅ Added: {expanded_path}")
                else:
                    print(f"   ⚠️  Directory not found: {expanded_path}")
        
        print("\n🏷️  Repository Classification (optional)")
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
        
        self.save_config()
        print("\n✅ Setup complete! Run 'learning-agent-local analyze' to start.\n")
    
    def find_all_repos(self):
        """Find all git repositories in configured directories"""
        repos = []
        
        if not self.config.get("project_directories"):
            return repos
        
        print("🔍 Scanning for git repositories...\n")
        
        for base_dir in self.config["project_directories"]:
            if not os.path.exists(base_dir):
                continue
            
            print(f"📁 Scanning: {base_dir}")
            
            for root, dirs, files in os.walk(base_dir):
                dirs[:] = [d for d in dirs if not d.startswith('.') or d == '.git']
                
                if '.git' in dirs:
                    repos.append(root)
                    dirs[:] = []
        
        print(f"\n✅ Found {len(repos)} repositories\n")
        return repos
    
    def get_git_activity(self, since_hours=24, repo_path=None):
        """Get git commits and changes"""
        since_time = datetime.now() - timedelta(hours=since_hours)
        since_str = since_time.strftime("%Y-%m-%d %H:%M:%S")
        
        if repo_path is None:
            repo_path = os.getcwd()
        
        activity = {
            "commits": [],
            "files_changed": [],
            "stats": {"additions": 0, "deletions": 0, "files": 0},
            "repo_path": repo_path,
            "repo_name": os.path.basename(repo_path)
        }
        
        original_dir = os.getcwd()
        
        try:
            os.chdir(repo_path)
            
            # Get commits
            result = subprocess.run(
                ["git", "log", f"--since={since_str}", "--pretty=format:%H|%an|%ad|%s", "--date=iso"],
                capture_output=True,
                text=True,
                check=True
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
            
            # Get file changes with stats
            if activity["commits"]:
                for commit in activity["commits"]:
                    result = subprocess.run(
                        ["git", "show", "--stat", "--oneline", commit["hash"]],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    activity["files_changed"].append(result.stdout)
                
                # Get overall stats
                result = subprocess.run(
                    ["git", "diff", "--shortstat", f"{activity['commits'][-1]['hash']}^", activity['commits'][0]['hash']],
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                # Parse stats
                stat_match = re.search(r'(\d+) files? changed(?:, (\d+) insertions?\(\+\))?(?:, (\d+) deletions?\(-\))?', result.stdout)
                if stat_match:
                    activity["stats"]["files"] = int(stat_match.group(1))
                    activity["stats"]["additions"] = int(stat_match.group(2) or 0)
                    activity["stats"]["deletions"] = int(stat_match.group(3) or 0)
            
            # Get current branch
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                check=True
            )
            activity["branch"] = result.stdout.strip()
            
        except subprocess.CalledProcessError:
            pass
        finally:
            os.chdir(original_dir)
        
        return activity
    
    def classify_activity(self, activity):
        """Determine if activity is learning or work"""
        repo_path = activity["repo_path"]
        
        for learning_repo in self.config.get("learning_repos", []):
            if learning_repo in repo_path:
                return "learning"
        
        for work_repo in self.config.get("work_repos", []):
            if work_repo in repo_path:
                return "work"
        
        # Use keywords
        commit_messages = " ".join([c["message"].lower() for c in activity["commits"]])
        
        learning_keywords = ["learn", "tutorial", "practice", "study", "example", "test", "experiment", "try"]
        work_keywords = ["fix", "feature", "bug", "prod", "deploy", "release", "client", "merge"]
        
        learning_score = sum(1 for kw in learning_keywords if kw in commit_messages)
        work_score = sum(1 for kw in work_keywords if kw in commit_messages)
        
        if learning_score > work_score:
            return "learning"
        elif work_score > learning_score:
            return "work"
        else:
            return "mixed"
    
    def detect_language(self, activity):
        """Detect primary programming language"""
        extensions = {
            '.jsx': 'React Native', '.tsx': 'React Native',
            '.js': 'JavaScript', '.ts': 'TypeScript',
            '.py': 'Python', '.dart': 'Flutter/Dart',
            '.java': 'Java', '.kt': 'Kotlin',
            '.swift': 'Swift', '.go': 'Go', '.rs': 'Rust',
        }
        
        files = " ".join(activity.get("files_changed", []))
        counts = Counter()
        
        for ext, lang in extensions.items():
            if ext in files:
                counts[lang] += files.count(ext)
        
        if counts:
            return counts.most_common(1)[0][0]
        return "Unknown"
    
    def analyze_local(self, activity, activity_type, language):
        """Analyze activity using local pattern recognition"""
        
        commits = activity["commits"]
        messages = [c["message"] for c in commits]
        files_text = " ".join(activity["files_changed"])
        
        # Extract patterns
        analysis = {}
        
        # 1. What was built/learned
        built_patterns = {
            "component": ["component", "create", "build", "implement", "add"],
            "feature": ["feature", "functionality", "capability"],
            "fix": ["fix", "bug", "issue", "error", "resolve"],
            "refactor": ["refactor", "cleanup", "improve", "optimize"],
            "test": ["test", "testing", "spec"],
            "style": ["style", "css", "design", "ui", "layout"],
        }
        
        detected_work = []
        for pattern_type, keywords in built_patterns.items():
            for msg in messages:
                msg_lower = msg.lower()
                if any(kw in msg_lower for kw in keywords):
                    detected_work.append(f"• {msg}")
                    break
        
        if activity_type == "learning":
            analysis["What You Learned Today"] = self._generate_learning_summary(detected_work, language, messages)
        else:
            analysis["What You Accomplished Today"] = self._generate_work_summary(detected_work, messages)
        
        # 2. Components/Features
        analysis["Components & Features"] = self._extract_components(messages, files_text, language)
        
        # 3. Bug fixes
        bug_fixes = [msg for msg in messages if any(word in msg.lower() for word in ["fix", "bug", "issue", "error"])]
        if bug_fixes:
            analysis["Bugs Fixed & Solutions"] = self._format_bug_fixes(bug_fixes)
        else:
            analysis["Bugs Fixed & Solutions"] = "No bugs fixed today."
        
        # 4. Code changes analysis
        analysis["Code Changes Summary"] = self._analyze_code_changes(activity["stats"], files_text)
        
        # 5. Technologies used
        analysis["Technologies & Tools Used"] = self._extract_technologies(messages, files_text)
        
        # 6. Patterns observed
        analysis["Patterns & Best Practices"] = self._identify_patterns(messages, files_text, language)
        
        # 7. Areas for improvement
        analysis["Areas for Improvement"] = self._suggest_improvements(activity, language, activity_type)
        
        # 8. Next steps
        analysis["Next Learning Goals"] = self._generate_next_steps(detected_work, language, activity_type)
        
        return {
            "activity_type": activity_type,
            "language": language,
            "sections": analysis,
            "metadata": {
                "repo": activity["repo_name"],
                "branch": activity.get("branch", "unknown"),
                "commits_count": len(commits),
                "date": datetime.now().isoformat(),
                "stats": activity["stats"]
            }
        }
    
    def _generate_learning_summary(self, work_items, language, messages):
        """Generate learning summary"""
        if not work_items:
            return f"Continued learning {language} through various exercises and examples."
        
        summary = f"Today's {language} learning session covered:\n"
        summary += "\n".join(work_items[:5])
        
        if len(work_items) > 5:
            summary += f"\n\n...and {len(work_items) - 5} more learning activities."
        
        return summary
    
    def _generate_work_summary(self, work_items, messages):
        """Generate work summary"""
        if not work_items:
            return "Continued development on various project tasks."
        
        summary = "Today's development work included:\n"
        summary += "\n".join(work_items[:5])
        
        if len(work_items) > 5:
            summary += f"\n\n...and {len(work_items) - 5} more tasks."
        
        return summary
    
    def _extract_components(self, messages, files, language):
        """Extract components and features"""
        components = []
        
        # React/React Native patterns
        if language in ["React Native", "JavaScript", "TypeScript"]:
            jsx_files = re.findall(r'(\w+\.jsx|\w+\.tsx)', files)
            if jsx_files:
                components.append(f"React components: {', '.join(list(set(jsx_files))[:5])}")
        
        # Python modules
        if language == "Python":
            py_files = re.findall(r'(\w+\.py)', files)
            if py_files:
                components.append(f"Python modules: {', '.join(list(set(py_files))[:5])}")
        
        # Generic components from commit messages
        component_keywords = ["component", "module", "class", "function", "api", "service", "controller", "model"]
        for msg in messages:
            for kw in component_keywords:
                if kw in msg.lower():
                    components.append(f"• {msg}")
                    break
        
        if not components:
            return "Various code modules and structures."
        
        return "\n".join(components[:7])
    
    def _format_bug_fixes(self, bug_fixes):
        """Format bug fixes"""
        result = "Today's bug fixes:\n"
        for fix in bug_fixes[:5]:
            result += f"• {fix}\n"
        
        if len(bug_fixes) > 5:
            result += f"\n...and {len(bug_fixes) - 5} more bug fixes."
        
        return result
    
    def _analyze_code_changes(self, stats, files):
        """Analyze code changes"""
        additions = stats.get("additions", 0)
        deletions = stats.get("deletions", 0)
        file_count = stats.get("files", 0)
        
        summary = f"Modified {file_count} files with {additions} additions and {deletions} deletions.\n\n"
        
        if additions > deletions * 2:
            summary += "Primarily adding new functionality and features."
        elif deletions > additions:
            summary += "Focused on code cleanup and refactoring."
        else:
            summary += "Balanced mix of additions and refactoring."
        
        return summary
    
    def _extract_technologies(self, messages, files):
        """Extract technologies used"""
        tech_patterns = {
            "React": ["react", "jsx", "component"],
            "React Native": ["react native", "expo", "react-navigation"],
            "Python": ["python", "django", "flask", "fastapi"],
            "Node.js": ["node", "express", "npm"],
            "Database": ["sql", "postgres", "mysql", "mongodb", "database"],
            "API": ["api", "rest", "graphql", "endpoint"],
            "Testing": ["test", "jest", "pytest", "unittest"],
            "Git": ["merge", "branch", "rebase"],
        }
        
        found_tech = []
        text = " ".join(messages).lower() + " " + files.lower()
        
        for tech, keywords in tech_patterns.items():
            if any(kw in text for kw in keywords):
                found_tech.append(tech)
        
        if not found_tech:
            return "Various development tools and technologies."
        
        return ", ".join(found_tech[:8])
    
    def _identify_patterns(self, messages, files, language):
        """Identify patterns and practices"""
        patterns = []
        
        text = " ".join(messages).lower()
        
        if "async" in text or "await" in text:
            patterns.append("• Using asynchronous programming patterns")
        
        if "test" in text:
            patterns.append("• Writing tests for code reliability")
        
        if "refactor" in text:
            patterns.append("• Refactoring for cleaner code")
        
        if "type" in text and language in ["TypeScript", "Python"]:
            patterns.append("• Using type annotations for better code quality")
        
        if "component" in text and language in ["React Native", "JavaScript"]:
            patterns.append("• Building reusable component architecture")
        
        if not patterns:
            return "Applying standard development practices."
        
        return "\n".join(patterns)
    
    def _suggest_improvements(self, activity, language, activity_type):
        """Suggest areas for improvement"""
        suggestions = []
        
        commits = activity["commits"]
        messages = [c["message"].lower() for c in commits]
        
        # Check for descriptive commit messages
        short_messages = [m for m in messages if len(m.split()) < 3]
        if len(short_messages) > len(messages) / 2:
            suggestions.append("• Write more descriptive commit messages explaining 'why' not just 'what'")
        
        # Check for tests
        has_tests = any("test" in m for m in messages)
        if not has_tests and activity_type == "work":
            suggestions.append("• Consider adding tests for new features and bug fixes")
        
        # Language-specific suggestions
        if language == "React Native":
            if any("style" in m for m in messages):
                suggestions.append("• Explore React Native styling best practices (StyleSheet vs styled-components)")
        
        if language == "Python":
            suggestions.append("• Consider using type hints for better code documentation")
        
        # General suggestions
        if len(commits) > 20:
            suggestions.append("• Many commits today - consider breaking work into smaller, focused sessions")
        
        if not suggestions:
            suggestions.append("• Keep up the good work! Consider documenting your learning process.")
        
        return "\n".join(suggestions[:4])
    
    def _generate_next_steps(self, work_items, language, activity_type):
        """Generate next learning goals"""
        goals = []
        
        if activity_type == "learning":
            goals.append(f"• Continue deepening {language} knowledge with more complex examples")
            goals.append("• Build a small project to apply what you've learned")
            goals.append("• Review and refactor today's code with fresh eyes")
        else:
            goals.append("• Document any new patterns or solutions discovered today")
            goals.append("• Review code for potential refactoring opportunities")
            goals.append("• Consider edge cases and error handling for today's changes")
        
        # Language-specific goals
        if language == "React Native":
            goals.append("• Explore React Native performance optimization techniques")
        elif language == "Python":
            goals.append("• Study Python design patterns and best practices")
        
        return "\n".join(goals[:4])
    
    def save_to_markdown(self, analysis):
        """Save analysis to markdown file"""
        notes_dir = self.config_dir / "notes"
        notes_dir.mkdir(exist_ok=True)
        
        date_str = datetime.now().strftime("%Y-%m-%d")
        repo_safe = analysis['metadata']['repo'].replace('/', '-')
        filename = f"{date_str}_{repo_safe}_{analysis['language']}_{analysis['activity_type']}.md"
        filepath = notes_dir / filename
        
        content = f"""# {analysis['language']} - {analysis['activity_type'].capitalize()}

**Date:** {analysis['metadata']['date'][:10]}  
**Repository:** {analysis['metadata']['repo']}  
**Branch:** {analysis['metadata']['branch']}  
**Commits:** {analysis['metadata']['commits_count']}  
**Changes:** +{analysis['metadata']['stats']['additions']} -{analysis['metadata']['stats']['deletions']} ({analysis['metadata']['stats']['files']} files)

---

"""
        
        for section, text in analysis['sections'].items():
            content += f"## {section}\n\n{text}\n\n"
        
        content += "---\n\n*Generated by Learning Agent - Local Edition*\n"
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f"📝 Saved to: {filepath}")
        return filepath
    
    def analyze(self, hours=24, all_repos=False):
        """Main analysis function"""
        print(f"🔍 Analyzing your activity from the last {hours} hours...\n")
        
        repos_to_analyze = []
        
        if all_repos:
            repos_to_analyze = self.find_all_repos()
            if not repos_to_analyze:
                print("❌ No repositories found.")
                print("   Run 'learning-agent-local setup' to add project directories")
                return
        else:
            if not os.path.exists('.git'):
                print("❌ Current directory is not a git repository.")
                print("   Use 'learning-agent-local analyze --all' to scan all projects")
                return
            repos_to_analyze = [os.getcwd()]
        
        # Collect activity
        all_activities = []
        for repo_path in repos_to_analyze:
            activity = self.get_git_activity(hours, repo_path)
            if activity and activity["commits"]:
                all_activities.append(activity)
        
        if not all_activities:
            print("❌ No git activity found.")
            return
        
        # Display summary
        print("="*60)
        print("📊 ACTIVITY SUMMARY")
        print("="*60)
        
        total_commits = sum(len(act["commits"]) for act in all_activities)
        total_additions = sum(act["stats"]["additions"] for act in all_activities)
        total_deletions = sum(act["stats"]["deletions"] for act in all_activities)
        
        print(f"\n✅ Repositories with activity: {len(all_activities)}")
        print(f"📝 Total commits: {total_commits}")
        print(f"📈 Total changes: +{total_additions} -{total_deletions}\n")
        
        for activity in all_activities:
            activity_type = self.classify_activity(activity)
            language = self.detect_language(activity)
            
            icon = "📚" if activity_type == "learning" else "💼" if activity_type == "work" else "🔀"
            print(f"{icon} {activity['repo_name']}")
            print(f"   └─ {len(activity['commits'])} commits | {language} | {activity_type}")
        
        print("\n" + "="*60 + "\n")
        
        # Analyze each repository
        for i, activity in enumerate(all_activities, 1):
            if len(all_activities) > 1:
                print(f"\n{'='*60}")
                print(f"Analyzing {i}/{len(all_activities)}: {activity['repo_name']}")
                print('='*60 + "\n")
            
            activity_type = self.classify_activity(activity)
            language = self.detect_language(activity)
            
            analysis = self.analyze_local(activity, activity_type, language)
            
            print("📖 LEARNING ANALYSIS")
            print("-" * 60 + "\n")
            
            for section, content in analysis['sections'].items():
                print(f"## {section}")
                print(content)
                print()
            
            self.save_to_markdown(analysis)
            
            if i < len(all_activities):
                print("\n" + "="*60)

def main():
    agent = LocalLearningAgent()
    
    if len(sys.argv) < 2:
        print("""
🎯 Learning Agent - Local Edition (No API Required!)

Usage:
  learning-agent-local setup         Configure project directories
  learning-agent-local analyze       Analyze current repository
  learning-agent-local analyze --all Analyze all your projects
  learning-agent-local help          Show this help

Examples:
  learning-agent-local analyze              # Current repo, last 24 hours
  learning-agent-local analyze --all        # All projects
  learning-agent-local analyze --hours 48   # Last 48 hours
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
                hours = int(sys.argv[idx + 1])
        
        if "--all" in sys.argv:
            all_repos = True
        
        agent.analyze(hours, all_repos)
    elif command == "help":
        main()
    else:
        print(f"❌ Unknown command: {command}")
        print("   Run 'learning-agent-local help' for usage")

if __name__ == "__main__":
    main()
