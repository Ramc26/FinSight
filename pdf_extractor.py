# pdf_extractor.py
import pymupdf
import os
import csv
import logging
from pathlib import Path
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFExtractor:
    def __init__(self):
        logger.info("Initializing PDFExtractor")
        self.extraction_count = 0
        logger.info("PDFExtractor initialized successfully")
    
    def unlock_pdf(self, pdf_path, password=None):
        logger.info(f"Attempting to open PDF: {pdf_path}")
        try:
            doc = pymupdf.open(pdf_path)
            if doc.needs_pass:
                logger.info("PDF is password protected.")
                if not password:
                    logger.error("Password required but not provided.")
                    return None
                
                if doc.authenticate(password):
                    logger.info("PDF unlocked successfully.")
                    return doc
                else:
                    logger.error("Incorrect password provided.")
                    return None
            return doc
        except Exception as e:
            logger.error(f"Error opening PDF: {e}")
            return None
    
    # This function signature is the one that needs to be updated.
    def extract_pdf_content(self, pdf_path, output_dir=None, password=None):
        logger.info(f"Starting PDF content extraction: {pdf_path}")
        
        doc = self.unlock_pdf(pdf_path, password=password)
        if doc is None:
            logger.error("Failed to open or unlock the PDF document.")
            return None

        if output_dir is None:
            pdf_name = Path(pdf_path).stem
            output_dir = Config.EXTRACTIONS_DIR / f"{pdf_name}_extracted"
        
        text_dir = output_dir / "text"
        tables_dir = output_dir / "tables"
        images_dir = output_dir / "images"
        
        for directory in [text_dir, tables_dir, images_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        try:
            for page_num in range(len(doc)):
                page = doc[page_num]
                self._extract_text(page, page_num, text_dir)
                self._extract_tables(page, page_num, tables_dir)
                self._extract_images(doc, page, page_num, images_dir)
            
            self._extract_metadata(doc, text_dir)
            logger.info(f"✓ Extraction complete! Results saved in: {output_dir}")
            return output_dir
            
        except Exception as e:
            logger.error(f"Error during extraction: {e}")
            return None
        finally:
            if doc:
                doc.close()
                logger.info("PDF document closed")

    def _extract_text(self, page, page_num, text_dir):
        text = page.get_text()
        text_file = text_dir / f"page_{page_num + 1}_text.txt"
        with open(text_file, "w", encoding="utf-8") as f:
            f.write(text)
        
        text_sorted = page.get_text(sort=True)
        text_sorted_file = text_dir / f"page_{page_num + 1}_text_sorted.txt"
        with open(text_sorted_file, "w", encoding="utf-8") as f:
            f.write(text_sorted)
    
    def _extract_tables(self, page, page_num, tables_dir):
        try:
            tables = page.find_tables()
            if tables.tables:
                for table_num, table in enumerate(tables.tables):
                    table_data = table.extract()
                    if table_data:
                        csv_file = tables_dir / f"page_{page_num + 1}_table_{table_num + 1}.csv"
                        with open(csv_file, "w", newline="", encoding="utf-8") as f:
                            writer = csv.writer(f)
                            for row in table_data:
                                cleaned_row = [str(cell).strip() if cell is not None else "" for cell in row]
                                writer.writerow(cleaned_row)
            else:
                with open(tables_dir / f"page_{page_num + 1}_no_tables.txt", "w") as f:
                    f.write("No tables detected on this page.")
        except Exception as e:
            with open(tables_dir / f"page_{page_num + 1}_table_error.txt", "w") as f:
                f.write(f"Error extracting tables: {e}")
    
    def _extract_images(self, doc, page, page_num, images_dir):
        try:
            image_list = page.get_images()
            if image_list:
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    extracted_image = doc.extract_image(xref)
                    if extracted_image:
                        image_bytes = extracted_image["image"]
                        image_ext = extracted_image["ext"]
                        image_file = images_dir / f"page_{page_num + 1}_image_{img_index + 1}.{image_ext}"
                        with open(image_file, "wb") as f:
                            f.write(image_bytes)
            else:
                with open(images_dir / f"page_{page_num + 1}_no_images.txt", "w") as f:
                    f.write("No images detected on this page.")
        except Exception as e:
            with open(images_dir / f"page_{page_num + 1}_image_error.txt", "w") as f:
                f.write(f"Error extracting images: {e}")
    
    def _extract_metadata(self, doc, text_dir):
        metadata = doc.metadata
        metadata_file = text_dir / "metadata.txt"
        with open(metadata_file, "w", encoding="utf-8") as f:
            f.write("PDF Metadata:\n")
            f.write("=" * 50 + "\n")
            for key, value in metadata.items():
                f.write(f"{key}: {value}\n")
            f.write(f"\nDocument Properties:\n")
            f.write("=" * 50 + "\n")
            f.write(f"Total pages: {len(doc)}\n")
            f.write(f"PDF is encrypted: {doc.is_encrypted}\n")