import os
import sys
from dotenv import load_dotenv

# Load variables from .env file (local dev); on Streamlit Cloud, secrets are injected directly
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
DB_NAME = os.getenv("DB_NAME", "review_history.db")

# Safety gate: halt execution if the API key is missing
if not GROQ_API_KEY:
    print("❌ Configuration Error: GROQ_API_KEY is missing!")
    print("Please add your key to a .env file locally or to Streamlit's Secrets panel on the cloud.")
    sys.exit(1)
