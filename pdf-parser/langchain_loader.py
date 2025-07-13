from typing import List, Optional, Dict, Any
from langchain.schema import Document
from langchain.document_loaders.base import BaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from parser import CustomPDFParser

class LangChainPDFLoader(BaseLoader):
   def __init__(
       self,file_path: str,parser_config: Optional[Dict[str, Any]] = None,chunk_size: int = 500, chunk_overlap: int = 50
   ):
       """
       Initialize the loader with the PDF file path, parser configuration, and chunking parameters.
       Args:
           file_path: path to PDF file
           parser_config: dictionary of parser options
           chunk_size: chunk size for splitting long texts
           chunk_overlap: chunk overlap for splitting
       """
       self.file_path = file_path
       self.parser_config = parser_config or {}
       self.chunk_size = chunk_size
       self.chunk_overlap = chunk_overlap
       self.parser = CustomPDFParser(**self.parser_config)

   def load(self) -> List[Document]:
       """
       Load PDF, parse pages, and convert each page to a LangChain Document.
       Returns:
           List of Document objects with page text and combined metadata.
       """
       parsed_data = self.parser.parse_pdf(self.file_path)
       documents = []
       for page_data in parsed_data["pages"]:
           if page_data["text"]:
               metadata = {**parsed_data["document_metadata"], **page_data["metadata"]}
               doc = Document(page_content=page_data["text"], metadata=metadata)
               documents.append(doc)
       return documents
   
   def load_and_split(self) -> List[Document]:
       """
       Load the PDF and split large documents into smaller chunks.
       Returns:
           List of Document objects after splitting large texts.
       """
       documents = self.load()
       text_splitter = RecursiveCharacterTextSplitter(
           chunk_size=self.chunk_size,
           chunk_overlap=self.chunk_overlap,
           separators=["\n\n", "\n", " ", ""]
       )
       split_docs = text_splitter.split_documents(documents)
       return split_docs