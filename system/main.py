import sys
import logging
from main import main

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"An error occurred in the main program: {str(e)}")
        sys.exit(1)
