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
from utils.prompt_loader import load_markdown_sections

# Setup logger
logger = get_logger("two_agents")

# Load environment variables
load_dotenv()
logger.info("Environment variables loaded")

#Stock to analyze
stocks = "TSLA and NVIDIA"


def agent_team(model, prompts) -> list:
    try:
        logger.info("Initializing agent team")
        web_agent = Agent(
            name="Web Agent",
            model=model,
            tools=[DuckDuckGo()],
            instructions=prompts["web_agent_instructions"].splitlines(),
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
            instructions=prompts["finance_agent_instructions"].splitlines(),
            show_tool_calls=True,
            markdown=True,
        )
        # return [web_agent]
        return [web_agent, finance_agent]
    except Exception as e:
        logger.error(f"Failed to initialize agent team: {e}", exc_info=True)
        raise


def execute_agent(prompts, agent_type="groq"):
    """
    Initializes and executes a financial analysis agent.

    Args:
        query (str): The query for the agent to execute.
        agent_type (str): The type of agent to use ('groq' or 'openai').

    Returns:
        The response from the agent.
    """
    try:
        logger.info("Initializing %s model", agent_type)
        if agent_type == "groq":
            model = Groq(id="llama-3.3-70b-versatile")
        elif agent_type == "openai":
            model = OpenAIChat(id="gpt-4o")
        else:
            raise ValueError(f"Unsupported agent type: {agent_type}")

        logger.debug("%s model initialized successfully", agent_type)

        team = agent_team(model, prompts)

        logger.info("Creating %s agent", agent_type)
        agent = Agent(
            model=model,
            team=team,
            show_tool_calls=True,
            markdown=True,
        )
        logger.info("%s agent setup complete", agent_type)
        query = prompts["query"].format(stocks=prompts["stocks"])
        response = agent.print_response(query)
        return response
    except Exception as e:
        logger.error("Failed to execute %s agent: %s", agent_type, e, exc_info=True)
        raise


def main():
    """Main function to run the stock analysis."""
    try:
        PROMPTS_FILE = Path(__file__).parent.parent / "prompts" / "instructions.md"
        prompts = load_markdown_sections(str(PROMPTS_FILE))
        query = prompts["query"]
        logger.info("Query: %s", query)
        logger.info("Starting stock analysis")

        # # Run analysis with Groq agent
        # logger.info("--- Running Groq Agent ---")
        # execute_agent(prompts, agent_type="groq")
        
        # Run analysis with OpenAI agent
        logger.info("--- Running OpenAI Agent ---")
        execute_agent(prompts, agent_type="openai")

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
        logger.critical(f"Unhandled exception: {e}", exc_info=True)
        sys.exit(1)
