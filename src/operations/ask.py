from typing import List, Dict, Any
from src.api import execute_prompt
from src.operations.search import SearchEngine

class LLMAsker:
    def __init__(self):
        self.search_engine = SearchEngine()

    def ask(self, question: str) -> str:
        # First, search for relevant context
        relevant_docs = self.search_engine.search(question)
        
        # Build context from relevant documents
        context = self._build_context(relevant_docs)
        
        # Create the prompt
        prompt = self._create_prompt(question, context)
        
        # Get response from LLM
        print('We are processing your question. Please wait...')
        response = execute_prompt(prompt)
        
        return response['response']

    def _build_context(self, docs: List[Dict[str, Any]]) -> str:
        """
        Constructs a context string from a list of documents.

        This method takes a list of documents, extracts relevant metadata and content,
        and formats them into a structured string that provides context for a given question.

        :param docs: A list of documents, where each document is a dictionary containing
                     'metadata' and 'content' keys.
        :return: A formatted string containing the context derived from the documents.
        """
        context_parts = []
        for doc in docs:
            metadata = doc['metadata']
            context_parts.append(
                f"From {metadata['source']}, section '{metadata['context']}':\n{doc['content']}\n"
            )
        return "\n".join(context_parts)

    def _create_prompt(self, question: str, context: str) -> str:
        return f"""You are a legal assistant helping to answer questions about various legal documents. 
                Please answer the following question based on the provided context. 

                Important guidelines:
                1. Be very specific in your references
                2. If multiple documents support your answer, reference all of them
                3. Use direct quotes when appropriate
                4. If the information is not in the context, say so
                5. Structure your answer clearly, with references inline

                Context:
                {context}

                Question: {question}

                Answer:"""