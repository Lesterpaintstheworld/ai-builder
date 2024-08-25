import logging
import os
import sys
from bake_texture_transform import bake_texture_transform, logger
from git_operations import git_commit_and_push, get_current_branch, get_last_commit_hash

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger(__name__)

def main():
    logger = setup_logging()
    logger.info("Starting main process")

    try:
        if process_glb_file(logger, input_file, output_file):
            commit_message = f"Processed {input_file} to {output_file}"
            current_branch = get_current_branch()
            last_commit = get_last_commit_hash()
            logger.info(f"Current branch: {current_branch}")
            logger.info(f"Last commit hash: {last_commit}")
            if git_commit_and_push(commit_message):
                logger.info("Changes committed and pushed successfully")
            else:
                logger.error("Failed to commit and push changes")
        else:
            logger.error("Failed to process GLB file")
    except Exception as e:
        logger.error(f"An error occurred in the main process: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
