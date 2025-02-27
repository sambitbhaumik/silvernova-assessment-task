import logging
import os
from pathlib import Path
import pypdf
from docx import Document
import pandas as pd
import extract_msg
from typing import Optional, Dict
import re
from typing import List, Dict, Any

logger = logging.getLogger('markdown-extractor')

class MarkdownExtractor:
    """Extracts content from legal document types and converts to formatted markdown"""

    SUPPORTED_EXTENSIONS = {'.pdf', '.docx', '.xlsx', '.msg'}

    def __init__(self):
        logger.info('MarkdownExtractor initialized')

    def extract_from_directory(self, input_dir: str, output_dir: str) -> Dict[str, str]:
        """
        Extracts content from all the source files and returns markdown content
        
        Args:
            input_dir: Directory containing source documents
            output_dir: Directory to save markdown files
        Returns:
            Dict mapping filenames to their markdown content
        """
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        results = {}
        
        for file_path in input_path.glob('**/*'):
            if file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                try:
                    content = self.extract_content(file_path)
                    if content:
                        markdown_content = self.format_markdown(content, file_path.name)
                        output_file = output_path / f"{file_path.stem}.md"
                        output_file.write_text(markdown_content, encoding='utf-8')
                        results[file_path.name] = markdown_content
                        logger.info(f"Extracted {file_path.name}")
                except Exception as e:
                    logger.error(f"Failed to extract {file_path}: {str(e)}")
        
        return results

    def extract_content(self, file_path: Path) -> Optional[str]:
        """Extract content from a file based on its extension"""
        ext = file_path.suffix.lower()
        
        try:
            if ext == '.pdf':
                return self._extract_pdf(file_path)
            elif ext == '.docx':
                return self._extract_docx(file_path)
            elif ext == '.xlsx':
                return self._extract_xlsx(file_path)
            elif ext == '.msg':
                return self._extract_msg(file_path)
        except Exception as e:
            logger.error(f"Error extracting {file_path}: {str(e)}")
            return None

    def _extract_pdf(self, file_path: Path) -> str:
        text_parts = []
        with open(file_path, 'rb') as file:
            reader = pypdf.PdfReader(file)
            for page_num, page in enumerate(reader.pages, 1):
                text = page.extract_text()
                if text.strip():
                    text_parts.append(f"## Page {page_num}\n\n{text}")
        return '\n\n'.join(text_parts)

    def _extract_docx(self, file_path: Path) -> str:
        doc = Document(file_path)
        sections = []
        
        for para in doc.paragraphs:
            if para.text.strip():
                # Check if it's a heading
                if para.style.name.startswith('Heading'):
                    sections.append(f"{'#' * int(para.style.name[-1])} {para.text}")
                else:
                    sections.append(para.text)
        
        return '\n\n'.join(sections)

    def _extract_xlsx(self, file_path: Path) -> str:
        df = pd.read_excel(file_path, sheet_name=None)
        sections = []
        
        for sheet_name, sheet_df in df.items():
            sections.append(f"## Sheet: {sheet_name}\n")
            sections.append(sheet_df.to_markdown(index=False))
            sections.append("\n")
        
        return '\n'.join(sections)
    
    def create_hierarchical_chunks(self, content: str, filename: str) -> List[Dict[str, Any]]:
        """
        Creates hierarchical chunks from document content.

        This function processes the provided document content to create structured chunks 
        based on headers and sections. It identifies headers to determine the hierarchy 
        of sections and organizes the content accordingly. Each chunk includes metadata 
        about its source, section title, context, and level.

        Args:
            content (str): The content of the document to be processed.
            filename (str): The name of the file from which the content was extracted.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each representing a chunk of 
            content with associated metadata.
        """
        chunks = []
        current_section = {"title": "", "content": [], "level": 0}
        section_stack = []
        
        lines = content.split('\n')
        buffer = []
        
        for line in lines:
            # Detect headers (e.g., "1.", "1.1", "1.1.1" or "#", "##", "###")
            if line.strip():
                is_header = bool(re.match(r'^#+\s|^\d+(\.\d+)*\s', line.strip()))
                header_level = len(re.findall(r'#|\.', line)) if is_header else 0
                
                if is_header:
                    # Process previous buffer if exists
                    if buffer:
                        chunk_text = '\n'.join(buffer)
                        if current_section["title"]:
                            context = " > ".join(s["title"] for s in section_stack + [current_section])
                            chunks.append({
                                "content": chunk_text,
                                "metadata": {
                                    "source": filename,
                                    "section": current_section["title"],
                                    "context": context,
                                    "level": current_section["level"]
                                }
                            })
                        buffer = []
                    
                    # Update section stack when section level changes
                    while section_stack and section_stack[-1]["level"] >= header_level:
                        section_stack.pop()
                    
                    current_section = {"title": line.strip(), "level": header_level}
                    section_stack.append(current_section)
                else:
                    buffer.append(line)
                    
                    # Create chunk when buffer gets too large
                    if len('\n'.join(buffer)) > 500:  # Adjust size as needed
                        chunk_text = '\n'.join(buffer)
                        context = " > ".join(s["title"] for s in section_stack)
                        chunks.append({
                            "content": chunk_text,
                            "metadata": {
                                "source": filename,
                                "section": current_section["title"],
                                "context": context,
                                "level": current_section["level"]
                            }
                        })
                        # Keep last paragraph for overlap
                        buffer = buffer[-1:] if buffer else []
        
        # processing the last buffer
        if buffer:
            chunk_text = '\n'.join(buffer)
            context = " > ".join(s["title"] for s in section_stack)
            chunks.append({
                "content": chunk_text,
                "metadata": {
                    "source": filename,
                    "section": current_section["title"],
                    "context": context,
                    "level": current_section["level"]
                }
            })
        
        return chunks

    def _extract_msg(self, file_path: Path) -> str:
        msg = extract_msg.Message(file_path)
        sections = [
            f"# Email: {msg.subject}",
            f"**From:** {msg.sender}",
            f"**To:** {msg.to}",
            f"**Date:** {msg.date}",
            "",
            "## Body",
            msg.body
        ]
        
        if msg.attachments:
            sections.extend([
                "",
                "## Attachments",
                ", ".join(att.filename for att in msg.attachments)
            ])
        
        return '\n\n'.join(sections)

    def format_markdown(self, content: str, original_filename: str) -> str:
        """Format extracted content as markdown with metadata"""
        header = f"""# Content from {original_filename}

        """
        return header + content.strip()