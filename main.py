import sys
from pathlib import Path
from crewai import Crew

from config import Config
from pdf_extractor import PDFExtractor
from data_loader import FinancialDataLoader
from agent import DocumentAgents
from tasks import DocumentTasks
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FinSight:
    def __init__(self):
        self.pdf_extractor = PDFExtractor()
        self.data_loader = None

    def extract_pdf(self, pdf_path, password=None):
        """Extract content from PDF, passing an optional password."""
        logger.info(f"Starting PDF extraction: {pdf_path}")
        print(f"Starting PDF extraction: {pdf_path}")
        extraction_path = self.pdf_extractor.extract_pdf_content(pdf_path, password=password)
        
        if extraction_path:
            logger.info(f"PDF extraction successful, setting up data loader for: {extraction_path}")
            self.data_loader = FinancialDataLoader(extraction_path)
            return extraction_path
        else:
            logger.error(f"PDF extraction failed for: {pdf_path}")
            return None

    def get_full_text_content(self):
        if not self.data_loader:
            return ""
        text_data = self.data_loader.load_text_data()
        return "\n\n".join(text_data.values())

    def analyze_document(self, extraction_path):
        print("Starting comprehensive document analysis...")
        
        full_content = self.get_full_text_content()
        if not full_content:
            return "Could not read content from the extracted files."

        tasks_manager = DocumentTasks(str(extraction_path))
        
        context_task = tasks_manager.create_contextualization_task(full_content)
        extraction_task = tasks_manager.create_data_extraction_task(context_task)
        report_task = tasks_manager.create_reporting_task(extraction_task)
        
        document_crew = Crew(
            agents=list(DocumentAgents.create_all_agents().values()),
            tasks=[context_task, extraction_task, report_task],
            verbose=True
        )
        
        result = document_crew.kickoff()
        return result

    def ask_question(self, question, extraction_path):
        if self.data_loader is None:
            self.data_loader = FinancialDataLoader(extraction_path)
        
        full_content = self.get_full_text_content()
        if not full_content:
            return "Could not read content to answer the question."

        tasks_manager = DocumentTasks(str(extraction_path))
        question_task = tasks_manager.create_specific_question_task(question, full_content)
        
        qa_crew = Crew(
            agents=[DocumentAgents.create_reporting_agent()],
            tasks=[question_task],
            verbose=True
        )
        
        return qa_crew.kickoff()

    def run_interactive(self):
        print("🤖 Welcome to FinSight - Your AI Document Assistant!")
        print("=" * 50)
        
        while True:
            pdf_path = input("\nEnter path to a PDF file (or type 'exit' to quit): ").strip()
            
            if pdf_path.lower() == 'exit':
                break

            if not Path(pdf_path).exists():
                print("Error: PDF file not found! Please try again.")
                continue
            
            extraction_path = self.extract_pdf(pdf_path)
            if not extraction_path:
                print("PDF extraction failed! Please try again.")
                continue
            
            print(f"✓ PDF extracted to: {extraction_path}")
            
            while True:
                print("\nOptions for the current document:")
                print("1. Run comprehensive analysis")
                print("2. Ask a specific question")
                print("3. Process another document")
                print("4. Exit")
                
                choice = input("\nChoose an option (1-4): ").strip()
                
                if choice == "1":
                    result = self.analyze_document(extraction_path)
                    print("\n" + "="*50)
                    print("DOCUMENT ANALYSIS RESULTS:")
                    print("="*50)
                    print(result)
                    
                elif choice == "2":
                    question = input("\nEnter your question: ").strip()
                    answer = self.ask_question(question, extraction_path)
                    print("\n" + "="*50)
                    print("ANSWER:")
                    print("="*50)
                    print(answer)
                    
                elif choice == "3":
                    break
                
                elif choice == "4":
                    print("Thank you for using FinSight! 👋")
                    return
                
                else:
                    print("Invalid choice. Please try again.")

        print("Thank you for using FinSight! 👋")

def main():
    finsight = FinSight()
    
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        extraction_path = finsight.extract_pdf(pdf_path)
        
        if extraction_path and len(sys.argv) > 2:
            question = " ".join(sys.argv[2:])
            answer = finsight.ask_question(question, extraction_path)
            print(answer)
        elif extraction_path:
            result = finsight.analyze_document(extraction_path)
            print(result)
    else:
        finsight.run_interactive()

if __name__ == "__main__":
    main()