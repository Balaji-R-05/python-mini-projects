import os
from pathlib import Path
from pipeline import PDFProcessingPipeline  # Add this line if your class is in pipeline.py

def main():
   print("👋 Welcome to the Custom PDF Parser!")
   print("What would you like to do?")
   print("1. View full parsed raw data")
   print("2. Extract full plain text")
   print("3. Get LangChain documents (no chunking)")
   print("4. Get LangChain documents (with chunking)")
   print("5. Show document metadata")
   print("6. Show per-page metadata")
   print("7. Show cleaned page text (header/footer removed)")
   print("8. Show extracted image metadata")
   choice = input("Enter the number of your choice: ").strip()
   if choice not in {'1', '2', '3', '4', '5', '6', '7', '8'}:
       print("❌ Invalid option.")
       return
   file_path = input("Enter the path to your PDF file: ").strip()
   if not Path(file_path).exists():
       print("❌ File not found.")
       return
   # Initialize pipeline
   pipeline = PDFProcessingPipeline({
       "preserve_layout": False,
       "remove_headers_footers": True,
       "extract_images": True,
       "min_text_length": 20
   })
   # Raw data is needed for most options
   parsed = pipeline.process_single_pdf(file_path, output_format="raw")
   if choice == '1':
       print("\nFull Raw Parsed Output:")
       for k, v in parsed.items():
           print(f"{k}: {str(v)[:300]}...")
   elif choice == '2':
       print("\nFull Cleaned Text (truncated preview):")
       print("Previewing the first 1000 characters:\n"+parsed["full_text"][:1000], "...")
   elif choice == '3':
       docs = pipeline.process_single_pdf(file_path, output_format="langchain", chunk_documents=False)
       print(f"\nLangChain Documents: {len(docs)}")
       print("Previewing the first 500 characters:\n", docs[0].page_content[:500], "...")
   elif choice == '4':
       docs = pipeline.process_single_pdf(file_path, output_format="langchain", chunk_documents=True)
       print(f"\nLangChain Chunks: {len(docs)}")
       print("Sample chunk content (first 500 chars):")
       print(docs[0].page_content[:500], "...")
   elif choice == '5':
       print("\nDocument Metadata:")
       for key, value in parsed["document_metadata"].items():
           print(f"{key}: {value}")
   elif choice == '6':
       print("\nPer-page Metadata:")
       for i, page in enumerate(parsed["pages"]):
           print(f"Page {i+1}: {page['metadata']}")
   elif choice == '7':
       print("\nCleaned Text After Header/Footer Removal.")
       print("Showing the first 3 pages and first 500 characters of the text from each page.")
       for i, page in enumerate(parsed["pages"][:3]):  # First 3 pages
           print(f"\n--- Page {i+1} ---")
           print(page["text"][:500], "...")
   elif choice == '8':
       print("\nExtracted Image Metadata (if available):")
       found = False
       for i, page in enumerate(parsed["pages"]):
           images = page["metadata"].get("images", [])
           if images:
               found = True
               print(f"\n--- Page {i+1} ---")
               for img in images:
                   print(img)
       if not found:
           print("No image metadata found.")
if __name__ == "__main__":
   main()