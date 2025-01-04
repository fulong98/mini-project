#!/usr/bin/env python3

import os
import random
import time
import datetime
import subprocess

# ---- CONFIGURABLE PARAMETERS ----
PROJECT_DIR = "my_private_useless_project"  # Local folder name
REMOTE_URL = "git@github.com:your-username/your-private-repo.git"  
BRANCH_NAME = "main"

# Probability of skipping all commits (10%)
SKIP_THRESHOLD = 0.10

# Range of commits if not skipped
MIN_COMMITS = 1
MAX_COMMITS = 10

# Sleep range between commits in seconds (e.g., 5-30 minutes)
MIN_SLEEP = 5 * 60
MAX_SLEEP = 30 * 60

# Some realistic-ish commit messages to choose from
COMMIT_MESSAGES = [
    "Fix typo in documentation",
    "Update usage instructions",
    "Refactor minor code details",
    "Enhance build script",
    "Improve configuration",
    "Update README with new info",
    "Add more notes to documentation",
    "Adjust project structure",
    "Minor improvements",
    "Refactor for clarity"
]


def run_command(cmd):
    """
    Helper function to run shell commands with error handling.
    """
    print(f"> {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error running command:", result.stderr)
    else:
        if result.stdout.strip():
            print("Output:", result.stdout.strip())
    return result


def initialize_repo_if_needed():
    """
    Checks if the project folder exists. If not, create it, init Git, 
    add a README and connect to remote (first-time setup only).
    """
    if not os.path.isdir(PROJECT_DIR):
        print(f"Creating folder: {PROJECT_DIR}")
        os.makedirs(PROJECT_DIR, exist_ok=True)

    os.chdir(PROJECT_DIR)

    # Check if it's already a Git repo
    if not os.path.isdir(".git"):
        print("Initializing new Git repository...")
        run_command("git init")

        # Create a basic README and NOTES if not present
        if not os.path.isfile("README.md"):
            with open("README.md", "w") as f:
                f.write("# Useless Private Project\n\n")
                f.write("This is an automatically updated project for daily commits.\n")

        if not os.path.isfile("NOTES.md"):
            with open("NOTES.md", "w") as f:
                f.write("# Notes\n\nInitial notes file.\n")

        # Stage and commit initial files
        run_command("git add README.md NOTES.md")
        run_command('git commit -m "Initial commit (auto)"')

        # Add remote if needed (uncomment if you haven’t set it manually)
        # run_command(f"git remote add origin {REMOTE_URL}")
        
        # Push initial commit (uncomment once remote is set)
        # run_command(f"git push -u origin {BRANCH_NAME}")

    else:
        print("Git repository already initialized.")


def make_commits():
    """
    Decides how many commits to make today (1–3) and makes them over time,
    each with a realistic commit message. Pushes changes after final commit.
    """
    num_commits = random.randint(MIN_COMMITS, MAX_COMMITS)
    print(f"Will make {num_commits} commits today.")

    for i in range(num_commits):
        # Randomly choose a commit message
        commit_message = random.choice(COMMIT_MESSAGES)

        # Update NOTES.md with a short line to simulate a real change
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"- {now_str} : {commit_message}\n"
        with open("NOTES.md", "a") as f:
            f.write(line)

        # Add & commit
        run_command("git add NOTES.md")
        run_command(f'git commit -m "{commit_message}"')

        # If this isn't the last commit, sleep a random time before next commit
        if i < num_commits - 1:
            sleep_seconds = random.randint(MIN_SLEEP, MAX_SLEEP)
            print(f"Sleeping for ~{sleep_seconds // 60} minutes.")
            time.sleep(sleep_seconds)

    # Push all commits at once at the end
    print("Pushing commits to remote...")
    run_command(f"git push origin {BRANCH_NAME}")


def daily_commit():
    """
    Main logic:
      1. Check if we skip commits (10% chance).
      2. If not skipped, do 1–3 commits at random intervals.
    """
    chance = random.random()
    if chance < SKIP_THRESHOLD:
        print(f"Skipping commits today (chance={chance:.2f}).")
        return
    else:
        print(f"Proceeding with commits (chance={chance:.2f}).")
        make_commits()


if __name__ == "__main__":
    # 1) Initialize or move into the repo if needed
    # initialize_repo_if_needed()

    # 2) Run daily commit logic
    daily_commit()
