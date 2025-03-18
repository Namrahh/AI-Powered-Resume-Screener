import gradio as gr
import os
from resume_parser import parse_resumes
from similarity import compute_similarity
from utils import remove_duplicate_resumes, merge_resumes
from email_fetch import fetch_email_resumes

# Define job description
JOB_DESCRIPTION = """
Looking for a Python Developer with experience in data analysis.
Required skills: Python, Pandas, NumPy, Data Cleaning, Data Visualization, SQL,
Machine Learning, Jupyter Notebook, Data Science.
"""

def fetch_resumes():
    """Fetch resumes from unread emails and return the count."""
    resumes = fetch_email_resumes()
    return f"✅ Fetched {len(resumes)} resumes."

def upload_resumes(files):
    """Handle file uploads."""
    resume_paths = [file.name for file in files]
    merge_resumes(resume_paths, "resume_documents")
    return f"✅ Uploaded {len(resume_paths)} resumes."

def process_resumes():
    """Process resumes (remove duplicates, parse, and compute similarity)."""
    unique_resumes = remove_duplicate_resumes("resume_documents")
    fixed_resumes = parse_resumes(unique_resumes)
    shortlisted = compute_similarity(JOB_DESCRIPTION, fixed_resumes, 0.4)

    if not shortlisted:
        return "⚠️ No matching resumes found!"
    
    result = "\n".join([f"📄 {res[0]} | Score: {res[1]:.4f}" for res in shortlisted[:5]])
    return f"✅ Top Matches:\n\n{result}"

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# 📄 AI-Powered Resume Screener")

    # Email fetching
    with gr.Row():
        fetch_btn = gr.Button("📩 Fetch Resumes from Email")
        fetch_output = gr.Textbox(label="Email Fetch Status")

    fetch_btn.click(fetch_resumes, outputs=fetch_output)

    # File Upload
    with gr.Row():
        file_input = gr.File(label="Upload Resume(s)", multiple=True)
        upload_output = gr.Textbox(label="Upload Status")

    upload_btn = gr.Button("📤 Upload")
    upload_btn.click(upload_resumes, inputs=file_input, outputs=upload_output)

    # Processing
    with gr.Row():
        process_btn = gr.Button("🚀 Process & Shortlist Resumes")
        process_output = gr.Textbox(label="Shortlisted Candidates")

    process_btn.click(process_resumes, outputs=process_output)

# Run the app
demo.launch(server_name="0.0.0.0", server_port=5000)

