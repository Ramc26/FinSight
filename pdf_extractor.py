import pymupdf
import os
import csv
import logging
from pathlib import Path
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFExtractor:
    """Handles PDF extraction including password-protected files"""
    
    def __init__(self):
        logger.info("Initializing PDFExtractor")
        self.extraction_count = 0
        logger.info("PDFExtractor initialized successfully")
    
    def unlock_pdf(self, pdf_path):
        """Handle password-protected PDF files"""
        logger.info(f"Attempting to unlock PDF: {pdf_path}")
        try:
            doc = pymupdf.open(pdf_path)
            
            if doc.needs_pass:
                logger.info(f"PDF '{os.path.basename(pdf_path)}' is password protected")
                print(f"\nThe PDF '{os.path.basename(pdf_path)}' is password protected.")
                attempts = 0
                
                while attempts < Config.MAX_PASSWORD_ATTEMPTS:
                    password = input("Please enter the password: ")
                    if doc.authenticate(password):
                        logger.info("PDF unlocked successfully")
                        print("✓ PDF unlocked successfully!")
                        return doc
                    else:
                        attempts += 1
                        remaining = Config.MAX_PASSWORD_ATTEMPTS - attempts
                        logger.warning(f"Incorrect password, {remaining} attempts remaining")
                        if remaining > 0:
                            print(f"✗ Incorrect password. {remaining} attempts remaining.")
                        else:
                            logger.error("Maximum password attempts exceeded")
                            print("✗ Maximum password attempts exceeded.")
                            doc.close()
                            return None
            else:
                logger.info("PDF is not password protected")
            return doc
        except Exception as e:
            logger.error(f"Error opening PDF: {e}")
            print(f"Error opening PDF: {e}")
            return None
    
    def extract_pdf_content(self, pdf_path, output_dir=None):
        """Main extraction method"""
        logger.info(f"Starting PDF content extraction: {pdf_path}")
        
        if output_dir is None:
            pdf_name = Path(pdf_path).stem
            output_dir = Config.EXTRACTIONS_DIR / f"{pdf_name}_extracted"
        
        logger.info(f"Output directory: {output_dir}")
        
        # Create output directories
        text_dir = output_dir / "text"
        tables_dir = output_dir / "tables"
        images_dir = output_dir / "images"
        
        logger.info("Creating output directories")
        for directory in [text_dir, tables_dir, images_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        # Handle password protection
        doc = self.unlock_pdf(pdf_path)
        if doc is None:
            logger.error("Failed to unlock PDF")
            return False
        
        logger.info(f"Processing PDF with {len(doc)} pages")
        print(f"Processing PDF with {len(doc)} pages...")
        
        try:
            for page_num in range(len(doc)):
                page = doc[page_num]
                logger.info(f"Extracting content from page {page_num + 1}")
                print(f"Extracting content from page {page_num + 1}")
                
                self._extract_text(page, page_num, text_dir)
                self._extract_tables(page, page_num, tables_dir)
                self._extract_images(doc, page, page_num, images_dir)
            
            self._extract_metadata(doc, text_dir)
            logger.info(f"PDF extraction completed successfully: {output_dir}")
            print(f"✓ Extraction complete! Results saved in: {output_dir}")
            return True
            
        except Exception as e:
            logger.error(f"Error during extraction: {e}")
            print(f"Error during extraction: {e}")
            return False
        finally:
            doc.close()
            logger.info("PDF document closed")
    
    def _extract_text(self, page, page_num, text_dir):
        """Extract text content"""
        logger.debug(f"Extracting text from page {page_num + 1}")
        
        # Raw text
        text = page.get_text()
        text_file = text_dir / f"page_{page_num + 1}_text.txt"
        with open(text_file, "w", encoding="utf-8") as f:
            f.write(text)
        logger.debug(f"Saved raw text to: {text_file}")
        
        # Sorted text
        text_sorted = page.get_text(sort=True)
        text_sorted_file = text_dir / f"page_{page_num + 1}_text_sorted.txt"
        with open(text_sorted_file, "w", encoding="utf-8") as f:
            f.write(text_sorted)
        logger.debug(f"Saved sorted text to: {text_sorted_file}")
    
    def _extract_tables(self, page, page_num, tables_dir):
        """Extract tables as CSV"""
        logger.debug(f"Extracting tables from page {page_num + 1}")
        try:
            tables = page.find_tables()
            
            if tables.tables:
                logger.debug(f"Found {len(tables.tables)} tables on page {page_num + 1}")
                for table_num, table in enumerate(tables.tables):
                    table_data = table.extract()
                    
                    if table_data:
                        csv_file = tables_dir / f"page_{page_num + 1}_table_{table_num + 1}.csv"
                        with open(csv_file, "w", newline="", encoding="utf-8") as f:
                            writer = csv.writer(f)
                            for row in table_data:
                                cleaned_row = [str(cell).strip() if cell is not None else "" for cell in row]
                                writer.writerow(cleaned_row)
                        logger.debug(f"Saved table {table_num + 1} to: {csv_file}")
            else:
                logger.debug(f"No tables found on page {page_num + 1}")
                no_tables_file = tables_dir / f"page_{page_num + 1}_no_tables.txt"
                with open(no_tables_file, "w") as f:
                    f.write("No tables detected on this page.")
                    
        except Exception as e:
            logger.error(f"Error extracting tables from page {page_num + 1}: {e}")
            error_file = tables_dir / f"page_{page_num + 1}_table_error.txt"
            with open(error_file, "w") as f:
                f.write(f"Error extracting tables: {e}")
    
    def _extract_images(self, doc, page, page_num, images_dir):
        """Extract images"""
        logger.debug(f"Extracting images from page {page_num + 1}")
        try:
            image_list = page.get_images()
            
            if image_list:
                logger.debug(f"Found {len(image_list)} images on page {page_num + 1}")
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    extracted_image = doc.extract_image(xref)
                    
                    if extracted_image:
                        image_bytes = extracted_image["image"]
                        image_ext = extracted_image["ext"]
                        
                        image_file = images_dir / f"page_{page_num + 1}_image_{img_index + 1}.{image_ext}"
                        with open(image_file, "wb") as f:
                            f.write(image_bytes)
                        logger.debug(f"Saved image {img_index + 1} to: {image_file}")
            else:
                logger.debug(f"No images found on page {page_num + 1}")
                no_images_file = images_dir / f"page_{page_num + 1}_no_images.txt"
                with open(no_images_file, "w") as f:
                    f.write("No images detected on this page.")
                    
        except Exception as e:
            logger.error(f"Error extracting images from page {page_num + 1}: {e}")
            error_file = images_dir / f"page_{page_num + 1}_image_error.txt"
            with open(error_file, "w") as f:
                f.write(f"Error extracting images: {e}")
    
    def _extract_metadata(self, doc, text_dir):
        """Extract PDF metadata"""
        logger.info("Extracting PDF metadata")
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
        
        logger.info(f"Metadata saved to: {metadata_file}")