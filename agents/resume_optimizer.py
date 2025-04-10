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
    """
    Extracts only the JSON part from a mixed LLM response.

    Args:
        response_text (str): The raw response from the LLM.

    Returns:
        str: Cleaned JSON string.
    """
    match = re.search(r"\{.*\}", response_text, re.DOTALL)
    return match.group(0) if match else None  # Return only the extracted JSON

def generate_optimized_resume_per_client(client_experience):
    """
    Generates an ATS-optimized resume for a **single client** by integrating extracted experience data.

    Args:
        client_experience (dict): Client-specific extracted resume data.

    Returns:
        dict: Optimized experience for the client.
    """

    # LLM Prompt for ATS-Optimized Resume Per Client
    prompt = (
    "You are an expert resume writer and ATS optimization specialist. Your task is to enhance the provided resume experience "
    "for a **single client**, ensuring ATS-friendly formatting, impactful storytelling, and industry-specific keyword optimization "
    "by aligning the candidate's experience with the **job description requirements**.\n\n"

    "### **KEY ENHANCEMENTS TO BE APPLIED** ###\n"
    "1️⃣ **Replace existing tools with the most relevant ones from the job description**\n"
    "   - Identify tools in the job description that are missing from the resume.\n"
    "   - Replace or enhance existing tools in the experience where applicable.\n"
    "   - Ensure **seamless integration of tools** into the enhanced experience points.\n\n"

    "2️⃣ **Enhance the existing experience points instead of just adding new ones**\n"
    "   - Modify current points by incorporating **missing technical details, problem-solving scenarios, and tools**.\n"
    "   - Ensure a **logical progression** in how the job description aligns with the candidate’s experience.\n"
    "   - **No redundant additions**—only meaningful and contextual enhancements.\n\n"

    "3️⃣ **Ensure the output has exactly 5 bullet points per role**\n"
    "   - 🔹 **3 Concise Bullet Points (22-27 words each):** Highlight key tasks, accomplishments, and tools.\n"
    "   - 🔹 **2 Detailed Bullet Points (25-30 words each):** Explain a challenge, the solution, and the impact.\n\n"

    "4️⃣ **Highlight how the existing story was modified**\n"
    "   - Show how the missing elements were incorporated into the experience.\n"
    "   - Describe the **real-world scenarios** generated based on the existing story.\n"
    "   - Ensure that all modifications **feel natural and aligned** with the candidate’s role.\n\n"

    "### **STRICT OUTPUT FORMAT (JSON)** ###\n"
    "📌 **Respond ONLY in valid JSON format. Do NOT include markdown, explanations, or extra text.**\n"
    "Ensure the JSON follows the structured format for easy parsing.\n\n"

    "```json\n"
    "{\n"
    "  \"added_elements\": {\n"
    "    \"technical_skills\": [\"Scala\", \"MongoDB\", \"MapReduce\", \"AWS S3\", \"EC2\"],\n"
    "    \"soft_skills\": [\"Leadership\", \"Team Collaboration\", \"Strategic Thinking\"]\n"
    "  },\n"

    "  \"modifications\": {\n"
    "    \"existing_story\": \"Developed and deployed AI-driven predictive models, improving fraud detection by 30%.\",\n"
    "    \"enhanced_story\": \"Developed and deployed AI-driven predictive models, improving fraud detection by 30%. "
    "Recognizing gaps, I implemented real-time anomaly detection pipelines, reducing false positives by 20%.\"\n"
    "  },\n"

    "  \"tool_integration\": {\n"
    "    \"previous_tools\": [\"Python\", \"TensorFlow\"],\n"
    "    \"new_tools_added\": [\"Scala\", \"MongoDB\", \"AWS S3\"],\n"
    "    \"integration_details\": \"Upgraded ML workflows by incorporating Scala for high-performance computations and MongoDB for efficient model storage, optimizing fraud detection speed.\"\n"
    "  },\n"

    "  \"real_world_scenarios\": [\n"
    "    \"Optimized fraud detection by building real-time anomaly pipelines using AWS S3 and MapReduce, reducing transaction review time by 25%.\",\n"
    "    \"Enhanced AI-driven insights by transitioning model storage to MongoDB, improving query efficiency by 40%.\"\n"
    "  ],\n"

    "  \"enhanced_resume\": {\n"
    "    \"role\": \"Senior Data Scientist\",\n"
    "    \"company\": \"XYZ Corp\",\n"
    "    \"enhanced_experience\": [\n"
    "      \"Developed and deployed AI-driven predictive models, improving fraud detection accuracy by 30%.\",\n"
    "      \"Designed scalable anomaly detection systems, reducing false positives by 20% through real-time analytics and advanced feature engineering.\",\n"
    "      \"Optimized data pipelines for high-velocity financial transactions using Scala and AWS S3, improving processing speeds by 35%.\",\n"
    "      \"Led security-compliant deployment of AI models on AWS, implementing encryption techniques to ensure data privacy and regulatory compliance.\",\n"
    "      \"Collaborated with cross-functional teams to integrate AI models into production systems, enhancing operational efficiency.\"\n"
    "    ],\n"
    "    \"tools_used\": [\"AWS S3\", \"EC2\", \"Scala\", \"MongoDB\", \"Spark\"],\n"
    "    \"industry_keywords\": [\"Machine Learning\", \"Fraud Detection\", \"Data Pipelines\", \"Real-Time Analytics\"]\n"
    "  }\n"
    "}\n"
    "```\n\n"

    "NOW GENERATE THE FINAL ATS-OPTIMIZED EXPERIENCE FOR THE CLIENT:\n\n"
    "--- CLIENT EXPERIENCE DATA ---\n"
    f"{json.dumps(client_experience, indent=2)}\n"
    )


    # Call LLM for response
    response = llm.invoke(prompt)

    # Extract AIMessage content and clean response
    response_text = response.content if hasattr(response, "content") else str(response)

    # Extract only JSON from response
    json_response = extract_json_from_response(response_text)

    if json_response is None:
        return {"error": "Invalid JSON response from LLM"}
    

    # Convert the response to a Python dictionary (safe handling)
    try:
        optimized_client_resume = json.loads(json_response)
        return optimized_client_resume
    except json.JSONDecodeError as e:
        print("\n❌ JSON Decoding Error:", str(e))  # Debug: Print exact JSON error
        return {"error": "Invalid JSON response from LLM"}

def process_all_clients(resume_text, jd_text):
    """
    Extracts resume data, processes each client separately, and merges optimized experiences.

    Args:
        resume_text (str): Candidate's original resume.
        jd_text (str): Job description text.

    Returns:
        list: List of optimized experience sections per client.
    """

    # Step 1: Extract Resume Data Per Client
    extracted_resume_data = extract_resume_data(resume_text, jd_text)

    if "error" in extracted_resume_data:
        return {"error": "Failed to extract resume details."}

    experience_sections = extracted_resume_data.get("experience_sections", [])

    all_optimized_clients = []

    # Step 2: Process Each Client Separately
    for client_experience in experience_sections:
      
        optimized_client = generate_optimized_resume_per_client(client_experience)
        print(optimized_client)
        if "error" not in optimized_client:
            all_optimized_clients.append(optimized_client)

    return all_optimized_clients

# Define as a LangChain tool
resume_optimizer_agent = Tool(
    name="Resume Optimizer Per Client",
    func=process_all_clients,
    description="Generates an ATS-optimized experience section for each client."
)

if __name__ == "__main__":
    print("✅ Resume Optimizer Agent Ready!")
