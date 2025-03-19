import gradio as gr
import os
import concurrent.futures
import shutil
from resume_parser import parse_resumes
from similarity import compute_similarity
from utils import remove_duplicate_resumes, save_uploaded_resumes, download_resumes_from_email

SHORTLISTED_FOLDER = "shortlisted_resumes"

def save_shortlisted_resumes(shortlisted, destination_folder=SHORTLISTED_FOLDER):
    """Save shortlisted resumes to a separate folder for downloading."""
    os.makedirs(destination_folder, exist_ok=True)
    shortlisted_files = []
    
    for res in shortlisted:
        source_path = res["filepath"]
        destination_path = os.path.join(destination_folder, os.path.basename(source_path))
        shutil.copy(source_path, destination_path)
        shortlisted_files.append(destination_path)
    
    return shortlisted_files

import socket

def is_imap_port_open():
    """Check if IMAP (port 993) is open on the server."""
    test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = test_socket.connect_ex(("imap.gmail.com", 993))
    return result == 0
    
def process_resumes(email, password, job_description, uploaded_resumes):
    """Processes resumes from email and uploaded files, then shortlists candidates."""

    if not is_imap_port_open():
        return ["❌ IMAP (Port 993) is blocked on this server. Email fetching won't work."], []

    # 🔹 Fetch resumes from email
    email_resumes = download_resumes_from_email(email, password)

    # 🔹 Save uploaded resumes
    uploaded_paths = save_uploaded_resumes(uploaded_resumes)

    # 🔹 Merge email & uploaded resumes, then remove duplicates
    all_resumes = remove_duplicate_resumes(email_resumes + uploaded_paths)

    # 🔹 Parse resumes in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        parsed_resumes = list(executor.map(parse_resumes, all_resumes))

    # 🔹 Compute similarity scores
    shortlisted = compute_similarity(job_description, parsed_resumes, threshold=0.4)

    # 🔹 Save shortlisted resumes to a folder for downloading
    shortlisted_files = save_shortlisted_resumes(shortlisted)

    # 🔹 Return formatted shortlist & paths for download
    shortlist_text = [f"📄 {res['filename']} | Score: {res['score']:.4f}" for res in shortlisted[:5]]
    return shortlist_text, shortlisted_files  # Returns text & file paths for download

# 🎨 UI with Gradio
with gr.Blocks() as app:
    gr.Markdown("# 📄 AI-Powered Resume Screener")

    # 🔹 Email & Password Fields
    email_input = gr.Textbox(label="Enter Your Email", type="text", placeholder="example@gmail.com")
    password_input = gr.Textbox(label="Enter Your Email Password", type="password", placeholder="••••••••")

    # 🔹 Job Description Field
    job_description = gr.Textbox(label="Enter Job Description", lines=5)

    upload_button = gr.Files(
    label="Upload Resumes",
    file_types=[".pdf", ".doc", ".docx"],
    interactive=True
)

    # 🔹 Process Button
    process_button = gr.Button("Process Resumes")

    # 🔹 Output Section
    output = gr.Textbox(label="Shortlisted Candidates", interactive=False)

    # 🔹 Download Button
    download_files = gr.File(label="📥 Download Shortlisted Resumes", interactive=True, type="file", multiple=True)

    # 🔹 Button Click Event
    process_button.click(
        process_resumes,  
        inputs=[email_input, password_input, job_description, upload_button],  
        outputs=[output, download_files]  # Now downloads shortlisted resumes
    )

# 🚀 Launch App
if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))

