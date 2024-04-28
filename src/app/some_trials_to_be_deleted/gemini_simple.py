import os
import pathlib

import google.generativeai as genai
from dotenv import load_dotenv

if __name__ == "__main__":
    """This script demonstrates how to use the Google GenAI API to generate content using the Gemini model."""
    # Traverse up two directories
    env_path = pathlib.Path(__file__).parents[2] / ".env"
    load_dotenv(dotenv_path=env_path)

    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
    response = model.generate_content("Please give me python code to sort a list.")
    print(response.text)
