from langchain.tools import Tool
from langchain_groq import ChatGroq

import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="deepseek-r1-distill-llama-70b",api_key=GROQ_API_KEY)
def extract_job_data(jd_text):
    """
    Extracts key skills, responsibilities, and ATS keywords from the job description.
    
    Args:
        jd_text (str): The job description text.

    Returns:
        str: Structured JSON output containing extracted data.
    """
    prompt = f"""
    You are an ATS optimization specialist. Extract the following key elements from the job description:

    - **Technical Skills** (Programming languages, tools, frameworks)
    - **Soft Skills** (Leadership, teamwork, communication)
    - **Key Responsibilities** (Job duties)
    - **Industry Keywords** (ATS-relevant phrases)
    - **Required Metrics** (Performance indicators mentioned)

    Format the output as **structured JSON**.

    Job Description:
    {jd_text}
    """
    return llm.invoke(prompt)

# Define as a LangChain tool
job_description_agent = Tool(
    name="Job Description Extractor",
    func=extract_job_data,
    description="Extracts ATS-friendly keywords and responsibilities from job descriptions."
)

if __name__ == "__main__":
    print("✅ Job Description Extractor Agent Ready!")