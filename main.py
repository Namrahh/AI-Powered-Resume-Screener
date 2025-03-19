import gradio as gr
import os
import shutil
from resume_parser import parse_resumes
from similarity import compute_similarity
from utils import remove_duplicate_resumes, merge_resumes
from email_fetch import fetch_email_resumes

# ✅ Get Email Credentials Securely from Railway Environment Variables
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_FOLDER = "INBOX"

UPLOAD_FOLDER = "uploaded_resumes"
SHORTLIST_FOLDER = "shortlisted_resumes"

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SHORTLIST_FOLDER, exist_ok=True)

# Function to process resumes
def process_resumes(job_description, uploaded_files):
    resumes_list = []
    
    # 1️⃣ **Fetch resumes from email**
    email_resumes = fetch_email_resumes(EMAIL_USER, EMAIL_PASS, EMAIL_FOLDER)
    resumes_list.extend(email_resumes)
    
    # 2️⃣ **Save uploaded files (Supports multiple uploads)**
    if uploaded_files:
        for file in uploaded_files:
            file_path = os.path.join(UPLOAD_FOLDER, file.name)
            shutil.copy(file.name, file_path)
            resumes_list.append(file_path)

    # 3️⃣ **Merge resumes**
    merge_resumes([UPLOAD_FOLDER, "resume_documents"], "resume_documents")

    # 4️⃣ **Remove duplicate resumes**
    unique_resumes = remove_duplicate_resumes("resume_documents")

    # 5️⃣ **Parse resumes**
    parsed_resumes = parse_resumes(unique_resumes)

    # 6️⃣ **Compute similarity**
    shortlisted = compute_similarity(job_description, parsed_resumes, 0.4)

    # 7️⃣ **Save shortlisted resumes**
    shortlisted_files = []
    for res in shortlisted[:5]:
        filename = os.path.basename(res[0])
        shutil.copy(res[0], os.path.join(SHORTLIST_FOLDER, filename))
        shortlisted_files.append((filename, res[1]))

    # Return results with download links
    return [(f"📄 {file} | Score: {score:.4f}", os.path.join(SHORTLIST_FOLDER, file)) for file, score in shortlisted_files]

# **Gradio UI**
with gr.Blocks() as app:
    gr.Markdown("# 📄 AI-Powered Resume Screener")
    
    job_description = gr.Textbox(label="Enter Job Description", lines=3)

    with gr.Row():
        upload_button = gr.File(label="Upload Resumes", file_types=[".pdf", ".doc", ".docx"], type="file", multiple=True)
        fetch_email_button = gr.Button("Fetch from Emails")
    
    process_button = gr.Button("Process Resumes")
    
    output = gr.Dataframe(label="Shortlisted Candidates", headers=["Candidate", "Matching Score"])
    download_link = gr.File(label="Download Shortlisted Resumes")

    # **Button Click Actions**
    process_button.click(process_resumes, inputs=[job_description, upload_button], outputs=[output, download_link])

# **Deploy with Public URL**
if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)), share=True)

