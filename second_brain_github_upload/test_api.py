import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

try:
    print("Testing gemini-1.5-flash...")
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Hello")
    print("1.5-flash success:", response.text[:20])
except Exception as e:
    print("1.5-flash error:", e)

try:
    print("\nTesting gemini-flash-latest...")
    model = genai.GenerativeModel('gemini-flash-latest')
    response = model.generate_content("Hello")
    print("flash-latest success:", response.text[:20])
except Exception as e:
    print("flash-latest error:", e)
