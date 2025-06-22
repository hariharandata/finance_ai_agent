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
from utils.prompt_loader import load_markdown_sections

# Setup logger
logger = get_logger("ai_agent")

# Load environment variables
load_dotenv()
logger.info("Environment variables loaded")



def setup_and_analyze_stocks(stocks, instructions, query, agent_type="groq"):
    """
    Setup agent and analyze stocks in one function call.
    
    Args:
        agent_type (str): Type of agent to use ("groq" or "openai")
        stocks (str): Comma-separated stock symbols to analyze
    
    Returns:
        The analysis response from the agent
    """
    try:
        logger.info("Setting up YFinance tools")
        tools = [
            YFinanceTools(
                stock_price=True,
                analyst_recommendations=True,
                company_info=True,
                company_news=False,
            )
        ]
        # Setup agent based on type
        if agent_type.lower() == "groq":
            logger.info("Initializing Groq model")
            groq_model = Groq(id="llama-3.3-70b-versatile")
            agent = Agent(
                model=groq_model,
                tools=tools,
                instructions=instructions.splitlines(),
                markdown=True,
            )
            agent_name = "Groq"
        elif agent_type.lower() == "openai":
            logger.info("Initializing OpenAI model")
            openai_model = OpenAIChat(id="gpt-4o")
            agent = Agent(
                model=openai_model,
                tools=tools,
                instructions=instructions.splitlines(),
                markdown=True,
            )
            agent_name = "OpenAI"
        else:
            raise ValueError(f"Unsupported agent type: {agent_type}")
        
        logger.info("%s agent setup complete", agent_name)

        # Analyze stocks
        logger.info("%s analyzing stocks: %s", agent_name, stocks)
        query = query.format(stocks=stocks)

        response = agent.print_response(query)
        logger.info("%s analysis complete", agent_name)
        return response
    except Exception as e:
        logger.error("Error in stock analysis: %s", e, exc_info=True)
        raise


def main():
    """Main function to run the stock analysis."""
    try:
        # Load prompts from markdown file
        PROMPTS_FILE = Path(__file__).parent.parent / "prompts" / "instructions.md"
        prompts = load_markdown_sections(str(PROMPTS_FILE))
        stocks = prompts["stocks"]
        instructions = prompts["instructions"]
        query = prompts["query"]

        logger.info("Starting stock analysis")
        
        # Run analysis with Groq agent
        logger.info("Running Groq agent analysis")
        setup_and_analyze_stocks(stocks, instructions, query, agent_type="groq")
        
        # Run analysis with OpenAI agent
        logger.info("Running OpenAI agent analysis")
        setup_and_analyze_stocks(stocks, instructions, query, agent_type="openai")
        
        logger.info("Stock analysis completed successfully")
        return 0
    except Exception as e:
        logger.critical("Fatal error in main: %s", e, exc_info=True)
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
        logger.critical("Unhandled exception: %s", e, exc_info=True)
        sys.exit(1)
