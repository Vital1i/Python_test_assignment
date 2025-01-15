import os
import random
import time

# Define LLM configuration
gpt4_config = {
    "cache_seed": int(time.time()) + random.randint(1, 1000),  # Change the cache_seed for different trials
    "temperature": 0.7,
    "config_list": [
        {"model": "gpt-3.5-turbo", "api_key": os.environ.get("OPENAI_API_KEY")}
    ],
    "timeout": 120,
}
