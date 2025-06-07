import os
from datetime import datetime
from utils.logger import get_logger

logger = get_logger("save_response")

def save_response_to_file(response, agent_name, stocks):
    """
    Save the model response to a timestamped file.
    
    Args:
        response: The response content to save
        agent_name: Name of the agent that generated the response
        stocks: Stock symbols that were analyzed
    """
    try:
        # Create responses directory if it doesn't exist
        os.makedirs('responses', exist_ok=True)
        
        # Generate filename with timestamp and agent name
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_stocks = ''.join(c if c.isalnum() else '_' for c in stocks)
        filename = f"responses/{timestamp}_{agent_name}_{safe_stocks[:50]}.txt"
        
        # Write the response to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Agent: {agent_name}\n")
            f.write(f"Stocks: {stocks}\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            f.write("-" * 80 + "\n")
            f.write(str(response))
            
        logger.info(f"Response saved to {filename}")
        return filename
    except Exception as e:
        logger.error(f"Error saving response to file: {e}")
        return None
