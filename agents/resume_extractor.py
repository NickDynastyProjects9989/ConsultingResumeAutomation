import json
import re
from langchain.tools import Tool
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from agents.jd_extractor import extract_job_data  # Import JD Extractor

# Load API Key from .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize ChatGroq LLM
llm = ChatGroq(model="deepseek-r1-distill-llama-70b", api_key=GROQ_API_KEY)

def extract_json_from_response(response_text):
    """
    Extracts only the JSON part from a mixed LLM response.

    Args:
        response_text (str): The raw response from the LLM.

    Returns:
        str: Cleaned JSON string.
    """
    # Use regex to find the first occurrence of `{` and last `}`
    match = re.search(r"\{.*\}", response_text, re.DOTALL)
    if match:
        return match.group(0)  # Return only the extracted JSON
    return None  # If no JSON is found, return None

def extract_resume_data(resume_text, jd_text):
    """
    Extracts key skills, responsibilities, and experience from the provided resume.
    If extracted JD JSON is provided, compares against it to identify missing skills.

    Args:
        resume_text (str): Candidate's resume.
        jd_text (str): Job description text.

    Returns:
        dict: Extracted resume details and missing skills.
    """

    # Step 1: Extract JD Data
    extracted_jd_data = extract_job_data(jd_text)  # Call First Agent

    # Fix: Convert AIMessage object to string
    extracted_jd_text = extracted_jd_data.content if hasattr(extracted_jd_data, "content") else str(extracted_jd_data)

    # Extract and parse JD JSON
    jd_json_text = extract_json_from_response(extracted_jd_text)
    
    try:
        jd_json = json.loads(jd_json_text) if jd_json_text else {}
        jd_summary = "\n".join(
            [f"- {key}: {', '.join(value) if isinstance(value, list) else value}"
             for key, value in jd_json.items()]
        )
    except json.JSONDecodeError:
        jd_summary = "Invalid JD format received."

    # LLM Prompt for Resume Extraction
    # LLM Prompt for Resume Extraction and Story Enhancement
    prompt = (
        "You are an ATS optimization specialist and expert resume writer. Your task is to analyze the provided **resume** and "
        "compare it against the **job description** to find gaps, add missing skills, and extend the story in a meaningful way "
        "that aligns with the job requirements while preserving the candidate’s original contributions.\n\n"

        "### TASKS ###\n"
        "1️⃣ **Extract Key Details** from the resume:\n"
        "   - **Technical Skills**: Programming languages, tools, frameworks.\n"
        "   - **Soft Skills**: Leadership, teamwork, communication, problem-solving.\n"
        "   - **Experience Sections**: Extract each role’s key responsibilities, tools used, and achievements.\n\n"

        "2️⃣ **Find and Extend Missing Story Elements**:\n"
        "   - Compare the extracted experience with the job description.\n"
        "   - Identify areas where additional details or achievements could enhance alignment.\n"
        "   - Extend the story of each experience without losing authenticity.\n"
        "   - Ensure that modifications feel like a natural **extension of the original story**, "
        "     rather than artificial additions.\n\n"

        "3️⃣ **Generate a Well-Structured Paragraph for Each Role**:\n"
        "   - Combine the original experience with the missing story into a cohesive narrative.\n"
        "   - Ensure that the paragraph **flows naturally** and integrates the **missing elements seamlessly**.\n"
        "   - Use **action-oriented language**, focus on **impact**, and highlight **problem-solving skills**.\n\n"

        "4️⃣ **Enhance ATS Optimization**:\n"
        "   - Identify missing **industry keywords** and integrate them meaningfully.\n"
        "   - Ensure the resume naturally includes relevant **technical and soft skills**.\n"
        "   - Reframe experience points to highlight **problem-solving, impact, and metrics**.\n\n"

        "### OUTPUT REQUIREMENT ###\n"
        "📌 Respond **ONLY in valid JSON format**. Do NOT include explanations, markdown, or extra text.\n\n"
        "Output Example:\n"
        '{\n'
        '  "technical_skills": ["Python", "SQL", "Databricks"],\n'
        '  "soft_skills": ["Leadership", "Collaboration", "Problem-Solving"],\n'
        '  "experience_sections": [\n'
        '    {\n'
        '      "role": "Senior Data Engineer",\n'
        '      "company": "XYZ Corp",\n'
        '      "existing_story": "Built ETL pipelines and optimized workflows using Spark and AWS.",\n'
        '      "missing_story_extension": "Additionally, designed scalable data lake architectures, reducing query latency by 30%."\n'
        '      "enhanced_experience": [\n'
        '        "Developed and optimized ETL pipelines using Spark and AWS, reducing processing time by 40%.",\n'
        '        "Designed and implemented scalable data lake solutions, improving analytics efficiency by 30%.",\n'
        '        "Collaborated with data scientists to deploy machine learning models in production using Databricks."\n'
        '      ],\n'
        '      "tools_used": ["AWS", "Spark", "Databricks", "SQL"],\n'
        '      "industry_keywords": ["ETL", "Data Pipelines", "AWS Redshift", "Databricks"],\n'
        '      "story_paragraph": "At XYZ Corp, I spearheaded the development and optimization of ETL pipelines using Spark and AWS, leading to a 40% reduction in processing time. '
        'In response to growing data demands, I designed and implemented scalable data lake solutions, improving analytics efficiency by 30%. '
        'Collaborating closely with data scientists, I ensured seamless deployment of machine learning models in production using Databricks, enhancing the company’s predictive analytics capabilities."\n'
        '    }\n'
        '  ]\n'
        '}\n\n'

        "NOW GENERATE THE RESPONSE IN STRICT JSON FORMAT BASED ON THE PROVIDED RESUME AND JOB DESCRIPTION:\n\n"
        "--- RESUME ---\n"
        f"{resume_text}\n\n"
        "--- JOB DESCRIPTION DETAILS ---\n"
        f"{jd_summary}\n"
    )

    # Call LLM for response
    response = llm.invoke(prompt)

    # Fix: Extract AIMessage content and clean response
    response_text = response.content if hasattr(response, "content") else str(response)
   # Debugging: Print raw LLM output

    # Extract only JSON from response
    json_response = extract_json_from_response(response_text)

    if json_response is None:
        print("\n❌ ERROR: LLM response does not contain valid JSON.")
        return {"error": "Invalid JSON response from LLM"}
    
    
    # Convert the response to a Python dictionary (safe handling)
    try:
        extracted_data = json.loads(json_response)
        print(extracted_data)
        return extracted_data
    except json.JSONDecodeError as e:
        print("\n❌ JSON Decoding Error:", str(e))  # Debug: Print exact JSON error
        return {"error": "Invalid JSON response from LLM"}

# Define as a LangChain tool
resume_extractor_agent = Tool(
    name="Resume Extractor",
    func=extract_resume_data,
    description="Extracts skills, experience, and responsibilities from a resume."
)

if __name__ == "__main__":
    print("✅ Resume Extractor Agent Ready!")
