import logging
import os
import sys
from bake_texture_transform import bake_texture_transform
from git_operations import git_commit_and_push

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger(__name__)

def process_scene2_glb(logger):
    input_file = 'scene2.glb'
    output_file = 'scene2_baked.glb'
    
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

    try:
        success = process_scene2_glb(logger)
        if success:
            logger.info("scene2.glb processed successfully")
            # Commit and push changes
            git_commit_and_push("Updated scene2_baked.glb")
        else:
            logger.warning("Failed to process scene2.glb")

    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)

    logger.info("Main process completed")

if __name__ == "__main__":
    main()
