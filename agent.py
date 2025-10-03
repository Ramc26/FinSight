from crewai import Agent
from config import Config

class DocumentAgents:
    @staticmethod
    def create_context_agent():
        return Agent(
            role="Document Contextualizer",
            goal="Accurately identify the type and primary subject of a document from its raw text content.",
            backstory="""You are an expert in document analysis. Your strength lies in quickly reading through unstructured text 
            to classify documents. You can instantly recognize invoices, receipts, tickets, financial statements, or legal agreements
            and provide a concise summary of the document's core purpose and key entities.""",
            verbose=Config.AGENT_VERBOSE,
            allow_delegation=False
        )

    @staticmethod
    def create_data_analyst_agent():
        return Agent(
            role="Data Extraction Specialist",
            goal="Extract specific, structured information from a document based on its identified context.",
            backstory="""You are a meticulous data analyst. Once you know what a document is about, you excel at
            extracting all relevant details in a clean, structured format. For a ticket, you'd find names, dates, and locations.
            For an invoice, you'd find line items, totals, and due dates.""",
            verbose=Config.AGENT_VERBOSE,
            allow_delegation=False
        )

    @staticmethod
    def create_reporting_agent():
        return Agent(
            role="Information Reporting Specialist",
            goal="Synthesize extracted data into a clear, comprehensive report and answer user questions.",
            backstory="""You are a master communicator who transforms raw data into understandable insights.
            You can generate final reports, summaries, or answer specific user questions based on the structured
            information provided to you, ensuring the output is always clear and directly addresses the user's needs.""",
            verbose=Config.AGENT_VERBOSE,
            allow_delegation=True
        )

    @staticmethod
    def create_all_agents():
        return {
            'context_agent': DocumentAgents.create_context_agent(),
            'analyst_agent': DocumentAgents.create_data_analyst_agent(),
            'reporting_agent': DocumentAgents.create_reporting_agent()
        }