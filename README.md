# Finance AI Agent Project (WIP- Work in progress)
## Project Overview
This project is a great example of an LLM-powered agentic system in a specific domain (finance).
A multi-agent AI system integrating open-source and OpenAI LLMs to analyze financial data, aggregate news, and deliver actionable insights using APIs like YFinance and DuckDuckGo.

A Python-based project that compares AI agents from different providers (Groq and OpenAI) for financial analysis tasks. The project has been refactored to be configuration-driven, using a central markdown file to manage prompts, instructions, and target stocks. It includes two main scripts: one for single-agent analysis and another for multi-agent team collaboration.

### Key Features:
- Multi-agent setup – distinct components for financial analysis and web search.
- Tool use – fetches external data (e.g., stock prices, news) using YFinance and DuckDuckGo APIs.
- Reasoning & decision-making – uses LLMs to interpret and combine data signals.
- **Configuration-Driven**: All prompts, instructions, and target stocks are managed in a central `prompts/instructions.md` file, allowing for easy customization without code changes.

### Is it an AI Agent?

Yes. Each part (e.g., fetching stock data, summarizing news, generating insights) acts like an AI agent—a function with a clear task.

### Is it Agentic AI?

Partially, yes. Here's why:

| Agentic Trait        | Present in Repo? | Notes |
|----------------------|------------------|-------|
| Tool integration     | ✅ Yes           | Uses YFinance, news APIs |
| Reasoning           | ✅ Yes           | LLM used to interpret and combine signals |
| Planning            | 🟡 Partial       | Logic is based on provided prompts; no dynamic task chaining |
| Memory/State        | ❌ No            | Stateless (no long-term memory of past runs) |
| Delegation/Subagents| ✅ Yes           | The `two_agents.py` script delegates tasks to a Finance Agent and a Web Agent. |
| Autonomy            | ❌ No            | Needs user to trigger execution (not persistent or self-initiating) |

Finance AI Agent is a strong example of a modular, task-focused AI agent system with some agentic traits. It doesn't yet reach full Agentic AI status (e.g., self-planning, persistent memory, dynamic agent coordination), but it's a practical and well-scoped implementation of agent-based thinking applied to real-world data.


## Theory
In this theory section, we'll explore the common patterns for agentic systems. We'll start with our foundational building block—the augmented LLM—and progressively increase complexity, from simple compositional workflows to  autonomous agents.

![Augmented LLM Architecture](src/utils/images/augumented_LLM.png)

*Image source: [Anthropic - Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)*

### Building block: The augmented LLM

The basic building block of agentic systems is an LLM enhanced with augmentations such as retrieval, tools, and memory. Our current models can actively use the augmentation of using the tools and determining what information to retain. Further, these tools act as a independent agents and can work in parallel to each other to retrieve information and provide a response.

In this project, the usage of single agent and multi-agent team is compared. In the single agent case, the agent is using the Yahoo Finance tools to retrieve information from the Yahoo Finance API. In the multi-agent case, one agent uses Yahoo Finance tools while another agent uses DuckDuckGo for the latest web information.


![Multi Agent Architecture](src/utils/images/agent_call_image.png)

As together, we make this as LLM enhanced agentic method to retrieve information from the Yahoo Finance API and provide a response of the latest web information about the stock provided by the user. But this is not the end of the story. As said in this block post [Anthropic - Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)*, we can make this as a autonomous agent to retrieve information from the Yahoo Finance API and provide a response of the latest web information about the stock provided by the user and connecting to the appropriate stock broker to place the order when the certain conditions are met. This make a complete autonomous agent for the stock information and trading but there should be a human in the loop to watch this process as it's still in the developemnt phase.
## Project Structure

```
ai_agent/
├── .env                    # Environment variables (not in version control)
├── .gitignore
├── pyproject.toml          # Project dependencies and configuration
├── Makefile               # Make commands for common tasks
├── README.md              # Project documentation
├── src/
│   ├── ai_agent/
│   │   ├── __init__.py
│   │   ├── single_agent.py     # Single agent implementation
│   │   └── two_agents.py       # Multi-agent team implementation
│   ├── prompts/
│   │   └── instructions.md # Central configuration for prompts and stocks
│   └── utils/
│       ├── __init__.py
│       ├── logger.py       # Logging configuration
│       └── prompt_loader.py # Utility to load prompts from markdown
└──tests/                 # Unit and integration tests
```

## Setup Instructions

### Prerequisites

- Python 3.10+
- API keys for:
  - Groq
  - OpenAI
- Make sure you have the required dependencies installed by running `make install`

### Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# Required API Keys
OPENAI_API_KEY=your_openai_api_key_here
GROQ_API_KEY=your_groq_api_key_here

# Optional: Logging configuration
LOG_LEVEL=INFO
LOG_FILE=ai_agent.log
```

### Configuration File

All runtime behavior is controlled by `src/prompts/instructions.md`. This file uses markdown headers to define different configuration sections.

- `# stocks`: The company tickers to analyze.
- `# instructions`: The system prompt/instructions for the AI agent.
- `# query`: The main user query template. Use `{stocks}` as a placeholder.

## Available Scripts

### Single Agent Analysis (`single_agent.py`)

A simple implementation that uses either Groq or OpenAI's model to analyze stocks.

**Features:**
- Single AI agent implementation
- Supports both Groq and OpenAI models
- Basic financial analysis using yfinance
- Response logging and saving
A simple implementation that uses a single agent (either Groq or OpenAI) to analyze stocks based on the configuration in `instructions.md`.
**Usage:**
```bash
python src/ai_agent/single_agent.py
```

### Multi-Agent Team (`two_agents.py`)

Implements a team of specialized agents working together:
1. **Web Agent**: Handles web searches using DuckDuckGo
2. **Finance Agent**: Handles financial data using yfinance

**Features:**
- Multiple specialized agents working in parallel
- Collaborative problem solving
- Integrated web search and financial analysis
- Response logging and saving
A simple implementation that uses a two agent (either Groq or OpenAI) to analyze stocks based on the configuration in `instructions.md`.
**Usage:**
```bash
python src/ai_agent/two_agents.py
```

## API Key Management

### Obtaining API Keys

1. **OpenAI API Key**:
   - Visit: https://platform.openai.com/api-keys
   - Create a new secret key
   - Add it to your `.env` file as `OPENAI_API_KEY`

2. **Groq API Key**:
   - Visit: https://console.groq.com/keys
   - Create a new API key
   - Add it to your `.env` file as `GROQ_API_KEY`

### Rate Limits

- **OpenAI**: Varies by account tier
- **Groq**: 
  - Free tier: 100,000 tokens/day
  - Monitor usage at: https://console.groq.com/usage

## Development

### Setting Up Development Environment

1.  Create and activate a virtual environment and install dependencies:
    ```bash
    make install
    ```

### Customizing the Analysis

To change the stocks, prompts, or queries, **edit the `src/prompts/instructions.md` file**. You no longer need to modify the Python scripts.

### Running the Agents

1.  Run the single agent script:
    ```bash
    make single_agent
    ```

3. Run the multi-agent script:
   ```bash
   make two_agents
   ```
To know the further information about the executuon check the Makefile
If you need to customize the stocks to analyze, you can change the stocks variable in the single_agent.py and two_agents.py files at the top.


## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Comparsion of the free open source available LLM model and OPENAI's paid LLM model for the ai agentic development