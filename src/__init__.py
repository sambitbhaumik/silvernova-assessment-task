import logging
from pathlib import Path
from src.operations.ask import LLMAsker
from src.operations.search import SearchEngine
from src.operations.embed import EmbedService
from src.operations.extract import MarkdownExtractor
import argparse

class App:
    def __init__(self):
        self.extractor = MarkdownExtractor()
        self.embed_service = EmbedService()
        self.search_engine = SearchEngine()
        self.asker = LLMAsker()

    def load_files(self):
        # Extract markdown from documents
        markdown_dir = Path('markdown_output')
        markdown_contents = {}
        
        
        # Read all markdown files in the directory
        for file_path in markdown_dir.glob('*.md'):
            with open(file_path, 'r', encoding='utf-8') as f:
                markdown_contents[file_path.name] = f.read()
        
        for filename, content in markdown_contents.items():
            chunks = self.extractor.create_hierarchical_chunks(content, filename)
            
            for chunk in chunks:
                self.embed_service.embed_and_store(chunk["content"], chunk["metadata"])
                
        print("Files have been indexed successfully!")

    def search(self, query):
        results = self.search_engine.search(query)
        
        print("\nSearch Results:")
        for i, result in enumerate(results, 1):
            print(f"\n{i}. Source: {result['metadata']['source']}")
            print(f"Section: {result['metadata']['section']}")
            print(f"Context: {result['metadata']['context']}")
            print(f"Similarity: {result['similarity']:.4f}")
            print(f"Content: {result['content'][:200]}...")


    def get_markdown(self):
        """
        This function reads all documents from the 'documents' directory, processes them to 
        generate markdown files, and saves the results in the 'markdown_output' directory.

        Returns:
            None
        """
        docs_dir = Path('documents')
        markdown_dir = Path('markdown_output')
        
        results = self.extractor.extract_from_directory(
            str(docs_dir), 
            str(markdown_dir)
        )
        
        print("Markdown files have been generated in the markdown_output directory")
        for filename in results.keys():
            print(f"- {filename}")

    def ask_question(self, question):
        logging.info(f'Asking question: {question}')
        response = self.asker.ask(question)
        print(response)