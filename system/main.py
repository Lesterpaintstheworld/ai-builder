import sys
import logging
from git_operations import git_commit_and_push, get_current_branch, get_last_commit_hash

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger(__name__)

def main():
    logger = setup_logging()
    logger.info("Starting main process")

    try:
        # Commit and push changes
        commit_message = "Update main process"
        current_branch = get_current_branch()
        last_commit = get_last_commit_hash()
        logger.info(f"Current branch: {current_branch}")
        logger.info(f"Last commit hash: {last_commit}")
        if git_commit_and_push(commit_message):
            logger.info("Changes committed and pushed successfully")
        else:
            logger.error("Failed to commit and push changes")
    except Exception as e:
        logger.error(f"An error occurred in the main process: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
