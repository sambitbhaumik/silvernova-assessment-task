import dotenv
dotenv.load_dotenv()

from src import App
import logging
import logging.config
import os
import argparse

log_file_path = os.path.join(os.path.dirname(__file__), 'logging.conf')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='RAG System for Legal Documents')
    parser.add_argument('--mode', type=str, choices=['get-markdown', 'index-files', 'search', 'ask-question'],
                      help='Operation mode')
    parser.add_argument('query', nargs='?', help='Query for search or question mode')
    
    args = parser.parse_args()
    app = App()
    
    if args.mode == 'get-markdown':
        app.get_markdown()
    elif args.mode == 'index-files':
        app.load_files()
    elif args.mode == 'search' and args.query:
        app.search(args.query)
    elif args.mode == 'ask-question' and args.query:
        app.ask_question(args.query)
    else:
        if args.query:
            # Default mode is ask-question
            app.ask_question(args.query)
        else:
            parser.print_help()