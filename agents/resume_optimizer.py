import json
import re
from langchain.tools import Tool
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from agents.resume_extractor import extract_resume_data  # Import Second Agent

# Load API Key from .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize ChatGroq LLM
llm = ChatGroq(model="deepseek-r1-distill-llama-70b", api_key=GROQ_API_KEY)

def extract_json_from_response(response_text):
    match = re.search(r"\{.*\}", response_text, re.DOTALL)
    return match.group(0) if match else None

def generate_optimized_resume_per_client(client_experience):
    prompt = (
    "You are an expert resume writer and ATS optimization specialist. Your task is to enhance the provided resume experience "
    "for a **single client**, ensuring ATS-friendly formatting, impactful storytelling, and industry-specific keyword optimization "
    "by aligning the candidate's experience with the **job description requirements**.\n\n"

    "### 🎯 CORE OBJECTIVE ###\n"
    "Transform raw experience into a polished, compelling resume segment that:\n"
    "- Matches job description tools, responsibilities, and domain-specific keywords.\n"
    "- Demonstrates quantifiable business impact.\n"
    "- Aligns with both technical and strategic leadership expectations.\n\n"

    "### 🛠️ KEY ENHANCEMENTS TO BE APPLIED ###\n"
    "1️⃣ **Replace or Enrich Tools With JD-Relevant Technologies**\n"
    "- Cross-reference tools in the job description and resume.\n"
    "- Replace outdated or irrelevant tools with those mentioned in the JD (e.g., PyTorch, XGBoost, Scala, Databricks).\n"
    "- Integrate missing tools into the **existing context** instead of adding separate lines.\n\n"

    "2️⃣ **Enhance Existing Story With JD-Specific Contributions**\n"
    "- Embed job-relevant problem-solving, scaling, and deployment scenarios into the current story.\n"
    "- Prioritize R&D, reusable code templates, CI/CD, MLOps, business alignment, and dashboard delivery as described in the job description.\n"
    "- Ensure all additions feel **authentic**, not generic.\n\n"

    "3️⃣ **Ensure Output Has Exactly 5 Bullet Points per Role**\n"
    "- 🔹 **3 Concise Points (22-27 words):** Highlight key tools, responsibilities, and impact.\n"
    "- 🔹 **2 Detailed Points (25-30 words):** Include a challenge, solution, and business outcome.\n"
    "- Avoid repetition. Each point should add new value.\n\n"

    "4️⃣ **Summarize Modifications Clearly**\n"
    "- Show what was added in terms of:\n"
    "  • Technical tools (from JD)\n"
    "  • Soft skills or leadership traits\n"
    "  • Scenarios or deliverables\n"
    "- Describe real-world scenarios logically extended from the original experience.\n\n"

"5️⃣ **Format Requirements (MANDATORY)**\n"
"- Respond ONLY in **valid JSON format**.\n"
"- DO NOT include markdown, code blocks, explanations, or comments.\n"
"- Your output MUST contain the following top-level keys:\n\n"
"  📌 `added_elements`: \n"
"      - `technical_tools`: List of newly integrated tools (from job description).\n"
"      - `soft_skills`: List of soft skills emphasized in enhanced experience.\n\n"
"  📌 `modifications`: \n"
"      - `existing_story_enrichment`: Brief summary of how existing story was improved.\n"
"      - `new_contributions`: Summary of new contributions added.\n\n"
"  📌 `tool_integration`: \n"
"      - `replaced_tools`: List of old tools replaced.\n"
"      - `new_integrations`: List of tools added from the job description.\n"
"      - `integration_details`: How tools were logically added to experience.\n\n"
"  📌 `real_world_scenarios`: \n"
"      - List of JD-aligned problem-solving use cases implemented in real-world settings.\n\n"
"  📌 `enhanced_resume`: \n"
"      - `role`: Job title at client\n"
"      - `company`: Client/organization name\n"
"      - `enhanced_experience`: List of **exactly 5 bullet points** with:\n"
"          • 3 concise bullets (22-27 words)\n"
"          • 2 detailed bullets (25-30 words)\n"
"      - `tools_used`: List of technical tools referenced in bullets.\n"
"      - `industry_keywords`: ATS keywords aligned with the job description.\n\n"
    "--- CLIENT EXPERIENCE DATA ---\n"
    f"{json.dumps(client_experience, indent=2)}\n"
)
    response = llm.invoke(prompt)
    response_text = response.content if hasattr(response, "content") else str(response)
    json_response = extract_json_from_response(response_text)

    if json_response is None:
        return {"error": "Invalid JSON response from LLM"}

    try:
        return json.loads(json_response)
    except json.JSONDecodeError as e:
        print("\n❌ JSON Decoding Error:", str(e))
        return {"error": "Invalid JSON response from LLM"}

def process_all_clients(extracted_data_per_client):
    all_optimized_clients = []

    for client_data in extracted_data_per_client:
        optimized_client = generate_optimized_resume_per_client(client_data)
        if "error" not in optimized_client:
            all_optimized_clients.append(optimized_client)

    return all_optimized_clients

resume_optimizer_agent = Tool(
    name="Resume Optimizer Per Client",
    func=process_all_clients,
    description="Generates an ATS-optimized experience section for each client."
)

if __name__ == "__main__":
    print("✅ Resume Optimizer Agent Ready!")
