from typing import List, Optional, Dict, Any
from langchain.schema import Document
from parser import CustomPDFParser
from langchain_loader import LangChainPDFLoader
import logging

logger = logging.getLogger(__name__)

class PDFProcessingPipeline:
   def __init__(self, parser_config: Optional[Dict[str, Any]] = None):
       """
       Args:
          parser_config: dictionary of options passed to CustomPDFParser
       """
       self.parser_config = parser_config or {}
   def process_single_pdf(
       self,pdf_path: str,output_format: str = "langchain",chunk_documents: bool = True,chunk_size: int = 500,chunk_overlap: int = 50
   ) -> Any:
       """
       Args:
           pdf_path: path to PDF file
           output_format: "raw" (dict), "langchain" (Documents), or "text" (string)
           chunk_documents: whether to split LangChain documents into chunks
           chunk_size: chunk size for splitting
           chunk_overlap: chunk overlap for splitting
       Returns:
           Parsed content in the requested format
       """
       if output_format == "raw":
           parser = CustomPDFParser(**self.parser_config)
           return parser.parse_pdf(pdf_path)
       elif output_format == "langchain":
           loader = LangChainPDFLoader(pdf_path, self.parser_config, chunk_size, chunk_overlap)
           if chunk_documents:
               return loader.load_and_split()
           else:
               return loader.load()
       elif output_format == "text":
           parser = CustomPDFParser(**self.parser_config)
           parsed_data = parser.parse_pdf(pdf_path)
           return parsed_data.get("full_text", "")
       else:
           raise ValueError(f"Unknown output_format: {output_format}")