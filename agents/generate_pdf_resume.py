from fpdf import FPDF

def clean_text(text):
    """Replace non-ASCII characters to avoid PDF encoding issues."""
    if not isinstance(text, str):
        return str(text)
    return (
        text.replace("–", "-")
            .replace("—", "-")
            .replace("“", "\"")
            .replace("”", "\"")
            .replace("’", "'")
            .replace("•", "-")
            .replace("•", "-")
    )

def generate_pdf_resume(basic_info, experience_data, filename="resume_output.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=10)
    
    # --- Header ---
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, clean_text(basic_info.get('full_name', 'Full Name')), ln=True)

    pdf.set_font("Arial", size=12)
    contact_line = f"Email: {basic_info.get('email', '')} | Phone: {basic_info.get('phone', '')}"
    pdf.cell(0, 8, clean_text(contact_line), ln=True)
    pdf.cell(0, 8, clean_text(f"Address: {basic_info.get('address', '')}"), ln=True)
    if basic_info.get("linkedin"):
        pdf.cell(0, 8, f"LinkedIn: {clean_text(basic_info['linkedin'])}", ln=True)
    if basic_info.get("github"):
        pdf.cell(0, 8, f"GitHub: {clean_text(basic_info['github'])}", ln=True)

    # --- Education ---
    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Education", ln=True)
    pdf.set_font("Arial", "", 12)
    for edu in basic_info.get("education", []):
        pdf.cell(0, 8, clean_text(f"{edu.get('degree', '')} - {edu.get('university', '')} ({edu.get('year', '')})"), ln=True)
        pdf.cell(0, 8, clean_text(f"Location: {edu.get('location', '')}"), ln=True)
        pdf.ln(2)

    # --- Experience Section ---
    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Professional Experience", ln=True)
    pdf.set_font("Arial", "", 12)

    for entry in experience_data:
        exp = entry.get("enhanced_resume", {})
        if isinstance(exp, str):
            continue  # safety check if mistakenly string

        role = exp.get("role", "Unknown Role")
        company = exp.get("company", "Unknown Company")
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, f"{clean_text(role)} at {clean_text(company)}", ln=True)

        pdf.set_font("Arial", "", 12)
        for point in exp.get("enhanced_experience", []):
            pdf.multi_cell(0, 8, f"- {clean_text(point)}")
        pdf.ln(3)

    # --- Skills Section ---
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Skills", ln=True)
    pdf.set_font("Arial", "", 12)

    tech_skills = []
    soft_skills = []
    for entry in experience_data:
        tech_skills.extend(entry.get("added_elements", {}).get("technical_tools", []))
        soft_skills.extend(entry.get("added_elements", {}).get("soft_skills", []))

    # Deduplicate and clean
    tech_skills = sorted(set(map(clean_text, tech_skills)))
    soft_skills = sorted(set(map(clean_text, soft_skills)))

    pdf.cell(0, 8, f"Technical Skills: {', '.join(tech_skills)}", ln=True)
    pdf.cell(0, 8, f"Soft Skills: {', '.join(soft_skills)}", ln=True)

    # --- Output ---
    pdf.output(filename)
    print(f"✅ Resume saved to {filename}")
    return filename
