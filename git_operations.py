import subprocess
import logging

logger = logging.getLogger(__name__)

def git_commit_and_push(commit_message):
    try:
        # Stage all changes
        subprocess.run(["git", "add", "."], check=True)
        logger.info("Staged all changes")

        # Commit changes
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        logger.info(f"Committed changes with message: {commit_message}")

        # Push changes
        subprocess.run(["git", "push"], check=True)
        logger.info("Pushed changes to remote repository")

    except subprocess.CalledProcessError as e:
        logger.error(f"Git operation failed: {e}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise
