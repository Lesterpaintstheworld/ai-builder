import subprocess
import logging
import os

logger = logging.getLogger(__name__)

def run_git_command(command, error_message):
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        logger.info(f"Git command successful: {' '.join(command)}")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logger.error(f"{error_message}: {e}")
        logger.error(f"Command output: {e.output}")
        raise

def git_commit_and_push(commit_message):
    try:
        # Check if we're in a git repository
        if not os.path.exists('.git'):
            raise Exception("Not a git repository")

        # Stage all changes
        run_git_command(["git", "add", "."], "Failed to stage changes")

        # Commit changes
        run_git_command(["git", "commit", "-m", commit_message], "Failed to commit changes")

        # Push changes
        run_git_command(["git", "push"], "Failed to push changes")

        logger.info(f"Successfully committed and pushed changes with message: {commit_message}")

    except Exception as e:
        logger.error(f"Git operation failed: {e}")
        raise

def get_current_branch():
    return run_git_command(["git", "rev-parse", "--abbrev-ref", "HEAD"], "Failed to get current branch")

def get_last_commit_hash():
    return run_git_command(["git", "rev-parse", "HEAD"], "Failed to get last commit hash")
import subprocess
import logging

logger = logging.getLogger(__name__)

def git_commit_and_push(message):
    try:
        # Stage all changes
        subprocess.run(["git", "add", "."], check=True)
        logger.info("Staged all changes")

        # Commit changes
        subprocess.run(["git", "commit", "-m", message], check=True)
        logger.info(f"Committed changes with message: {message}")

        # Push changes
        subprocess.run(["git", "push"], check=True)
        logger.info("Pushed changes to remote repository")

        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Git operation failed: {e}")
        return False
