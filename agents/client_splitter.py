import json
import re
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="deepseek-r1-distill-llama-70b", api_key=GROQ_API_KEY)

def extract_json_from_response(response_text):
    """Extract JSON block from mixed LLM output."""
    match = re.search(r"\[.*\]", response_text, re.DOTALL)
    return match.group(0) if match else None

def split_clients(resume_text: str) -> list:
    """
    Use LLM to split the resume into per-client experience blocks.

    Args:
        resume_text (str): Full resume text.

    Returns:
        list: List of client experience blocks with role, company, and experience_text.
    """
    prompt = f"""
You are a resume parser specialized in extracting professional experience.

👉 Your task is to extract **only full-time work experiences** under the "Work Experience" section.
❌ Do NOT extract:
- Projects
- Internships
- Education
- Certifications

✅ For each full-time job entry, extract:
- "role"
- "company"
- "experience_text" (include bullet points or summary lines)

Return your output in this **STRICT JSON format**:
[
  {{
    "role": "Data Scientist",
    "company": "ABC Corp",
    "experience_text": "• Developed models...\\n• Used Spark, SQL, and AWS..."
  }},
  ...
]

Here is the full resume:
{resume_text}
"""


    response = llm.invoke(prompt)
    response_text = response.content if hasattr(response, "content") else str(response)
    json_part = extract_json_from_response(response_text)

    if not json_part:
        return [{"error": "Invalid JSON returned from LLM"}]
    
    try:
        return json.loads(json_part)
    except json.JSONDecodeError as e:
        return [{"error": f"JSON decode failed: {str(e)}"}]

if __name__ == "__main__":
    print("✅ LLM Client Splitter Agent Ready")