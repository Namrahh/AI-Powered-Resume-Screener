import gradio as gr
import os
from resume_parser import parse_resumes
from similarity import compute_similarity
from utils import remove_duplicate_resumes, merge_resumes
from email_fetch import fetch_email_resumes

def process_resumes(job_description):
    # Fetch resumes from email
    email_resumes = fetch_email_resumes()

    # Merge resumes
    merge_resumes(["resume_documents"], "resume_documents")

    # Remove duplicates
    unique_resumes = remove_duplicate_resumes("resume_documents")

    # Parse resumes
    fixed_resumes = parse_resumes(unique_resumes)

    # Compute similarity
    shortlisted = compute_similarity(job_description, fixed_resumes, 0.4)

    return [f"📄 {res[0]} | Score: {res[1]:.4f}" for res in shortlisted[:5]]

with gr.Blocks() as app:
    gr.Markdown("# 📄 AI-Powered Resume Screener")
    
    job_description = gr.Textbox(label="Enter Job Description", lines=5)
    process_button = gr.Button("Process Resumes")
    
    output = gr.Textbox(label="Shortlisted Candidates", interactive=False)
    
    process_button.click(process_resumes, inputs=[job_description], outputs=[output])

# 🚀 Keep the app running
if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
