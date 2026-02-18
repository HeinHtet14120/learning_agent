#!/usr/bin/env python3
"""
Learning Agent - Local Edition (No API Required)
Analyzes your daily coding activity and creates structured notes
Works entirely offline with smart pattern recognition
"""

import os
import sys
import json
import shutil
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter
import re

CONCEPT_MAP = {
    "Python": {
        "concepts": {
            "variables": {
                "name": "Variables & Data Types",
                "triggers": {"patterns": [], "imports": [], "code_re": [r"^\w+\s*=\s*.+"]},
                "level": 0,
                "description": "Assigning values to variables and working with basic data types.",
                "next": ["control_flow", "functions"],
            },
            "data_types": {
                "name": "Data Structures",
                "triggers": {"patterns": [], "imports": [], "code_re": [r"\bdict\b|\blist\b|\bset\b|\btuple\b|\{\s*['\"]"]},
                "level": 0,
                "description": "Using Python's built-in data structures: lists, dicts, sets, tuples.",
                "next": ["list_comprehension", "functions"],
            },
            "control_flow": {
                "name": "Control Flow",
                "triggers": {"patterns": [], "imports": [], "code_re": [r"^\s*(?:if |elif |else:|for |while )"]},
                "level": 0,
                "description": "Branching and looping with if/elif/else, for, and while.",
                "next": ["functions", "error_handling"],
            },
            "functions": {
                "name": "Functions",
                "triggers": {"patterns": [], "imports": [], "code_re": [r"^def \w+\("]},
                "level": 0,
                "description": "Defining reusable functions with parameters and return values.",
                "next": ["oop_classes", "type_hints"],
            },
            "oop_classes": {
                "name": "Object-Oriented Programming",
                "triggers": {"patterns": [], "imports": [], "code_re": [r"^class \w+", r"self\.\w+"]},
                "level": 1,
                "description": "Building classes with __init__, methods, inheritance, and encapsulation.",
                "next": ["decorators", "dataclasses"],
            },
            "error_handling": {
                "name": "Error Handling",
                "triggers": {"patterns": ["error handling"], "imports": [], "code_re": [r"^\s*(?:try:|except |raise )"]},
                "level": 1,
                "description": "Using try/except/finally blocks and raising custom exceptions.",
                "next": ["context_managers", "testing"],
            },
            "file_io": {
                "name": "File I/O & JSON",
                "triggers": {"patterns": [], "imports": ["json", "csv", "pathlib"], "code_re": [r"open\(", r"json\.(load|dump)", r"Path\("]},
                "level": 1,
                "description": "Reading and writing files, working with JSON, CSV, and pathlib.",
                "next": ["error_handling", "context_managers"],
            },
            "type_hints": {
                "name": "Type Hints",
                "triggers": {"patterns": ["TypeScript types"], "imports": ["typing"], "code_re": [r":\s*(?:str|int|float|bool|list|dict|Optional|Union|List|Dict)"]},
                "level": 1,
                "description": "Annotating function signatures and variables with type hints.",
                "next": ["dataclasses", "testing"],
            },
            "list_comprehension": {
                "name": "Comprehensions",
                "triggers": {"patterns": ["functional patterns"], "imports": [], "code_re": [r"\[.+\bfor\b.+\bin\b.+\]"]},
                "level": 1,
                "description": "Using list, dict, and set comprehensions for concise data transformations.",
                "next": ["generators", "functional_patterns"],
            },
            "testing": {
                "name": "Testing",
                "triggers": {"patterns": ["testing"], "imports": ["pytest", "unittest"], "code_re": [r"(?:def test_|assert |pytest\.|unittest\.)"]},
                "level": 1,
                "description": "Writing unit tests with pytest or unittest for code reliability.",
                "next": ["decorators", "functional_patterns"],
            },
            "decorators": {
                "name": "Decorators",
                "triggers": {"patterns": ["decorators"], "imports": ["functools"], "code_re": [r"^@\w+"]},
                "level": 2,
                "description": "Functions that wrap other functions to extend behavior without modification.",
                "next": ["context_managers", "generators"],
            },
            "async_await": {
                "name": "Async/Await",
                "triggers": {"patterns": ["async/await"], "imports": ["asyncio", "aiohttp"], "code_re": [r"^async def ", r"await "]},
                "level": 2,
                "description": "Asynchronous programming with async/await and the asyncio event loop.",
                "next": ["generators", "functional_patterns"],
            },
            "functional_patterns": {
                "name": "Functional Patterns",
                "triggers": {"patterns": ["functional patterns"], "imports": ["functools", "itertools"], "code_re": [r"\bmap\(|\bfilter\(|\breduce\(|\blambda "]},
                "level": 2,
                "description": "Using map, filter, reduce, lambda, and higher-order functions.",
                "next": ["generators", "decorators"],
            },
            "context_managers": {
                "name": "Context Managers",
                "triggers": {"patterns": [], "imports": ["contextlib"], "code_re": [r"\bwith\b .+ as ", r"def __enter__", r"def __exit__"]},
                "level": 2,
                "description": "Using 'with' statements and building custom context managers.",
                "next": ["async_await", "generators"],
            },
            "generators": {
                "name": "Generators",
                "triggers": {"patterns": [], "imports": [], "code_re": [r"\byield\b"]},
                "level": 2,
                "description": "Creating lazy iterators with yield for memory-efficient data processing.",
                "next": ["async_await"],
            },
            "dataclasses": {
                "name": "Dataclasses",
                "triggers": {"patterns": [], "imports": ["dataclasses"], "code_re": [r"@dataclass"]},
                "level": 2,
                "description": "Using @dataclass to create clean data-holding classes with less boilerplate.",
                "next": ["type_hints", "testing"],
            },
        },
        "learning_path": [
            ["variables", "data_types", "control_flow", "functions"],
            ["oop_classes", "error_handling", "file_io", "type_hints", "list_comprehension", "testing"],
            ["decorators", "async_await", "functional_patterns", "context_managers", "generators", "dataclasses"],
        ],
    },
    "TypeScript": {
        "concepts": {
            "ts_types": {
                "name": "TypeScript Types",
                "triggers": {"patterns": ["TypeScript types"], "imports": [], "code_re": [r":\s*(?:string|number|boolean|void)", r"\binterface\s+\w+", r"\btype\s+\w+\s*="]},
                "level": 0,
                "description": "Defining interfaces, type aliases, and basic type annotations.",
                "next": ["generics", "ts_utility_types"],
            },
            "functions": {
                "name": "Functions & Arrow Functions",
                "triggers": {"patterns": [], "imports": [], "code_re": [r"(?:function|const\s+\w+\s*=\s*(?:async\s+)?\()"]},
                "level": 0,
                "description": "Defining functions with typed parameters, return types, and arrow syntax.",
                "next": ["ts_types", "async_await"],
            },
            "react_hooks": {
                "name": "React Hooks",
                "triggers": {"patterns": ["React Hooks"], "imports": ["react"], "code_re": [r"use[A-Z]\w+\s*\("]},
                "level": 1,
                "description": "Using useState, useEffect, useRef, useMemo, and custom hooks.",
                "next": ["state_management", "testing"],
            },
            "async_await": {
                "name": "Async/Await & Promises",
                "triggers": {"patterns": ["async/await"], "imports": [], "code_re": [r"\basync\b", r"\bawait\b", r"new Promise"]},
                "level": 1,
                "description": "Handling asynchronous operations with async/await and Promise chains.",
                "next": ["error_handling", "express_routing"],
            },
            "state_management": {
                "name": "State Management",
                "triggers": {"patterns": [], "imports": ["redux", "@reduxjs/toolkit", "zustand", "recoil"], "code_re": [r"createSlice|createStore|useSelector|useDispatch"]},
                "level": 1,
                "description": "Managing application state with Redux, Zustand, or Context API.",
                "next": ["react_hooks", "testing"],
            },
            "error_handling": {
                "name": "Error Handling",
                "triggers": {"patterns": ["error handling"], "imports": [], "code_re": [r"\btry\s*\{", r"\bcatch\s*\("]},
                "level": 1,
                "description": "Implementing try/catch blocks and custom error types for robust code.",
                "next": ["testing", "async_await"],
            },
            "nextjs": {
                "name": "Next.js Patterns",
                "triggers": {"patterns": [], "imports": ["next", "next/router", "next/image", "next/link"], "code_re": [r"getServerSideProps|getStaticProps|useRouter"]},
                "level": 1,
                "description": "Using Next.js routing, SSR, SSG, and API routes.",
                "next": ["express_routing", "testing"],
            },
            "express_routing": {
                "name": "Express/API Routing",
                "triggers": {"patterns": ["middleware"], "imports": ["express"], "code_re": [r"app\.(get|post|put|delete|use)\(", r"router\.(get|post|put|delete)\("]},
                "level": 1,
                "description": "Building REST APIs with Express routes, middleware, and request handling.",
                "next": ["error_handling", "testing"],
            },
            "generics": {
                "name": "Generics",
                "triggers": {"patterns": [], "imports": [], "code_re": [r"<T(?:\s|>|,)", r"<T\s+extends\b"]},
                "level": 2,
                "description": "Writing reusable, type-safe code with generic type parameters.",
                "next": ["ts_utility_types"],
            },
            "ts_utility_types": {
                "name": "Utility Types",
                "triggers": {"patterns": [], "imports": [], "code_re": [r"\b(?:Partial|Required|Pick|Omit|Record|Exclude|Extract)<"]},
                "level": 2,
                "description": "Using built-in utility types like Partial, Pick, Omit, and Record.",
                "next": ["generics"],
            },
            "testing": {
                "name": "Testing",
                "triggers": {"patterns": ["testing"], "imports": ["jest", "vitest", "@testing-library"], "code_re": [r"\b(?:describe|it|test|expect)\s*\("]},
                "level": 1,
                "description": "Writing unit and integration tests with Jest, Vitest, or Testing Library.",
                "next": ["error_handling"],
            },
        },
        "learning_path": [
            ["functions", "ts_types"],
            ["react_hooks", "async_await", "state_management", "error_handling", "nextjs", "express_routing", "testing"],
            ["generics", "ts_utility_types"],
        ],
    },
    "JavaScript": {
        "concepts": {
            "variables": {
                "name": "Variables & ES6",
                "triggers": {"patterns": [], "imports": [], "code_re": [r"\b(?:const|let|var)\s+\w+\s*="]},
                "level": 0,
                "description": "Using const/let, template literals, destructuring, and spread operators.",
                "next": ["functions", "dom"],
            },
            "functions": {
                "name": "Functions & Arrow Functions",
                "triggers": {"patterns": [], "imports": [], "code_re": [r"(?:function\s+\w+|=>\s*[\{(])"]},
                "level": 0,
                "description": "Defining functions with parameters, defaults, rest params, and arrow syntax.",
                "next": ["closures", "async_await"],
            },
            "dom": {
                "name": "DOM Manipulation",
                "triggers": {"patterns": [], "imports": [], "code_re": [r"document\.(querySelector|getElementById|createElement)", r"\.addEventListener\("]},
                "level": 0,
                "description": "Selecting, modifying, and listening to events on DOM elements.",
                "next": ["es6_features", "closures"],
            },
            "es6_features": {
                "name": "ES6+ Features",
                "triggers": {"patterns": [], "imports": [], "code_re": [r"\.\.\.\w+", r"\bclass\s+\w+", r"`[^`]*\$\{"]},
                "level": 1,
                "description": "Using classes, spread/rest, template literals, and modules.",
                "next": ["promises", "closures"],
            },
            "closures": {
                "name": "Closures & Scope",
                "triggers": {"patterns": [], "imports": [], "code_re": [r"function\s*\(.*\)\s*\{[^}]*function", r"=>\s*\{[^}]*=>"]},
                "level": 1,
                "description": "Understanding lexical scope, closures, and higher-order functions.",
                "next": ["functional_patterns", "promises"],
            },
            "promises": {
                "name": "Promises",
                "triggers": {"patterns": [], "imports": [], "code_re": [r"new Promise\(", r"\.then\(", r"Promise\.(all|race|allSettled)"]},
                "level": 1,
                "description": "Creating and chaining Promises for asynchronous operations.",
                "next": ["async_await", "error_handling"],
            },
            "async_await": {
                "name": "Async/Await",
                "triggers": {"patterns": ["async/await"], "imports": [], "code_re": [r"\basync\b", r"\bawait\b"]},
                "level": 1,
                "description": "Writing clean asynchronous code with async functions and await.",
                "next": ["error_handling", "testing"],
            },
            "error_handling": {
                "name": "Error Handling",
                "triggers": {"patterns": ["error handling"], "imports": [], "code_re": [r"\btry\s*\{", r"\bcatch\s*\("]},
                "level": 1,
                "description": "Implementing try/catch and custom error classes for robust code.",
                "next": ["testing"],
            },
            "react_hooks": {
                "name": "React Hooks",
                "triggers": {"patterns": ["React Hooks"], "imports": ["react"], "code_re": [r"use[A-Z]\w+\s*\("]},
                "level": 1,
                "description": "Using useState, useEffect, useRef, useMemo, and custom hooks.",
                "next": ["testing", "functional_patterns"],
            },
            "functional_patterns": {
                "name": "Functional Patterns",
                "triggers": {"patterns": ["functional patterns"], "imports": [], "code_re": [r"\.map\(|\.filter\(|\.reduce\("]},
                "level": 2,
                "description": "Using map, filter, reduce and composing functions for data transformation.",
                "next": ["closures", "testing"],
            },
            "testing": {
                "name": "Testing",
                "triggers": {"patterns": ["testing"], "imports": ["jest", "vitest", "mocha"], "code_re": [r"\b(?:describe|it|test|expect)\s*\("]},
                "level": 1,
                "description": "Writing unit and integration tests with Jest, Vitest, or Mocha.",
                "next": ["error_handling"],
            },
        },
        "learning_path": [
            ["variables", "functions", "dom"],
            ["es6_features", "closures", "promises", "async_await", "error_handling", "react_hooks", "testing"],
            ["functional_patterns"],
        ],
    },
    "React Native": {
        "concepts": {
            "native_components": {
                "name": "Core Components",
                "triggers": {"patterns": [], "imports": ["react-native"], "code_re": [r"\b(?:View|Text|ScrollView|FlatList|TouchableOpacity|Image)\b"]},
                "level": 0,
                "description": "Using React Native core components: View, Text, ScrollView, FlatList.",
                "next": ["navigation", "styling"],
            },
            "styling": {
                "name": "StyleSheet & Styling",
                "triggers": {"patterns": [], "imports": [], "code_re": [r"StyleSheet\.create\(", r"style=\{"]},
                "level": 0,
                "description": "Styling components with StyleSheet.create and inline styles.",
                "next": ["animations", "platform_specific"],
            },
            "navigation": {
                "name": "Navigation",
                "triggers": {"patterns": [], "imports": ["@react-navigation"], "code_re": [r"createStackNavigator|createBottomTabNavigator|useNavigation\("]},
                "level": 1,
                "description": "Implementing screen navigation with React Navigation stack and tab navigators.",
                "next": ["app_lifecycle", "async_storage"],
            },
            "expo": {
                "name": "Expo",
                "triggers": {"patterns": [], "imports": ["expo", "expo-camera", "expo-location", "expo-notifications"], "code_re": [r"expo\.\w+"]},
                "level": 1,
                "description": "Using Expo SDK for camera, location, notifications, and managed workflow.",
                "next": ["native_modules"],
            },
            "platform_specific": {
                "name": "Platform-Specific Code",
                "triggers": {"patterns": [], "imports": [], "code_re": [r"Platform\.(OS|select)\b", r"\.ios\.|\.android\."]},
                "level": 1,
                "description": "Writing platform-specific code for iOS and Android differences.",
                "next": ["native_modules"],
            },
            "animations": {
                "name": "Animations",
                "triggers": {"patterns": [], "imports": ["react-native-reanimated", "react-native-gesture-handler"], "code_re": [r"Animated\.\w+|useSharedValue|useAnimatedStyle"]},
                "level": 2,
                "description": "Creating animations with Animated API or Reanimated library.",
                "next": ["native_modules"],
            },
            "async_storage": {
                "name": "Local Storage",
                "triggers": {"patterns": [], "imports": ["@react-native-async-storage"], "code_re": [r"AsyncStorage\.(get|set|remove)Item"]},
                "level": 1,
                "description": "Persisting data locally with AsyncStorage or similar storage solutions.",
                "next": ["navigation", "app_lifecycle"],
            },
            "app_lifecycle": {
                "name": "App Lifecycle",
                "triggers": {"patterns": [], "imports": [], "code_re": [r"AppState\.(addEventListener|currentState)", r"useAppState"]},
                "level": 1,
                "description": "Handling app lifecycle events: foreground, background, and inactive states.",
                "next": ["native_modules"],
            },
            "native_modules": {
                "name": "Native Modules",
                "triggers": {"patterns": [], "imports": [], "code_re": [r"NativeModules\.\w+", r"requireNativeComponent"]},
                "level": 2,
                "description": "Bridging native iOS/Android code with JavaScript through native modules.",
                "next": [],
            },
        },
        "learning_path": [
            ["native_components", "styling"],
            ["navigation", "expo", "platform_specific", "async_storage", "app_lifecycle"],
            ["animations", "native_modules"],
        ],
    },
}

class LocalLearningAgent:
    def __init__(self):
        self.config_dir = Path.home() / ".learning-agent-local"
        self.config_file = self.config_dir / "config.json"
        self.config_dir.mkdir(exist_ok=True)
        self.notes_dir = Path(__file__).resolve().parent / "notes"
        self.config = self.load_config()
        self._migrate_old_notes()

    def _migrate_old_notes(self):
        """One-time migration of notes from ~/.learning-agent-local/notes/ to project notes/"""
        old_notes_dir = self.config_dir / "notes"
        if not old_notes_dir.exists():
            return
        old_files = list(old_notes_dir.glob("*.md"))
        if not old_files:
            return
        self.notes_dir.mkdir(exist_ok=True)
        migrated = 0
        for f in old_files:
            dest = self.notes_dir / f.name
            if not dest.exists():
                shutil.copy2(f, dest)
                migrated += 1
        if migrated > 0:
            print(f"📦 Migrated {migrated} notes from {old_notes_dir} to {self.notes_dir}")

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

            for root, dirs, _files in os.walk(base_dir):
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

            # Get file changes with stats
            if activity["commits"]:
                for commit in activity["commits"]:
                    result = subprocess.run(
                        ["git", "show", "--stat", "--oneline", commit["hash"]],
                        capture_output=True,
                        text=True,
                        check=True,
                        cwd=repo_path
                    )
                    activity["files_changed"].append(result.stdout)

                # Get overall stats
                result = subprocess.run(
                    ["git", "diff", "--shortstat", f"{activity['commits'][-1]['hash']}^", activity['commits'][0]['hash']],
                    capture_output=True,
                    text=True,
                    check=True,
                    cwd=repo_path
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
                check=True,
                cwd=repo_path
            )
            activity["branch"] = result.stdout.strip()

        except subprocess.CalledProcessError:
            pass

        return activity

    # ── Git Diff Reading ──────────────────────────────────────────

    def _get_git_diff(self, commits, repo_path):
        """Get actual git diff content for real code analysis"""
        if not commits:
            return ""
        try:
            if len(commits) == 1:
                cmd = ["git", "show", "-p", "--no-color", commits[0]["hash"]]
            else:
                oldest = commits[-1]["hash"]
                newest = commits[0]["hash"]
                cmd = ["git", "diff", "--no-color", f"{oldest}^", newest]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=repo_path,
                timeout=30
            )
            diff_text = result.stdout or ""

            # Fallback: if diff failed (e.g. oldest is root commit), show each commit
            if not diff_text.strip():
                parts = []
                for c in commits:
                    r = subprocess.run(
                        ["git", "show", "-p", "--no-color", c["hash"]],
                        capture_output=True, text=True,
                        cwd=repo_path, timeout=30
                    )
                    if r.stdout:
                        parts.append(r.stdout)
                diff_text = "\n".join(parts)
            # Cap at 50KB / 1000 lines
            lines = diff_text.split('\n')
            if len(lines) > 1000:
                lines = lines[:1000]
            diff_text = '\n'.join(lines)
            if len(diff_text) > 50000:
                diff_text = diff_text[:50000]
            return diff_text
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError):
            return ""

    def _parse_diff(self, diff_text):
        """Parse diff text into structured analysis data"""
        parsed = {
            "imports_added": [],
            "imports_removed": [],
            "functions_added": [],
            "functions_removed": [],
            "files_by_type": Counter(),
            "frameworks_detected": set(),
            "patterns_detected": set(),
            "config_files_changed": [],
        }

        if not diff_text:
            return parsed

        config_filenames = {
            "package.json", "requirements.txt", "Cargo.toml", "go.mod",
            "pubspec.yaml", "Dockerfile", "docker-compose.yml",
            "tsconfig.json", "pyproject.toml", "setup.py", "setup.cfg",
            "Makefile", ".env", "webpack.config.js", "vite.config.ts",
            "vite.config.js", "next.config.js", "next.config.mjs",
            "tailwind.config.js", "tailwind.config.ts", "jest.config.js",
            "jest.config.ts", "vitest.config.ts", "prisma/schema.prisma",
        }

        framework_import_map = {
            "react": "React",
            "react-dom": "React",
            "next": "Next.js",
            "next/": "Next.js",
            "express": "Express",
            "django": "Django",
            "flask": "Flask",
            "fastapi": "FastAPI",
            "redux": "Redux",
            "@reduxjs/toolkit": "Redux Toolkit",
            "prisma": "Prisma",
            "@prisma/client": "Prisma",
            "expo": "Expo",
            "react-native": "React Native",
            "tailwindcss": "Tailwind CSS",
            "mongoose": "Mongoose",
            "sequelize": "Sequelize",
            "typeorm": "TypeORM",
            "axios": "Axios",
            "socket.io": "Socket.IO",
            "graphql": "GraphQL",
            "@apollo": "Apollo GraphQL",
            "vue": "Vue.js",
            "svelte": "Svelte",
            "angular": "Angular",
            "jest": "Jest",
            "pytest": "pytest",
            "unittest": "unittest",
            "vitest": "Vitest",
            "pandas": "pandas",
            "numpy": "NumPy",
            "tensorflow": "TensorFlow",
            "torch": "PyTorch",
            "sqlalchemy": "SQLAlchemy",
        }

        for line in diff_text.split('\n'):
            # Track current file from diff headers
            if line.startswith('+++ b/') or line.startswith('--- a/'):
                filepath = line[6:]
                if line.startswith('+++ b/'):
                    # Count file extensions
                    ext = os.path.splitext(filepath)[1]
                    if ext:
                        parsed["files_by_type"][ext] += 1
                    # Check for config files
                    basename = os.path.basename(filepath)
                    if basename in config_filenames or filepath in config_filenames:
                        parsed["config_files_changed"].append(basename)
                continue

            is_added = line.startswith('+') and not line.startswith('+++')
            is_removed = line.startswith('-') and not line.startswith('---')

            if not (is_added or is_removed):
                continue

            content = line[1:].strip()
            if not content:
                continue

            # Detect imports
            import_match = False
            # Python imports
            if re.match(r'^(from\s+\S+\s+import\s+|import\s+)', content):
                import_match = True
                mod = re.match(r'^(?:from\s+(\S+)|import\s+(\S+))', content)
                if mod:
                    module_name = (mod.group(1) or mod.group(2)).split('.')[0]
                    for key, fw in framework_import_map.items():
                        if module_name == key or module_name.startswith(key):
                            parsed["frameworks_detected"].add(fw)

            # JS/TS imports
            if re.match(r'^import\s+', content) or re.search(r'require\s*\(', content):
                import_match = True
                # Extract package name from import ... from 'pkg' or require('pkg')
                pkg_match = re.search(r'''(?:from\s+['"]|require\s*\(\s*['"])([^'"./][^'"]*?)['"]''', content)
                if pkg_match:
                    pkg = pkg_match.group(1).split('/')[0]
                    if pkg.startswith('@'):
                        # Scoped package like @reduxjs/toolkit
                        scoped_match = re.search(r'''(?:from\s+['"]|require\s*\(\s*['"])(@[^'"]+?)['"]''', content)
                        if scoped_match:
                            pkg = scoped_match.group(1)
                    for key, fw in framework_import_map.items():
                        if pkg == key or pkg.startswith(key):
                            parsed["frameworks_detected"].add(fw)

            if import_match:
                if is_added:
                    parsed["imports_added"].append(content)
                else:
                    parsed["imports_removed"].append(content)
                continue

            # Detect function/class definitions
            func_match = False
            # Python: def, class
            if re.match(r'^(def\s+\w+|class\s+\w+|async\s+def\s+\w+)', content):
                func_match = True
                name_m = re.match(r'^(?:async\s+)?(?:def|class)\s+(\w+)', content)
                name = name_m.group(1) if name_m else content[:40]
                if is_added:
                    parsed["functions_added"].append(name)
                else:
                    parsed["functions_removed"].append(name)

            # JS/TS: function, const X = (arrow), class, export default function
            if not func_match and re.match(r'^(?:export\s+)?(?:default\s+)?(?:async\s+)?(?:function\s+\w+|class\s+\w+)', content):
                func_match = True
                name_m = re.match(r'^(?:export\s+)?(?:default\s+)?(?:async\s+)?(?:function|class)\s+(\w+)', content)
                name = name_m.group(1) if name_m else content[:40]
                if is_added:
                    parsed["functions_added"].append(name)
                else:
                    parsed["functions_removed"].append(name)

            if not func_match and re.match(r'^(?:export\s+)?(?:const|let|var)\s+\w+\s*=\s*(?:async\s+)?\(', content):
                name_m = re.match(r'^(?:export\s+)?(?:const|let|var)\s+(\w+)', content)
                name = name_m.group(1) if name_m else content[:40]
                if is_added:
                    parsed["functions_added"].append(name)
                else:
                    parsed["functions_removed"].append(name)

            # Detect patterns from added lines
            if is_added:
                if 'async ' in content or 'await ' in content:
                    parsed["patterns_detected"].add("async/await")
                if re.search(r'use[A-Z]\w+\s*\(', content):
                    parsed["patterns_detected"].add("React Hooks")
                if re.search(r'try\s*{|except\s|catch\s*\(', content):
                    parsed["patterns_detected"].add("error handling")
                if content.startswith('@') and re.match(r'^@\w+', content):
                    parsed["patterns_detected"].add("decorators")
                if re.search(r':\s*(string|number|boolean|interface|type\s+\w+|Record<|Array<|Promise<)', content):
                    parsed["patterns_detected"].add("TypeScript types")
                if re.search(r'(?:describe|it|test|expect|assert)\s*\(', content):
                    parsed["patterns_detected"].add("testing")
                if re.search(r'\.map\(|\.filter\(|\.reduce\(|\.forEach\(|lambda\s', content):
                    parsed["patterns_detected"].add("functional patterns")
                if re.search(r'middleware|app\.use\(|@middleware', content):
                    parsed["patterns_detected"].add("middleware")

        # Convert sets to sorted lists for consistent output
        parsed["frameworks_detected"] = sorted(parsed["frameworks_detected"])
        parsed["patterns_detected"] = sorted(parsed["patterns_detected"])

        return parsed

    # ── Concept Extraction ───────────────────────────────────────

    def _extract_concepts(self, diff_parsed, diff_text, language):
        """Match diff signals against CONCEPT_MAP to identify learning concepts"""
        lang_map = CONCEPT_MAP.get(language)
        if not lang_map:
            return []

        concepts = lang_map["concepts"]
        matched = []
        added_lines = []

        # Collect added lines from diff_text for regex matching
        if diff_text:
            for line in diff_text.split('\n'):
                if line.startswith('+') and not line.startswith('+++'):
                    added_lines.append(line[1:])

        patterns_detected = set(diff_parsed.get("patterns_detected", []))
        imports_added = diff_parsed.get("imports_added", [])

        # Extract module names from imports
        import_modules = set()
        for imp in imports_added:
            # Python: from X import ... or import X
            py_m = re.match(r'^(?:from\s+(\S+)|import\s+(\S+))', imp)
            if py_m:
                mod = (py_m.group(1) or py_m.group(2)).split('.')[0]
                import_modules.add(mod)
            # JS/TS: import ... from 'pkg' or require('pkg')
            js_m = re.search(r'''(?:from\s+['"]|require\s*\(\s*['"])([^'"]+?)['"]''', imp)
            if js_m:
                import_modules.add(js_m.group(1).split('/')[0])

        for key, concept in concepts.items():
            triggers = concept["triggers"]
            triggered = False

            # 1. Check patterns_detected (cheapest)
            for p in triggers.get("patterns", []):
                if p in patterns_detected:
                    triggered = True
                    break

            # 2. Check import modules
            if not triggered:
                for imp_trigger in triggers.get("imports", []):
                    if imp_trigger in import_modules:
                        triggered = True
                        break

            # 3. Check code regexes against added lines (most expensive)
            if not triggered and triggers.get("code_re"):
                for regex in triggers["code_re"]:
                    for line in added_lines:
                        if re.search(regex, line.strip()):
                            triggered = True
                            break
                    if triggered:
                        break

            if triggered:
                snippets = self._extract_code_snippets(added_lines, triggers.get("code_re", []))
                matched.append({
                    "key": key,
                    "name": concept["name"],
                    "level": concept["level"],
                    "description": concept["description"],
                    "next": concept.get("next", []),
                    "snippets": snippets,
                })

        return matched

    def _extract_code_snippets(self, added_lines, code_regexes):
        """Extract 1-3 code snippets matching a concept's triggers from added lines"""
        if not added_lines or not code_regexes:
            return []

        snippets = []
        used_indices = set()

        for regex in code_regexes:
            for i, line in enumerate(added_lines):
                if i in used_indices:
                    continue
                if re.search(regex, line.strip()):
                    # Grab matched line + up to 4 surrounding added lines for context
                    start = max(0, i - 1)
                    end = min(len(added_lines), i + 4)
                    snippet_lines = added_lines[start:end]
                    # Remove completely blank leading/trailing lines
                    while snippet_lines and not snippet_lines[0].strip():
                        snippet_lines = snippet_lines[1:]
                    while snippet_lines and not snippet_lines[-1].strip():
                        snippet_lines = snippet_lines[:-1]
                    if snippet_lines:
                        snippets.append('\n'.join(snippet_lines[:5]))
                        used_indices.update(range(start, end))
                    if len(snippets) >= 3:
                        return snippets
            if len(snippets) >= 3:
                break

        return snippets

    # ── Multi-Language Detection ──────────────────────────────────

    def detect_languages(self, activity, diff_parsed=None):
        """Detect all programming languages used, ordered by prevalence"""
        extensions = {
            '.jsx': 'JavaScript', '.tsx': 'TypeScript',
            '.js': 'JavaScript', '.ts': 'TypeScript',
            '.py': 'Python', '.dart': 'Flutter/Dart',
            '.java': 'Java', '.kt': 'Kotlin',
            '.swift': 'Swift', '.go': 'Go', '.rs': 'Rust',
            '.rb': 'Ruby', '.php': 'PHP',
            '.cs': 'C#', '.cpp': 'C++', '.c': 'C',
            '.vue': 'Vue.js', '.svelte': 'Svelte',
        }

        counts = Counter()

        # Primary source: diff file types (most accurate)
        if diff_parsed and diff_parsed.get("files_by_type"):
            for ext, count in diff_parsed["files_by_type"].items():
                if ext in extensions:
                    counts[extensions[ext]] += count

        # Fallback: files_changed stat output
        if not counts:
            files = " ".join(activity.get("files_changed", []))
            for ext, lang in extensions.items():
                c = files.count(ext)
                if c > 0:
                    counts[lang] += c

        if not counts:
            return {"language": "Unknown", "languages": ["Unknown"]}

        ordered = [lang for lang, _ in counts.most_common()]
        return {"language": ordered[0], "languages": ordered}

    # ── Project Tech Stack Detection ──────────────────────────────

    def _detect_project_tech_stack(self, repo_path):
        """Detect tech stack from project config files"""
        tech = set()

        # package.json
        pkg_path = os.path.join(repo_path, "package.json")
        if os.path.isfile(pkg_path):
            try:
                with open(pkg_path, 'r') as f:
                    pkg = json.load(f)
                all_deps = {}
                for key in ("dependencies", "devDependencies", "peerDependencies"):
                    all_deps.update(pkg.get(key, {}))

                dep_map = {
                    "react": "React", "react-dom": "React",
                    "next": "Next.js", "express": "Express",
                    "vue": "Vue.js", "svelte": "Svelte",
                    "@angular/core": "Angular",
                    "react-native": "React Native",
                    "expo": "Expo",
                    "tailwindcss": "Tailwind CSS",
                    "prisma": "Prisma", "@prisma/client": "Prisma",
                    "redux": "Redux", "@reduxjs/toolkit": "Redux Toolkit",
                    "mongoose": "Mongoose", "sequelize": "Sequelize",
                    "typeorm": "TypeORM",
                    "jest": "Jest", "vitest": "Vitest",
                    "mocha": "Mocha",
                    "typescript": "TypeScript",
                    "webpack": "Webpack", "vite": "Vite",
                    "axios": "Axios",
                    "socket.io": "Socket.IO",
                    "graphql": "GraphQL",
                    "@apollo/client": "Apollo GraphQL",
                    "styled-components": "Styled Components",
                    "@emotion/react": "Emotion",
                }
                for dep, name in dep_map.items():
                    if dep in all_deps:
                        tech.add(name)
            except (json.JSONDecodeError, OSError):
                pass

        # requirements.txt
        req_path = os.path.join(repo_path, "requirements.txt")
        if os.path.isfile(req_path):
            try:
                with open(req_path, 'r') as f:
                    reqs = f.read().lower()
                req_map = {
                    "django": "Django", "flask": "Flask", "fastapi": "FastAPI",
                    "pytest": "pytest", "pandas": "pandas", "numpy": "NumPy",
                    "tensorflow": "TensorFlow", "torch": "PyTorch",
                    "sqlalchemy": "SQLAlchemy", "celery": "Celery",
                    "requests": "Requests", "beautifulsoup4": "BeautifulSoup",
                    "scrapy": "Scrapy",
                }
                for pkg, name in req_map.items():
                    if pkg in reqs:
                        tech.add(name)
            except OSError:
                pass

        # pyproject.toml (basic check)
        pyproject_path = os.path.join(repo_path, "pyproject.toml")
        if os.path.isfile(pyproject_path):
            try:
                with open(pyproject_path, 'r') as f:
                    content = f.read().lower()
                if "django" in content:
                    tech.add("Django")
                if "flask" in content:
                    tech.add("Flask")
                if "fastapi" in content:
                    tech.add("FastAPI")
                if "pytest" in content:
                    tech.add("pytest")
            except OSError:
                pass

        # Check file existence for other ecosystems
        if os.path.isfile(os.path.join(repo_path, "Cargo.toml")):
            tech.add("Rust/Cargo")
        if os.path.isfile(os.path.join(repo_path, "go.mod")):
            tech.add("Go Modules")
        if os.path.isfile(os.path.join(repo_path, "pubspec.yaml")):
            tech.add("Flutter/Dart")
        if os.path.isfile(os.path.join(repo_path, "Dockerfile")):
            tech.add("Docker")
        if os.path.isfile(os.path.join(repo_path, "docker-compose.yml")) or os.path.isfile(os.path.join(repo_path, "docker-compose.yaml")):
            tech.add("Docker Compose")

        return sorted(tech)

    # ── Recent Notes & Progress Tracking ─────────────────────────

    def _load_recent_notes(self, days=7, max_notes=10):
        """Load recent notes for context and trend analysis"""
        if not self.notes_dir.exists():
            return []

        notes = []
        cutoff = datetime.now() - timedelta(days=days)

        for filepath in sorted(self.notes_dir.glob("*.md"), reverse=True):
            # Parse date from filename (format: YYYY-MM-DD_repo_lang_type.md)
            name = filepath.stem
            date_match = re.match(r'^(\d{4}-\d{2}-\d{2})', name)
            if not date_match:
                continue
            try:
                note_date = datetime.strptime(date_match.group(1), "%Y-%m-%d")
            except ValueError:
                continue
            if note_date < cutoff:
                continue

            try:
                with open(filepath, 'r') as f:
                    content = f.read(2000)
                notes.append({
                    "date": date_match.group(1),
                    "filename": filepath.name,
                    "content": content,
                })
            except OSError:
                continue

            if len(notes) >= max_notes:
                break

        return notes

    def _calculate_streak(self, sorted_dates):
        """Count consecutive coding days ending today"""
        if not sorted_dates:
            return 0
        today = datetime.now().date()
        streak = 0
        check_date = today
        for d in sorted(sorted_dates, reverse=True):
            if isinstance(d, str):
                d = datetime.strptime(d, "%Y-%m-%d").date()
            if d == check_date:
                streak += 1
                check_date -= timedelta(days=1)
            elif d < check_date:
                break
        return streak

    def _analyze_progress_trends(self, current_analysis, recent_notes):
        """Analyze progress trends from recent notes"""
        if not recent_notes:
            return "No previous notes found. This is your first session!"

        lines = []

        # Coding streak
        dates = set()
        for note in recent_notes:
            dates.add(note["date"])
        dates.add(datetime.now().strftime("%Y-%m-%d"))
        streak = self._calculate_streak(sorted(dates))
        if streak > 1:
            lines.append(f"🔥 **Coding streak:** {streak} consecutive days")
        elif streak == 1:
            lines.append("📅 Active today")

        # Language trends from recent notes
        lang_counts = Counter()
        for note in recent_notes:
            # Parse language from filename: YYYY-MM-DD_repo_LANG_type.md
            parts = note["filename"].replace(".md", "").split("_")
            if len(parts) >= 3:
                lang_counts[parts[-2]] += 1
        if lang_counts:
            top_langs = [f"{lang} ({count})" for lang, count in lang_counts.most_common(3)]
            lines.append(f"📊 **Recent languages:** {', '.join(top_langs)}")

        # Recurring focus areas
        focus_keywords = {
            "auth": "Authentication", "api": "API Development",
            "test": "Testing", "database": "Database",
            "style": "Styling/UI", "deploy": "Deployment",
            "refactor": "Refactoring", "bug": "Bug Fixing",
            "component": "Component Building", "config": "Configuration",
        }
        recent_text = " ".join(n["content"].lower() for n in recent_notes)
        current_text = " ".join(
            str(v).lower() for v in current_analysis.get("sections", {}).values()
        ) if "sections" in current_analysis else ""

        recurring = []
        for kw, label in focus_keywords.items():
            if kw in recent_text and kw in current_text:
                recurring.append(label)
        if recurring:
            lines.append(f"🔁 **Recurring focus:** {', '.join(recurring[:4])}")

        # Volume comparison
        current_adds = current_analysis.get("metadata", {}).get("stats", {}).get("additions", 0)
        past_adds = []
        for note in recent_notes:
            m = re.search(r'\+(\d+)\s+-(\d+)', note["content"])
            if m:
                past_adds.append(int(m.group(1)))
        if past_adds:
            avg_past = sum(past_adds) // len(past_adds)
            if current_adds > avg_past * 1.5:
                lines.append(f"📈 **High output today:** +{current_adds} lines (avg: +{avg_past})")
            elif current_adds < avg_past * 0.5 and avg_past > 0:
                lines.append(f"📉 **Lighter session today:** +{current_adds} lines (avg: +{avg_past})")

        # Sessions count
        lines.append(f"📝 **Recent sessions:** {len(recent_notes)} notes in last 7 days")

        if not lines:
            return "Building your coding history..."

        return "\n".join(lines)

    # ── Analysis Methods (Upgraded with Diff Data) ────────────────

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

    def analyze_local(self, activity, activity_type, lang_info, diff_parsed=None, recent_notes=None, diff_text=""):
        """Analyze activity using local pattern recognition"""

        commits = activity["commits"]
        messages = [c["message"] for c in commits]
        files_text = " ".join(activity["files_changed"])
        language = lang_info["language"]
        languages = lang_info["languages"]
        repo_path = activity["repo_path"]

        if diff_parsed is None:
            diff_parsed = {}

        # Extract concepts from diff
        concepts_learned = self._extract_concepts(diff_parsed, diff_text, language)

        # Build sections in order
        analysis = {}

        # 1. Progress & Trends
        partial = {
            "metadata": {"stats": activity["stats"]},
            "sections": {}
        }
        analysis["Progress & Trends"] = self._analyze_progress_trends(partial, recent_notes or [])

        # 2. Concepts Learned (replaces "What You Learned Today")
        built_patterns = {
            "component": ["component", "create", "build", "implement", "add"],
            "feature": ["feature", "functionality", "capability"],
            "fix": ["fix", "bug", "issue", "error", "resolve"],
            "refactor": ["refactor", "cleanup", "improve", "optimize"],
            "test": ["test", "testing", "spec"],
            "style": ["style", "css", "design", "ui", "layout"],
        }

        detected_work = []
        seen_messages = set()
        for _pattern_type, keywords in built_patterns.items():
            for msg in messages:
                if msg in seen_messages:
                    continue
                msg_lower = msg.lower()
                if any(kw in msg_lower for kw in keywords):
                    detected_work.append(f"• {msg}")
                    seen_messages.add(msg)
                    break

        # Add diff-based insights to work summary
        if diff_parsed.get("functions_added"):
            for fn in diff_parsed["functions_added"][:5]:
                item = f"• Created `{fn}`"
                if item not in detected_work:
                    detected_work.append(item)
        if diff_parsed.get("frameworks_detected"):
            for fw in diff_parsed["frameworks_detected"][:3]:
                item = f"• Integrated {fw}"
                if item not in detected_work:
                    detected_work.append(item)

        if activity_type == "learning":
            analysis["Concepts Learned"] = self._generate_learning_summary(detected_work, language, concepts_learned)
        else:
            if concepts_learned:
                analysis["Concepts Learned"] = self._generate_learning_summary(detected_work, language, concepts_learned)
            else:
                analysis["What You Accomplished Today"] = self._generate_work_summary(detected_work)

        # 3. Code Examples (new — only if snippets exist)
        code_examples = self._generate_code_examples_section(concepts_learned, language)
        if code_examples:
            analysis["Code Examples"] = code_examples

        # 4. Journey Progress (new)
        if concepts_learned:
            analysis["Journey Progress"] = self._generate_journey_progress_section(language, concepts_learned)

        # 5. Components & Features
        analysis["Components & Features"] = self._extract_components(messages, files_text, language, diff_parsed)

        # 6. Code Changes Summary
        analysis["Code Changes Summary"] = self._analyze_code_changes(activity["stats"], files_text, messages, diff_parsed)

        # 7. Technologies & Tools Used
        project_tech = self._detect_project_tech_stack(repo_path)
        analysis["Technologies & Tools Used"] = self._extract_technologies(messages, files_text, diff_parsed, project_tech)

        # 8. Patterns & Best Practices
        analysis["Patterns & Best Practices"] = self._identify_patterns(messages, files_text, language, diff_parsed)

        # 9. Areas for Improvement
        analysis["Areas for Improvement"] = self._suggest_improvements(activity, language, activity_type, diff_parsed)

        # 10. Next Steps (concept-aware)
        analysis["Next Steps"] = self._generate_next_steps(concepts_learned, language, activity_type, recent_notes)

        return {
            "activity_type": activity_type,
            "language": language,
            "languages": languages,
            "concepts_learned": concepts_learned,
            "sections": analysis,
            "metadata": {
                "repo": activity["repo_name"],
                "branch": activity.get("branch", "unknown"),
                "commits_count": len(commits),
                "date": datetime.now().isoformat(),
                "stats": activity["stats"]
            }
        }

    def _generate_learning_summary(self, work_items, language, concepts_learned):
        """Generate concept-aware learning summary"""
        level_labels = {0: "Beginner", 1: "Intermediate", 2: "Advanced"}

        if not concepts_learned:
            # Fallback to original behavior
            if not work_items:
                return f"Continued learning {language} through various exercises and examples."
            summary = f"Today's {language} learning session covered:\n"
            summary += "\n".join(work_items[:8])
            if len(work_items) > 8:
                summary += f"\n\n...and {len(work_items) - 8} more learning activities."
            return summary

        parts = []
        for concept in concepts_learned:
            level = level_labels.get(concept["level"], "Intermediate")
            header = f"### {concept['name']} ({level})"
            desc = concept["description"]
            snippet_block = ""
            if concept.get("snippets"):
                snippet = concept["snippets"][0]
                lang_tag = language.lower().replace(" ", "").replace("reactnative", "jsx")
                if lang_tag == "typescript":
                    lang_tag = "typescript"
                elif lang_tag == "javascript":
                    lang_tag = "javascript"
                elif lang_tag == "python":
                    lang_tag = "python"
                snippet_block = f"\n```{lang_tag}\n{snippet}\n```"
            parts.append(f"{header}\n{desc}{snippet_block}")

        summary = "\n\n".join(parts)

        # Add remaining work items that don't map to concepts
        concept_names = {c["name"].lower() for c in concepts_learned}
        other_items = []
        for item in work_items:
            item_lower = item.lower()
            if not any(cn in item_lower for cn in concept_names):
                other_items.append(item)
        if other_items:
            summary += "\n\n### Other Activity\n" + "\n".join(other_items[:5])

        return summary

    def _generate_work_summary(self, work_items):
        """Generate work summary"""
        if not work_items:
            return "Continued development on various project tasks."

        summary = "Today's development work included:\n"
        summary += "\n".join(work_items[:8])

        if len(work_items) > 8:
            summary += f"\n\n...and {len(work_items) - 8} more tasks."

        return summary

    def _generate_code_examples_section(self, concepts_learned, language):
        """Format code snippets from matched concepts into a markdown section"""
        if not concepts_learned:
            return None

        lang_tag = language.lower().replace(" ", "")
        if lang_tag == "reactnative":
            lang_tag = "jsx"

        parts = []
        for concept in concepts_learned:
            if not concept.get("snippets"):
                continue
            for snippet in concept["snippets"][:2]:
                parts.append(f"**{concept['name']}:**\n```{lang_tag}\n{snippet}\n```")

        if not parts:
            return None

        return "\n\n".join(parts)

    def _extract_components(self, messages, files, language, diff_parsed=None):
        """Extract components and features from diff data and commit messages"""
        components = []

        # Primary: functions/classes created from diff
        if diff_parsed and diff_parsed.get("functions_added"):
            funcs = diff_parsed["functions_added"]
            # Group by likely type
            react_components = [f for f in funcs if f[0].isupper()]
            regular_funcs = [f for f in funcs if not f[0].isupper()]

            if react_components and language in ("JavaScript", "TypeScript"):
                components.append(f"React components created: {', '.join(f'`{c}`' for c in react_components[:6])}")
            if regular_funcs:
                label = "Functions" if language not in ("Python",) else "Functions/methods"
                components.append(f"{label} created: {', '.join(f'`{f}`' for f in regular_funcs[:6])}")

        # Libraries integrated from imports
        if diff_parsed and diff_parsed.get("imports_added"):
            # Extract unique package names
            pkgs = set()
            for imp in diff_parsed["imports_added"]:
                pkg_m = re.search(r'''(?:from\s+['"]|require\s*\(\s*['"])([^'"./][^'"]*?)['"]''', imp)
                if pkg_m:
                    pkgs.add(pkg_m.group(1).split('/')[0])
                py_m = re.match(r'^(?:from\s+(\S+)|import\s+(\S+))', imp)
                if py_m:
                    mod = (py_m.group(1) or py_m.group(2)).split('.')[0]
                    pkgs.add(mod)
            if pkgs:
                components.append(f"Libraries integrated: {', '.join(sorted(pkgs)[:6])}")

        # Fallback: file-based detection
        if not components:
            if language in ("JavaScript", "TypeScript"):
                jsx_files = re.findall(r'(\w+\.(?:jsx|tsx))', files)
                if jsx_files:
                    components.append(f"React components: {', '.join(list(set(jsx_files))[:5])}")

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

        return "\n".join(components[:8])

    def _format_bug_fixes(self, bug_fixes):
        """Format bug fixes"""
        result = "Today's bug fixes:\n"
        for fix in bug_fixes[:5]:
            result += f"• {fix}\n"

        if len(bug_fixes) > 5:
            result += f"\n...and {len(bug_fixes) - 5} more bug fixes."

        return result

    def _analyze_code_changes(self, stats, _files, messages=None, diff_parsed=None):
        """Analyze code changes using diff data, commit messages, and stats"""
        additions = stats.get("additions", 0)
        deletions = stats.get("deletions", 0)
        file_count = stats.get("files", 0)

        summary = f"Modified {file_count} files with {additions} additions and {deletions} deletions.\n\n"

        # Diff-based work type detection (most accurate)
        if diff_parsed:
            parts = []
            if diff_parsed.get("functions_added"):
                parts.append(f"Created {len(diff_parsed['functions_added'])} new functions/components")
            if diff_parsed.get("functions_removed"):
                parts.append(f"Removed {len(diff_parsed['functions_removed'])} functions")
            if diff_parsed.get("imports_added"):
                parts.append(f"Added {len(diff_parsed['imports_added'])} new imports")
            if diff_parsed.get("config_files_changed"):
                parts.append(f"Config changes: {', '.join(diff_parsed['config_files_changed'][:4])}")
            if diff_parsed.get("files_by_type"):
                type_summary = ", ".join(f"{ext}: {c}" for ext, c in diff_parsed["files_by_type"].most_common(4))
                parts.append(f"File types: {type_summary}")

            if parts:
                summary += "\n".join(f"• {p}" for p in parts)
                return summary

        # Cross-reference commit messages for work type
        if messages:
            msg_text = " ".join(m.lower() for m in messages)
            fix_words = ["fix", "bug", "patch", "hotfix", "resolve", "issue"]
            feat_words = ["add", "feature", "implement", "create", "new", "introduce"]
            refactor_words = ["refactor", "cleanup", "reorganize", "simplify", "extract", "rename"]

            has_fixes = any(w in msg_text for w in fix_words)
            has_features = any(w in msg_text for w in feat_words)
            has_refactors = any(w in msg_text for w in refactor_words)

            parts = []
            if has_fixes:
                parts.append("bug fixes")
            if has_features:
                parts.append("new features")
            if has_refactors:
                parts.append("refactoring")

            if parts:
                summary += f"Work included: {', '.join(parts)}."
                return summary

        # Fall back to line-count heuristic
        if additions > deletions * 2:
            summary += "Primarily adding new functionality and features."
        elif deletions > additions:
            summary += "Focused on code cleanup and refactoring."
        else:
            summary += "Balanced mix of additions and refactoring."

        return summary

    def _extract_technologies(self, messages, files, diff_parsed=None, project_tech=None):
        """Extract technologies used from diff imports, project files, and keywords"""
        found_tech = set()

        # Primary: frameworks detected from actual imports in diff
        if diff_parsed and diff_parsed.get("frameworks_detected"):
            found_tech.update(diff_parsed["frameworks_detected"])

        # Secondary: project tech stack from config files
        if project_tech:
            found_tech.update(project_tech)

        # Tertiary: config files changed
        if diff_parsed and diff_parsed.get("config_files_changed"):
            for cfg in diff_parsed["config_files_changed"]:
                if cfg == "package.json":
                    found_tech.add("npm")
                elif cfg == "requirements.txt":
                    found_tech.add("pip")
                elif cfg == "Dockerfile":
                    found_tech.add("Docker")

        # Fallback: keyword matching (only if nothing found above)
        if not found_tech:
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

            text = " ".join(messages).lower() + " " + files.lower()

            for tech, keywords in tech_patterns.items():
                if any(kw in text for kw in keywords):
                    found_tech.add(tech)

        if not found_tech:
            return "Various development tools and technologies."

        return ", ".join(sorted(found_tech)[:10])

    def _identify_patterns(self, messages, _files, language, diff_parsed=None):
        """Identify patterns and practices from diff analysis and commit messages"""
        patterns = []

        # Primary: patterns detected from actual code in diff
        if diff_parsed and diff_parsed.get("patterns_detected"):
            pattern_labels = {
                "async/await": "Using asynchronous programming (async/await)",
                "React Hooks": "Using React Hooks (useState, useEffect, etc.)",
                "error handling": "Implementing error handling (try/catch/except)",
                "decorators": "Using decorators for cross-cutting concerns",
                "TypeScript types": "Applying TypeScript type annotations",
                "testing": "Writing tests for code reliability",
                "functional patterns": "Using functional programming patterns (map, filter, reduce)",
                "middleware": "Implementing middleware patterns",
            }
            for p in diff_parsed["patterns_detected"]:
                label = pattern_labels.get(p, p)
                patterns.append(f"• {label}")

        # Secondary: commit message keyword detection (only for patterns not already found)
        text = " ".join(messages).lower()
        detected_names = set(diff_parsed.get("patterns_detected", [])) if diff_parsed else set()

        keyword_patterns = [
            ("async/await", "async" in text or "await" in text, "Using asynchronous programming patterns"),
            ("testing", "test" in text, "Writing tests for code reliability"),
            ("refactoring", "refactor" in text, "Refactoring for cleaner code"),
            ("TypeScript types", "type" in text and language in ["TypeScript", "Python"], "Using type annotations for better code quality"),
            ("React Hooks", "component" in text and language in ["JavaScript", "TypeScript"], "Building reusable component architecture"),
            ("error handling", any(w in text for w in ["error", "exception", "try", "catch", "handle"]), "Implementing error handling strategies"),
            ("config", any(w in text for w in ["config", "env", "setting", "option"]), "Managing configuration and environment settings"),
            ("API", any(w in text for w in ["api", "endpoint", "route", "request", "response"]), "Working with API integration patterns"),
            ("state", any(w in text for w in ["state", "store", "redux", "context", "hook"]), "Applying state management patterns"),
            ("auth", any(w in text for w in ["auth", "login", "token", "permission", "session"]), "Implementing authentication/authorization"),
            ("database", any(w in text for w in ["database", "query", "model", "schema", "migration"]), "Working with database and data modeling patterns"),
        ]

        for name, condition, label in keyword_patterns:
            if condition and name not in detected_names:
                item = f"• {label}"
                if item not in patterns:
                    patterns.append(item)

        if not patterns:
            return f"Applying standard {language} development practices."

        return "\n".join(patterns[:8])

    def _suggest_improvements(self, activity, language, activity_type, diff_parsed=None):
        """Suggest areas for improvement based on diff analysis"""
        suggestions = []

        commits = activity["commits"]
        messages = [c["message"].lower() for c in commits]

        # Diff-based suggestions
        if diff_parsed:
            # New functions without test patterns
            if diff_parsed.get("functions_added") and "testing" not in diff_parsed.get("patterns_detected", []):
                count = len(diff_parsed["functions_added"])
                suggestions.append(f"• Added {count} new functions — consider adding tests for them")

            # Async without error handling
            if "async/await" in diff_parsed.get("patterns_detected", []) and "error handling" not in diff_parsed.get("patterns_detected", []):
                suggestions.append("• Using async/await without visible error handling — add try/catch blocks")

            # Many new imports (potential dependency bloat)
            if len(diff_parsed.get("imports_added", [])) > 8:
                suggestions.append(f"• Added {len(diff_parsed['imports_added'])} new imports — review for unused dependencies")

            # Removed functions (potential breaking changes)
            if diff_parsed.get("functions_removed"):
                count = len(diff_parsed["functions_removed"])
                suggestions.append(f"• Removed {count} functions — verify no callers are broken")

        # Check for descriptive commit messages
        short_messages = [m for m in messages if len(m.split()) < 3]
        if len(short_messages) > len(messages) / 2:
            suggestions.append("• Write more descriptive commit messages explaining 'why' not just 'what'")

        # Check for tests
        has_tests = any("test" in m for m in messages)
        if not has_tests and activity_type == "work" and "• Added" not in " ".join(suggestions):
            suggestions.append("• Consider adding tests for new features and bug fixes")

        # Language-specific suggestions
        if language == "Python":
            suggestions.append("• Consider using type hints for better code documentation")

        # General suggestions
        if len(commits) > 20:
            suggestions.append("• Many commits today — consider breaking work into smaller, focused sessions")

        if not suggestions:
            suggestions.append("• Keep up the good work! Consider documenting your learning process.")

        return "\n".join(suggestions[:5])

    def _parse_concepts_from_notes(self, recent_notes, language):
        """Scan recent note content for concept names from CONCEPT_MAP, return set of seen concept keys"""
        lang_map = CONCEPT_MAP.get(language)
        if not lang_map or not recent_notes:
            return set()

        seen = set()
        all_text = " ".join(n["content"].lower() for n in recent_notes)
        for key, concept in lang_map["concepts"].items():
            if concept["name"].lower() in all_text:
                seen.add(key)
        return seen

    def _generate_next_steps(self, concepts_learned, language, activity_type, recent_notes=None):
        """Generate concept-graph-based next step suggestions"""
        lang_map = CONCEPT_MAP.get(language)

        # Fallback if language not in CONCEPT_MAP
        if not lang_map:
            goals = []
            if activity_type == "learning":
                goals.append(f"• Continue deepening {language} knowledge with more complex examples")
                goals.append("• Build a small project to apply what you've learned")
            else:
                goals.append("• Document any new patterns or solutions discovered today")
                goals.append("• Review code for potential refactoring opportunities")
            return "\n".join(goals[:4])

        concepts_map = lang_map["concepts"]
        learning_path = lang_map["learning_path"]

        # Concepts already seen in recent notes
        seen_concepts = self._parse_concepts_from_notes(recent_notes or [], language)

        # Add today's concepts to seen set
        today_keys = {c["key"] for c in (concepts_learned or [])}
        seen_concepts |= today_keys

        # Collect 'next' topics from today's concepts
        candidates = []
        for concept in (concepts_learned or []):
            for next_key in concept.get("next", []):
                if next_key not in seen_concepts and next_key in concepts_map:
                    candidates.append(next_key)

        # If no concepts matched today, suggest fundamentals from learning_path not yet seen
        if not candidates:
            for level_group in learning_path:
                for key in level_group:
                    if key not in seen_concepts and key in concepts_map:
                        candidates.append(key)
                if candidates:
                    break

        # Deduplicate while preserving order
        seen_candidates = set()
        unique_candidates = []
        for c in candidates:
            if c not in seen_candidates:
                seen_candidates.add(c)
                unique_candidates.append(c)

        # Sort by learning_path position (suggest same level or one level up)
        def path_position(key):
            for level_idx, group in enumerate(learning_path):
                if key in group:
                    return level_idx
            return 99

        unique_candidates.sort(key=path_position)

        goals = []
        if unique_candidates:
            intro = "Based on today's work" if concepts_learned else "Suggested next topics"
            goals.append(f"{intro}:")
            for key in unique_candidates[:4]:
                concept = concepts_map[key]
                goals.append(f"• **{concept['name']}** — {concept['description']}")
        else:
            goals.append(f"• Keep practicing {language} — you've covered the fundamentals well!")
            goals.append("• Try building a project that combines multiple concepts")

        return "\n".join(goals[:5])

    # ── Per-Language Journey Tracking ────────────────────────────

    def _load_journey(self, language):
        """Load journey JSON for a language, or return empty default"""
        lang_safe = language.lower().replace(" ", "-").replace("/", "-")
        filepath = self.notes_dir / f"journey-{lang_safe}.json"
        if filepath.exists():
            try:
                with open(filepath, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                pass
        return {
            "language": language,
            "sessions": [],
            "concept_tracker": {},
        }

    def _save_journey(self, language, data):
        """Write journey JSON and regenerate the markdown summary"""
        self.notes_dir.mkdir(exist_ok=True)
        lang_safe = language.lower().replace(" ", "-").replace("/", "-")

        json_path = self.notes_dir / f"journey-{lang_safe}.json"
        with open(json_path, 'w') as f:
            json.dump(data, f, indent=2)

        md_path = self.notes_dir / f"journey-{lang_safe}.md"
        with open(md_path, 'w') as f:
            f.write(self._render_journey_markdown(data))

    def _update_journey(self, language, concepts_learned, repo, commits_count):
        """Append session and update concept counters"""
        data = self._load_journey(language)
        date_str = datetime.now().strftime("%Y-%m-%d")
        concept_keys = [c["key"] for c in concepts_learned]

        # Append session
        data["sessions"].append({
            "date": date_str,
            "repo": repo,
            "concepts": concept_keys,
            "commits": commits_count,
        })

        # Update concept tracker
        for c in concepts_learned:
            key = c["key"]
            if key not in data["concept_tracker"]:
                data["concept_tracker"][key] = {
                    "name": c["name"],
                    "level": c["level"],
                    "times_seen": 0,
                    "first_seen": date_str,
                    "last_seen": date_str,
                }
            data["concept_tracker"][key]["times_seen"] += 1
            data["concept_tracker"][key]["last_seen"] = date_str

        self._save_journey(language, data)

    def _get_mastery_status(self, times_seen):
        """Return mastery status based on how many times a concept has been seen"""
        if times_seen >= 3:
            return "Mastered"
        elif times_seen == 2:
            return "Practicing"
        else:
            return "Introduced"

    def _render_journey_markdown(self, data):
        """Render journey JSON into a formatted markdown document"""
        language = data["language"]
        sessions = data.get("sessions", [])
        tracker = data.get("concept_tracker", {})

        lines = [f"# {language} Learning Journey\n"]

        # Summary
        total_sessions = len(sessions)
        total_concepts = len(tracker)

        mastered = [k for k, v in tracker.items() if v["times_seen"] >= 3]
        practicing = [k for k, v in tracker.items() if v["times_seen"] == 2]
        introduced = [k for k, v in tracker.items() if v["times_seen"] == 1]

        # Determine level from highest concept level seen
        max_level = 0
        for v in tracker.values():
            if v.get("level", 0) > max_level:
                max_level = v.get("level", 0)
        level_labels = {0: "Beginner", 1: "Intermediate", 2: "Advanced"}
        level_str = level_labels.get(max_level, "Beginner")

        lines.append(f"**Sessions:** {total_sessions}")
        lines.append(f"**Level:** {level_str}")
        lines.append(f"**Concepts tracked:** {total_concepts}\n")

        if mastered:
            names = [tracker[k].get("name", k) for k in mastered]
            lines.append(f"**Mastered:** {', '.join(names)}")
        if practicing:
            names = [tracker[k].get("name", k) for k in practicing]
            lines.append(f"**Practicing:** {', '.join(names)}")
        if introduced:
            names = [tracker[k].get("name", k) for k in introduced]
            lines.append(f"**Introduced:** {', '.join(names)}")

        lines.append("")

        # Concept tracker table
        if tracker:
            lines.append("## Concept Tracker\n")
            lines.append("| Concept | Level | Times Seen | Status |")
            lines.append("|---------|-------|------------|--------|")
            level_names = {0: "Beginner", 1: "Intermediate", 2: "Advanced"}
            for key, info in sorted(tracker.items(), key=lambda x: (-x[1].get("level", 0), x[0])):
                name = info.get("name", key)
                lvl = level_names.get(info.get("level", 0), "?")
                times = info["times_seen"]
                status = self._get_mastery_status(times)
                lines.append(f"| {name} | {lvl} | {times} | {status} |")
            lines.append("")

        # Session log (last 20)
        if sessions:
            lines.append("## Session Log\n")
            for session in reversed(sessions[-20:]):
                concepts_str = ", ".join(session.get("concepts", [])) or "general"
                lines.append(f"- **{session['date']}** — {session['repo']} ({session['commits']} commits) — {concepts_str}")
            lines.append("")

        lines.append("---\n*Generated by Learning Agent*\n")
        return "\n".join(lines)

    def _generate_journey_progress_section(self, language, concepts_learned):
        """Generate a journey progress section for the daily note"""
        data = self._load_journey(language)
        tracker = data.get("concept_tracker", {})
        sessions = data.get("sessions", [])

        level_labels = {0: "Beginner", 1: "Intermediate", 2: "Advanced"}

        # Determine current level
        max_level = 0
        for v in tracker.values():
            if v.get("level", 0) > max_level:
                max_level = v.get("level", 0)
        level_str = level_labels.get(max_level, "Beginner")

        total_concepts = len(tracker)
        total_sessions = len(sessions) + 1  # +1 for current session (not yet saved)

        mastered = [tracker[k].get("name", k) for k, v in tracker.items() if v["times_seen"] >= 3]
        practicing = [tracker[k].get("name", k) for k, v in tracker.items() if v["times_seen"] == 2]
        new_today = [c["name"] for c in concepts_learned if c["key"] not in tracker]

        parts = []
        parts.append(f"**Level:** {level_str} ({total_concepts} concepts across {total_sessions} sessions)")

        if mastered:
            parts.append(f"**Mastered:** {', '.join(mastered)}")
        if practicing:
            parts.append(f"**Practicing:** {', '.join(practicing)}")
        if new_today:
            parts.append(f"**New today:** {', '.join(new_today)}")

        # Next milestone: find gaps in learning_path
        lang_map = CONCEPT_MAP.get(language)
        if lang_map:
            all_seen = set(tracker.keys()) | {c["key"] for c in concepts_learned}
            for level_idx, group in enumerate(lang_map["learning_path"]):
                missing = [k for k in group if k not in all_seen and k in lang_map["concepts"]]
                if missing:
                    missing_names = [lang_map["concepts"][k]["name"] for k in missing[:3]]
                    lvl_name = level_labels.get(level_idx, "?")
                    parts.append(f"**Next milestone ({lvl_name}):** {', '.join(missing_names)}")
                    break

        if not parts:
            return "Starting your learning journey!"

        return "\n".join(parts)

    def save_to_markdown(self, analysis):
        """Save analysis to markdown file"""
        self.notes_dir.mkdir(exist_ok=True)

        date_str = datetime.now().strftime("%Y-%m-%d")
        repo_safe = analysis['metadata']['repo'].replace('/', '-')
        filename = f"{date_str}_{repo_safe}_{analysis['language']}_{analysis['activity_type']}.md"
        filepath = self.notes_dir / filename

        languages_str = ", ".join(analysis.get("languages", [analysis["language"]]))

        content = f"""# {analysis['language']} - {analysis['activity_type'].capitalize()}

**Date:** {analysis['metadata']['date'][:10]}
**Repository:** {analysis['metadata']['repo']}
**Branch:** {analysis['metadata']['branch']}
**Languages:** {languages_str}
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

        # Update per-language journey tracker
        concepts_learned = analysis.get("concepts_learned", [])
        if concepts_learned:
            self._update_journey(
                analysis["language"],
                concepts_learned,
                analysis["metadata"]["repo"],
                analysis["metadata"]["commits_count"],
            )
            lang_safe = analysis["language"].lower().replace(" ", "-").replace("/", "-")
            print(f"📊 Journey updated: notes/journey-{lang_safe}.md")

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

        # Load recent notes for context
        recent_notes = self._load_recent_notes()

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
        print("=" * 60)
        print("📊 ACTIVITY SUMMARY")
        print("=" * 60)

        total_commits = sum(len(act["commits"]) for act in all_activities)
        total_additions = sum(act["stats"]["additions"] for act in all_activities)
        total_deletions = sum(act["stats"]["deletions"] for act in all_activities)

        print(f"\n✅ Repositories with activity: {len(all_activities)}")
        print(f"📝 Total commits: {total_commits}")
        print(f"📈 Total changes: +{total_additions} -{total_deletions}\n")

        for activity in all_activities:
            activity_type = self.classify_activity(activity)
            # Get diff for language detection
            diff_text = self._get_git_diff(activity["commits"], activity["repo_path"])
            diff_parsed = self._parse_diff(diff_text)
            lang_info = self.detect_languages(activity, diff_parsed)

            # Store parsed data on the activity for later use
            activity["_diff_text"] = diff_text
            activity["_diff_parsed"] = diff_parsed
            activity["_lang_info"] = lang_info

            icon = "📚" if activity_type == "learning" else "💼" if activity_type == "work" else "🔀"
            # Show top 3 languages
            langs_display = ", ".join(lang_info["languages"][:3])
            print(f"{icon} {activity['repo_name']}")
            print(f"   └─ {len(activity['commits'])} commits | {langs_display} | {activity_type}")

        print("\n" + "=" * 60 + "\n")

        # Analyze each repository
        for i, activity in enumerate(all_activities, 1):
            if len(all_activities) > 1:
                print(f"\n{'=' * 60}")
                print(f"Analyzing {i}/{len(all_activities)}: {activity['repo_name']}")
                print('=' * 60 + "\n")

            activity_type = self.classify_activity(activity)
            diff_text = activity.get("_diff_text", "")
            diff_parsed = activity.get("_diff_parsed", {})
            lang_info = activity.get("_lang_info", {"language": "Unknown", "languages": ["Unknown"]})

            analysis = self.analyze_local(activity, activity_type, lang_info, diff_parsed, recent_notes, diff_text)

            print("📖 LEARNING ANALYSIS")
            print("-" * 60 + "\n")

            for section, content in analysis['sections'].items():
                print(f"## {section}")
                print(content)
                print()

            self.save_to_markdown(analysis)

            if i < len(all_activities):
                print("\n" + "=" * 60)

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
        print("   Run 'learning-agent-local help' for usage")

if __name__ == "__main__":
    main()
