from crewai import Task
from agent import DocumentAgents

class DocumentTasks:
    def __init__(self, extraction_path):
        self.extraction_path = extraction_path
        self.agents = DocumentAgents.create_all_agents()

    def create_contextualization_task(self, document_content):
        return Task(
            description=f"""
            Analyze the following document content to determine its type and purpose.
            Identify key entities and provide a brief, high-level summary. Do not extract all details yet, just identify the document.

            Document Content:
            -----------------
            {document_content}
            """,
            agent=self.agents['context_agent'],
            expected_output="A concise summary identifying the document type (e.g., 'Train Ticket', 'Invoice', 'Bank Statement') and its main subject."
        )

    def create_data_extraction_task(self, context_task):
        return Task(
            description="""
            Based on the initial document context, perform a detailed extraction of all relevant information.
            Organize the extracted data into a clear, structured format. For example, if it's a ticket, extract passenger details,
            journey information, PNR, train number, dates, and times. If it's an invoice, extract vendor, client, line items, and totals.
            """,
            agent=self.agents['analyst_agent'],
            expected_output="A structured, itemized list of all key data points extracted from the document.",
            context=[context_task]
        )

    def create_reporting_task(self, extraction_task):
        return Task(
            description="""
            Synthesize the extracted data into a comprehensive and user-friendly report.
            The final report should be well-structured, easy to read, and summarize all the important findings from the document.
            """,
            agent=self.agents['reporting_agent'],
            expected_output="A clean, final report summarizing the document's content based on the extracted data.",
            context=[extraction_task]
        )

    def create_specific_question_task(self, question, document_content):
        return Task(
            description=f"""
            Answer the user's specific question based on the provided document content.

            User Question: {question}
            
            Full Document Content:
            ----------------------
            {document_content}

            Provide a direct and accurate answer based only on the information in the document content.
            """,
            agent=self.agents['reporting_agent'],
            expected_output="A direct, accurate answer to the user's question, citing information from the document."
        )