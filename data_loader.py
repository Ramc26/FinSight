import pandas as pd
import logging
from pathlib import Path
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FinancialDataLoader:
    """Handles loading and preprocessing of extracted PDF data"""
    
    def __init__(self, extraction_path):
        logger.info(f"Initializing FinancialDataLoader with path: {extraction_path}")
        self.base_path = Path(extraction_path)
        self.loaded_data = {}
        logger.info("FinancialDataLoader initialized successfully")
    
    def load_all_data(self):
        """Load all extracted data"""
        logger.info("Loading all extracted data")
        self.loaded_data = {
            'text': self.load_text_data(),
            'tables': self.load_table_data(),
            'metadata': self.get_metadata()
        }
        logger.info(f"Successfully loaded {len(self.loaded_data['text'])} text files and {len(self.loaded_data['tables'])} table files")
        return self.loaded_data
    
    def load_text_data(self):
        """Load all extracted text data"""
        logger.info("Loading text data from extracted files")
        text_data = {}
        text_dir = self.base_path / "text"
        
        if text_dir.exists():
            logger.info(f"Found text directory: {text_dir}")
            for text_file in text_dir.glob("*.txt"):
                try:
                    with open(text_file, 'r', encoding='utf-8') as f:
                        text_data[text_file.name] = f.read()
                    logger.debug(f"Loaded text file: {text_file.name}")
                except Exception as e:
                    logger.error(f"Error reading {text_file}: {e}")
                    print(f"Error reading {text_file}: {e}")
        else:
            logger.warning(f"Text directory not found: {text_dir}")
        
        logger.info(f"Loaded {len(text_data)} text files")
        return text_data
    
    def load_table_data(self):
        """Load all CSV table data"""
        logger.info("Loading table data from CSV files")
        table_data = {}
        tables_dir = self.base_path / "tables"
        
        if tables_dir.exists():
            logger.info(f"Found tables directory: {tables_dir}")
            for csv_file in tables_dir.glob("*.csv"):
                try:
                    df = pd.read_csv(csv_file)
                    table_data[csv_file.name] = {
                        'dataframe': df,
                        'summary': {
                            'rows': len(df),
                            'columns': list(df.columns),
                            'sample': df.head().to_dict()
                        }
                    }
                    logger.debug(f"Loaded table file: {csv_file.name} with {len(df)} rows")
                except Exception as e:
                    logger.error(f"Error loading {csv_file}: {e}")
                    print(f"Error loading {csv_file}: {e}")
        else:
            logger.warning(f"Tables directory not found: {tables_dir}")
        
        logger.info(f"Loaded {len(table_data)} table files")
        return table_data
    
    def get_metadata(self):
        """Extract document metadata"""
        logger.info("Loading document metadata")
        metadata_file = self.base_path / "text" / "metadata.txt"
        if metadata_file.exists():
            logger.info(f"Found metadata file: {metadata_file}")
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = f.read()
            logger.info("Metadata loaded successfully")
            return metadata
        else:
            logger.warning("No metadata file found")
            return "No metadata available"
    
    def get_data_summary(self):
        """Get summary of loaded data"""
        logger.info("Generating data summary")
        if not self.loaded_data:
            logger.info("No data loaded yet, loading all data first")
            self.load_all_data()
        
        summary = {
            'text_files': len(self.loaded_data['text']),
            'table_files': len(self.loaded_data['tables']),
            'text_samples': list(self.loaded_data['text'].keys())[:3],
            'table_samples': list(self.loaded_data['tables'].keys())[:3]
        }
        
        logger.info(f"Data summary: {summary['text_files']} text files, {summary['table_files']} table files")
        return summary