import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-flash-latest')

for i in range(5):
    try:
        response = model.generate_content(f"Hello {i}")
        print(f"Request {i} success")
    except Exception as e:
        print(f"Request {i} error:", e)
