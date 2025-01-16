import os
import random
import time
from dotenv import load_dotenv

load_dotenv()

# Define LLM configuration
gpt4_config = {
    # Change the cache_seed for different trials
    "cache_seed": int(time.time()) + random.randint(1, 1000),
    "temperature": 0.7,
    "config_list": [
        {"model": "gpt-3.5-turbo", "api_key": os.environ.get("OPENAI_API_KEY")}
    ],
    "timeout": 120,
}
