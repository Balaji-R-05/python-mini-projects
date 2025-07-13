# PDF Parser

A flexible PDF parsing and processing pipeline with support for text extraction, metadata, image info, header/footer removal, and integration with [LangChain](https://github.com/langchain-ai/langchain).

## Features

- Extracts clean text from PDFs, with optional layout preservation
- Removes repeated headers and footers
- Extracts per-page and document-level metadata
- Optionally extracts image metadata from pages
- Outputs:
  - Raw parsed data (dict)
  - Full plain text
  - [LangChain](https://github.com/langchain-ai/langchain) `Document` objects (with or without chunking)
- Interactive CLI example
