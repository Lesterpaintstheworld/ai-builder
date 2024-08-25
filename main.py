import logging
import os
import sys
from add_files import main as add_files_main
from bake_texture_transform import bake_texture_transform
def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger(__name__)

def add_files(logger):
    logger.info("Starting to add files...")
    try:
        with open('files_to_add.txt', 'r') as f:
            files_to_add = [line.strip() for line in f]
        logger.info(f"Files to add: {files_to_add}")
        files_added = []
        files_not_found = []
        for file in files_to_add:
            if os.path.exists(file):
                files_added.append(file)
                logger.info(f"Added file: {file}")
            else:
                files_not_found.append(file)
                logger.warning(f"File not found: {file}")
        logger.info(f"Successfully added {len(files_added)} files")
        if files_not_found:
            logger.warning(f"Files not found: {', '.join(files_not_found)}")
        return files_added
    except Exception as e:
        logger.error(f"Error while adding files: {str(e)}")
        return []

from bake_texture_transform import bake_texture_transform

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
        else:
            logger.warning("Failed to process scene2.glb")

    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)

    logger.info("Main process completed")

if __name__ == "__main__":
    main()
