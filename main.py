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
        logger.info(f"Baking process completed for {input_file}")
        logger.info(f"Output saved to {output_file}")
        return True
    except Exception as e:
        logger.error(f"Error during texture transform baking: {str(e)}")
        return False

def main():
    logger = setup_logging()
    logger.info("Starting main process")

    input_file = 'scene2.glb'
    output_file = 'scene2_baked.glb'

if __name__ == "__main__":
    main()
