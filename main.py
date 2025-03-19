import gradio as gr
import os
from resume_parser import parse_resumes
from similarity import compute_similarity
from utils import remove_duplicate_resumes, merge_resumes
from email_fetch import fetch_email_resumes
import shutil

UPLOAD_FOLDER = "uploaded_resumes"

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def process_resumes(job_description, uploaded_files):
    # Save uploaded resumes
    local_resumes = []
    for file in uploaded_files:
        file_path = os.path.join(UPLOAD_FOLDER, file.name)
        shutil.copy(file.name, file_path)
        local_resumes.append(file_path)

    # Fetch resumes from email
    email_resumes = fetch_email_resumes()

    # Merge all resumes (uploaded + email)
    all_resumes = local_resumes + email_resumes
    merge_resumes(all_resumes, "resume_documents")

    # Remove duplicates
    unique_resumes = remove_duplicate_resumes("resume_documents")

    # Parse resumes
    fixed_resumes = parse_resumes(unique_resumes)

    # Compute similarity
    shortlisted = compute_similarity(job_description, fixed_resumes, 0.4)

    # Prepare results
    results = [f"📄 {res[0]} | Score: {res[1]:.4f}" for res in shortlisted[:5]]

    # Prepare downloadable files
    shortlisted_files = [res[0] for res in shortlisted]
    return results, shortlisted_files

# Gradio UI
with gr.Blocks() as app:
    gr.Markdown("# 📄 AI-Powered Resume Screener")

    job_description = gr.Textbox(label="Enter Job Description", lines=5)
    uploaded_files = gr.File(label="Upload Resumes", file_types=[".pdf", ".docx"], multiple=True)
    
    process_button = gr.Button("Process Resumes")

    output = gr.Textbox(label="Shortlisted Candidates", interactive=False)
    download_button = gr.File(label="Download Shortlisted Resumes")

    process_button.click(
        process_resumes, 
        inputs=[job_description, uploaded_files], 
        outputs=[output, download_button]
    )

# 🚀 Deploy on Railway
if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)), share=True)
