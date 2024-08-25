import logging
import os
import sys
from bake_texture_transform import bake_texture_transform, logger
from git_operations import git_commit_and_push

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger(__name__)

def process_glb_file(logger, input_file, output_file):
    if not os.path.exists(input_file):
        logger.error(f"Input file {input_file} not found.")
        return False

    logger.info(f"Starting texture transform baking process for {input_file}")
    try:
        bake_texture_transform(input_file, output_file)
        logger.info(f"Successfully processed {input_file} and saved result to {output_file}")
        return True
    except Exception as e:
        logger.error(f"Error during texture transform baking: {str(e)}")
        return False

def main():
    logger = setup_logging()
    logger.info("Starting main process")

    input_file = 'scene2.glb'
    output_file = 'scene2_baked.glb'

    try:
        logger.info(f"Processing {input_file}")
        bake_texture_transform(input_file, output_file)
        logger.info(f"{input_file} processed successfully")
        # Commit and push changes
        git_commit_and_push(f"Updated {output_file}")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
    finally:
        logger.info("Main process completed")

if __name__ == "__main__":
    main()
