import sys
from pathlib import Path

from dotenv import load_dotenv
from phi.agent import Agent
from phi.model.groq import Groq
from phi.model.openai import OpenAIChat
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


#Stock to analyze
stocks = "TSLA and NVIDIA"

def setup_groq_agent(tools):
    """Initialize and return the Groq agent with YFinance tools."""
    try:
        logger.info("Initializing Groq model")
        groq_model = Groq(id="llama-3.3-70b-versatile")
        logger.debug("Groq model initialized successfully")

        logger.info("Creating Groq agent")
        agent = Agent(
            model=groq_model,
            tools=tools,
            instructions=["Always include sources", "Use tables to display data"],
            show_tool_calls=True,
            markdown=True,
        )
        logger.info("Groq agent setup complete")
        return agent
    except Exception as e:
        logger.error(f"Failed to initialize Groq agent: {e}", exc_info=True)
        raise


def setup_openai_agent(tools):
    """Initialize and return the OpenAI agent."""
    try:
        logger.info("Initializing OpenAI model")
        openai_model = OpenAIChat(id="gpt-4o")
        logger.debug("OpenAI model initialized successfully")

        logger.info("Creating OpenAI agent")
        agent = Agent(
            model=openai_model,
            tools=tools,
            instructions=["Use tables to display data"],
            # debug_mode=True,s
            show_tool_calls=True,
            markdown=True,
        )
        logger.info("OpenAI agent setup complete")
        return agent
    except Exception as e:
        logger.error(f"Failed to initialize OpenAI agent: {e}", exc_info=True)
        raise


def analyze_stocks(agent, stocks, agent_name="Agent"):
    """
    Analyze stocks using the specified agent, log the response, and save to file.

    Args:
        agent: The agent to use for analysis
        stocks (str): Comma-separated stock symbols to analyze
        agent_name (str): Name of the agent for logging purposes

    Returns:
        tuple: (response, filename) where filename is the path to the saved response
    """
    try:
        logger.info(f"{agent_name} analyzing stocks: {stocks}")
        query = f"""Summarize and compare the analyst recommendation and 
                 fundamentals of the following stocks with their current stock price: {stocks}"""

        logger.debug(f"{agent_name} query: {query}")

        # Capture the response
        response = agent.print_response(query)

        # Log the response summary
        logger.info(f"{agent_name} analysis complete")

        return response

    except Exception as e:
        logger.error(f"Error in {agent_name} stock analysis: {e}", exc_info=True)
        raise


def main():
    """Main function to run the stock analysis."""
    try:
        logger.info("Starting stock analysis")

        logger.info("Setting up YFinance tools")
        tools = [
            YFinanceTools(
                stock_price=True,
                analyst_recommendations=True,
                company_info=True,
                company_news=True,
            )
        ]
        # Initialize agents
        groq_agent = setup_groq_agent(tools)
        openai_agent = setup_openai_agent(tools)

        # Run analysis with both agents
        logger.info("Running Groq agent analysis")
        analyze_stocks(groq_agent, stocks, "Groq")

        logger.info("Running OpenAI agent analysis")
        analyze_stocks(openai_agent, stocks, "OpenAI")

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
