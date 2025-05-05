import dspy
from dotenv import load_dotenv
import os

def get_dspy():
    """Initialize and configure DSPy with OpenAI GPT-4."""
    load_dotenv()
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    lm = dspy.LM('openai/gpt-4o-mini', api_key=OPENAI_API_KEY, cache=False)
    dspy.configure(lm=lm)
    dspy.settings.configure(track_usage=True)
    
    return dspy, lm
