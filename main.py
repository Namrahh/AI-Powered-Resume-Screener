import gradio as gr
from resume_parser import extract_resume_text, parse_resumes
from similarity import compute_similarity
from utils import fetch_email_resumes

def resume_screening(job_description, resume_files=None):
    print("✅ Received Job Description")

    # Process uploaded resumes
    if resume_files:
        print("📂 Processing uploaded resumes...")
        resumes = parse_resumes(resume_files)
    else:
        resumes = []

    # Fetch resumes from email (if needed)
    email_resumes = fetch_email_resumes()
    if email_resumes:
        resumes.extend(email_resumes)

    print("🔍 Total resumes being checked:", len(resumes))

    # Compute similarity and shortlist resumes
    shortlisted_resumes = compute_similarity(job_description, resumes)

    print("✅ Shortlisting done! Found:", len(shortlisted_resumes))

    if not shortlisted_resumes:
        return "No matching resumes found.", []

    # Keep only the top 5 candidates
    shortlisted_resumes = sorted(shortlisted_resumes, key=lambda x: x[1], reverse=True)[:5]

    print("🏆 Final Top 5:", shortlisted_resumes)

    return "\n".join([f"{res[0]} (Score: {res[1]:.2f})" for res in shortlisted_resumes]), []

# Gradio interface
iface = gr.Interface(
    fn=resume_screening,
    inputs=[
        gr.Textbox(label="Job Description"),
        gr.File(file_types=[".pdf", ".docx"], type="filepath", label="Upload Resumes", file_count="multiple")
    ],
    outputs=["text", "file"],
    title="AI Resume Screener",
    description="Enter a job description and upload resumes (optional) to find the best match."
)

iface.launch(debug=True)
