import sys
from pathlib import Path

from dotenv import load_dotenv
from phi.agent import Agent
from phi.model.groq import Groq
from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools

# Add parent directory to path to allow imports from utils
sys.path.append(str(Path(__file__).parent.parent))

# Import logger after path is set
from utils.logger import get_logger

# Setup logger
logger = get_logger("ai_agent")

# Load environment variables
load_dotenv()
logger.info("Environment variables loaded")


def agent_team(model) -> list:
    try:
        logger.info("Initializing agent team")
        web_agent = Agent(
            name="Web Agent",
            model=model,
            tools=[DuckDuckGo()],
            instructions=["Always include sources"],
            show_tool_calls=True,
            markdown=True,
        )

        finance_agent = Agent(
            name="Finance Agent",
            role="Get financial data",
            model=model,
            tools=[
                YFinanceTools(
                    stock_price=True, analyst_recommendations=True, company_info=True
                )
            ],
            instructions=["Use tables to display data"],
            show_tool_calls=True,
            markdown=True,
        )
        # return [web_agent]
        return [web_agent, finance_agent]
    except Exception as e:
        logger.error(f"Failed to initialize agent team: {e}", exc_info=True)
        raise


def execute_groq_agent(query):
    """Initialize and return the Groq agent with YFinance tools."""
    try:
        logger.info("Initializing Groq model")
        groq_model = Groq(id="llama-3.3-70b-versatile")
        logger.debug("Groq model initialized successfully")
        team = agent_team(groq_model)
        logger.info("Creating Groq agent")
        agent = Agent(
            model=groq_model,
            team=team,
            instructions=["Always include sources", "Use tables to display data"],
            show_tool_calls=True,
            markdown=True,
        )
        logger.info("Groq agent setup complete")

        response = agent.print_response(query)

        return response
    except Exception as e:
        logger.error(f"Failed to initialize Groq agent: {e}", exc_info=True)
        raise


def execute_openai_agent(query):
    """Initialize and return the OpenAI agent."""
    try:
        logger.info("Initializing OpenAI model")
        openai_model = OpenAIChat(id="gpt-4o")
        logger.debug("OpenAI model initialized successfully")
        team = agent_team(openai_model)
        logger.info("Creating OpenAI agent")
        agent = Agent(
            model=openai_model,
            team=team,
            instructions=["Use tables to display data", "Always include sources"],
            # debug_mode=True,
            show_tool_calls=True,
            markdown=True,
        )
        logger.info("OpenAI agent setup complete")

        response = agent.print_response(query)

        return response
    except Exception as e:
        logger.error(f"Failed to initialize OpenAI agent: {e}", exc_info=True)
        raise


def main():
    """Main function to run the stock analysis."""
    try:
        logger.info("Starting stock analysis")
        stocks = "TSLA and NVIDIA"
        query = f"""Summarize analyst recommendations and share the latest news for companies with their current stock price: {stocks}"""
        logger.info(f"Query: {query}")
        # Initialize agents
        execute_groq_agent(query)
        # openai_agent_response = execute_openai_agent(query)

        logger.info("Stock analysis completed successfully")
        return 0
    except Exception as e:
        logger.critical(f"Fatal error in main: {e}", exc_info=True)
        return 1
    finally:
        logger.info("Application shutdown")


if __name__ == "__main__":
    try:
        logger.info("Application started")
        sys.exit(main())
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Unhandled exception: {e}", exc_info=True)
        sys.exit(1)
