import gradio as gr
import os
from resume_parser import parse_resumes
from similarity import compute_similarity
from utils import remove_duplicate_resumes, merge_resumes
from email_fetch import fetch_email_resumes

# Function to process resumes from email
def process_resumes(email, password, job_description):
    os.environ["EMAIL_USER"] = email
    os.environ["EMAIL_PASS"] = password

    # Fetch resumes from email
    email_resumes = fetch_email_resumes()

    # Merge and clean resumes
    merge_resumes(["resume_documents"], "resume_documents")
    unique_resumes = remove_duplicate_resumes("resume_documents")
    fixed_resumes = parse_resumes(unique_resumes)

    # Compute similarity
    shortlisted = compute_similarity(job_description, fixed_resumes, 0.4)

    # Prepare output
    result_text = "📄 **Shortlisted Resumes from Email:**\n\n"
    for res in shortlisted:
        result_text += f"🔹 **{res[0]}** | **Score:** {res[1]:.4f}\n"

    return result_text

# Function to process resumes uploaded manually
def process_uploaded_resumes(files, job_description):
    # Save uploaded files
    save_path = "uploaded_resumes"
    os.makedirs(save_path, exist_ok=True)
    
    file_paths = []
    for file in files:
        file_path = os.path.join(save_path, file.name)
        file_paths.append(file_path)
        with open(file_path, "wb") as f:
            f.write(file.read())

    # Merge and clean resumes
    merge_resumes([save_path], save_path)
    unique_resumes = remove_duplicate_resumes(save_path)
    fixed_resumes = parse_resumes(unique_resumes)

    # Compute similarity
    shortlisted = compute_similarity(job_description, fixed_resumes, 0.4)

    # Prepare output
    result_text = "📄 **Shortlisted Resumes from Uploaded Files:**\n\n"
    for res in shortlisted:
        result_text += f"🔹 **{res[0]}** | **Score:** {res[1]:.4f}\n"

    return result_text

# Create UI
with gr.Blocks() as demo:
    gr.Markdown("# 📩 AI Resume Screener")

    # Email fetch section
    gr.Markdown("### 🔍 Fetch Resumes from Email")
    with gr.Row():
        email_input = gr.Textbox(label="📧 Enter Your Email")
        password_input = gr.Textbox(label="🔑 Enter Your App Password", type="password")
    
    job_description = gr.Textbox(label="📝 Enter Job Description")
    fetch_button = gr.Button("📤 Fetch & Analyze Resumes")
    email_output_text = gr.Markdown()

    # File upload section
    gr.Markdown("### 📂 Upload Resumes from Computer")
    file_input = gr.File(label="📁 Upload Resume Files", type="file", multiple=True)
    upload_button = gr.Button("📤 Analyze Uploaded Resumes")
    upload_output_text = gr.Markdown()

    # Click actions
    fetch_button.click(process_resumes, inputs=[email_input, password_input, job_description], outputs=email_output_text)
    upload_button.click(process_uploaded_resumes, inputs=[file_input, job_description], outputs=upload_output_text)

demo.launch(share=True, server_name="0.0.0.0", server_port=int(os.getenv("PORT", 7860)))




