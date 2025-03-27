import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    raise ValueError("DeepSeek API key is not set in environment variables.")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

# Define the chat completion request
response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

# Print the response
print(response.choices[0].message.content)