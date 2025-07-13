import os
import logging
from pathlib import Path
from typing import List, Dict, Any
import pypdf
from pypdf import PdfReader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CustomPDFParser:
  def __init__(
      self,extract_images: bool = False,preserve_layout: bool = True,remove_headers_footers: bool = True,min_text_length: int = 10
  ):
      """
      Initialize the parser with options to extract images, preserve layout, remove repeated headers/footers, and minimum text length for pages.
      Args:
          extract_images: Whether to extract image info from pages
          preserve_layout: Whether to keep layout spacing in text extraction
          remove_headers_footers: Whether to detect and remove headers/footers
          min_text_length: Minimum length of text for a page to be considered valid
      """
      self.extract_images = extract_images
      self.preserve_layout = preserve_layout
      self.remove_headers_footers = remove_headers_footers
      self.min_text_length = min_text_length
  def extract_text_from_page(self, page: pypdf.PageObject, page_num: int) -> Dict[str, Any]:
      """
      Extract text and metadata from a single PDF page.
      Args:
          page: PyPDF page object
          page_num: zero-based page number
      Returns:
          dict with keys:
              - 'text': extracted and cleaned text string,
              - 'metadata': page metadata dict,
              - 'word_count': number of words in extracted text
      """
      try:
          if self.preserve_layout:
              text = page.extract_text(extraction_mode="layout")
          else:
              text = page.extract_text()
          text = self._clean_text(text)
          metadata = {
              "page_number": page_num + 1,  # 1-based numbering
              "rotation": getattr(page, "rotation", 0),
              "mediabox": str(getattr(page, "mediabox", None)),
          }
          if self.extract_images:
              metadata["images"] = self._extract_image_info(page)
          return {
              "text": text,
              "metadata": metadata,
              "word_count": len(text.split()) if text else 0
          }
      except Exception as e:
          logger.error(f"Error extracting page {page_num}: {e}")
          return {
              "text": "",
              "metadata": {"page_number": page_num + 1, "error": str(e)},
              "word_count": 0
          }
      
  def _clean_text(self, text: str) -> str:
      """
      Clean and normalize extracted text, preserving paragraph breaks.
      Args:
          text: raw text extracted from PDF page
      Returns:
          cleaned text string
      """
      if not text:
          return ""
      lines = text.split('\n')
      cleaned_lines = []
      for line in lines:
          line = line.strip()
          if line:
              cleaned_lines.append(line)
          elif cleaned_lines and cleaned_lines[-1]:
              cleaned_lines.append("")
      cleaned_text = '\n'.join(cleaned_lines)
      while '\n\n\n' in cleaned_text:
          cleaned_text = cleaned_text.replace('\n\n\n', '\n\n')
      return cleaned_text.strip()
  
  def _extract_image_info(self, page: pypdf.PageObject) -> List[Dict[str, Any]]:
      """
      Extract basic image metadata from page, if available.
      Args:
          page: PyPDF page object
      Returns:
          List of dictionaries with image info (index, name, width, height)
      """
      images = []
      try:
          if hasattr(page, 'images'):
              for i, image in enumerate(page.images):
                  images.append({
                      "image_index": i,
                      "name": getattr(image, 'name', f"image_{i}"),
                      "width": getattr(image, 'width', None),
                      "height": getattr(image, 'height', None)
                  })
      except Exception as e:
          logger.warning(f"Image extraction failed: {e}")
      return images

  def _remove_headers_footers(self, pages_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
      """
      Remove repeated headers and footers that appear on many pages.
      This is done by identifying lines appearing on over 50% of pages
      at the start or end of page text, then removing those lines.
      Args:
          pages_data: List of dictionaries representing each page's extracted data.
      Returns:
          Updated list of pages with headers/footers removed
      """
      if len(pages_data) < 3 or not self.remove_headers_footers:
          return pages_data
      first_lines = [page["text"].split('\n')[0] if page["text"] else "" for page in pages_data]
      last_lines = [page["text"].split('\n')[-1] if page["text"] else "" for page in pages_data]
      threshold = len(pages_data) * 0.5
      potential_headers = [line for line in set(first_lines)
                          if first_lines.count(line) > threshold and line.strip()]
      potential_footers = [line for line in set(last_lines)
                          if last_lines.count(line) > threshold and line.strip()]
      for page_data in pages_data:
          lines = page_data["text"].split('\n')
          if lines and potential_headers:
              for header in potential_headers:
                  if lines[0].strip() == header.strip():
                      lines = lines[1:]
                      break
          if lines and potential_footers:
              for footer in potential_footers:
                  if lines[-1].strip() == footer.strip():
                      lines = lines[:-1]
                      break

          page_data["text"] = '\n'.join(lines).strip()
      return pages_data
  def _extract_document_metadata(self, pdf_reader: PdfReader, pdf_path: str) -> Dict[str, Any]:
      """
      Extract metadata from the PDF document itself.
      Args:
          pdf_reader: PyPDF PdfReader instance
          pdf_path: path to PDF file
      Returns:
          Dictionary of metadata including file info and PDF document metadata
      """
      metadata = {
          "file_path": pdf_path,
          "file_name": Path(pdf_path).name,
          "file_size": os.path.getsize(pdf_path) if os.path.exists(pdf_path) else None,
      }
      try:
          if pdf_reader.metadata:
              metadata.update({
                  "title": pdf_reader.metadata.get('/Title', ''),
                  "author": pdf_reader.metadata.get('/Author', ''),
                  "subject": pdf_reader.metadata.get('/Subject', ''),
                  "creator": pdf_reader.metadata.get('/Creator', ''),
                  "producer": pdf_reader.metadata.get('/Producer', ''),
                  "creation_date": str(pdf_reader.metadata.get('/CreationDate', '')),
                  "modification_date": str(pdf_reader.metadata.get('/ModDate', '')),
              })
      except Exception as e:
          logger.warning(f"Metadata extraction failed: {e}")
      return metadata
  def parse_pdf(self, pdf_path: str) -> Dict[str, Any]:
      """
      Parse the entire PDF file. Opens the file, extracts text and metadata page by page, removes headers/footers if configured, and aggregates results.
      Args:
          pdf_path: Path to the PDF file
      Returns:
          Dictionary with keys:
              - 'full_text': combined text from all pages,
              - 'pages': list of page-wise dicts with text and metadata,
              - 'document_metadata': file and PDF metadata,
              - 'total_pages': total pages in PDF,
              - 'processed_pages': number of pages kept after filtering,
              - 'total_words': total word count of parsed text
      """
      try:
          with open(pdf_path, 'rb') as file:
              pdf_reader = PdfReader(file)
              doc_metadata = self._extract_document_metadata(pdf_reader, pdf_path)
              pages_data = []
              for i, page in enumerate(pdf_reader.pages):
                  page_data = self.extract_text_from_page(page, i)
                  if len(page_data["text"]) >= self.min_text_length:
                      pages_data.append(page_data)
              pages_data = self._remove_headers_footers(pages_data)
              full_text = '\n\n'.join(page["text"] for page in pages_data if page["text"])
              return {
                  "full_text": full_text,
                  "pages": pages_data,
                  "document_metadata": doc_metadata,
                  "total_pages": len(pdf_reader.pages),
                  "processed_pages": len(pages_data),
                  "total_words": sum(page["word_count"] for page in pages_data)
              }
      except Exception as e:
          logger.error(f"Failed to parse PDF {pdf_path}: {e}")
          raise