import gradio as gr
import os
import concurrent.futures
from resume_parser import parse_resume
from similarity import compute_similarity
from utils import remove_duplicate_resumes, save_uploaded_resumes
from email_fetch import fetch_email_resumes

def process_resumes(email, password, job_description, uploaded_resumes):
    """
    Processes resumes from uploaded files and emails, then shortlists candidates based on job description.
    """

    # 🔹 Fetch resumes from email (Parallel Processing)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_email_resumes = executor.submit(fetch_email_resumes, email, password)
        email_resumes = future_email_resumes.result()

    # 🔹 Save uploaded resumes efficiently
    uploaded_paths = save_uploaded_resumes(uploaded_resumes)

    # 🔹 Merge email & uploaded resumes, then remove duplicates
    all_resumes = remove_duplicate_resumes(email_resumes + uploaded_paths)

    # 🔹 Parse resumes in parallel (Faster Processing)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        parsed_resumes = list(executor.map(parse_resume, all_resumes))

    # 🔹 Compute similarity scores
    shortlisted = compute_similarity(job_description, parsed_resumes, threshold=0.4)

    return [f"📄 {res[0]} | Score: {res[1]:.4f}" for res in shortlisted[:5]]

# 🎨 UI with Gradio
with gr.Blocks() as app:
    gr.Markdown("# 📄 AI-Powered Resume Screener")

    # 🔹 Email & Password Fields
    email_input = gr.Textbox(label="Enter Your Email", type="text", placeholder="example@gmail.com")
    password_input = gr.Textbox(label="Enter Your Email Password", type="password", placeholder="••••••••")

    # 🔹 Job Description Field
    job_description = gr.Textbox(label="Enter Job Description", lines=5)

    # 🔹 Upload Resumes (Multiple Files Allowed)
    upload_button = gr.File(label="Upload Resumes", file_types=[".pdf", ".doc", ".docx"], type="file", interactive=True, multiple=True)

    # 🔹 Process Button
    process_button = gr.Button("Process Resumes")

    # 🔹 Output Section
    output = gr.Textbox(label="Shortlisted Candidates", interactive=False)

    # 🔹 Button Click Event
    process_button.click(
        process_resumes,  
        inputs=[email_input, password_input, job_description, upload_button],  
        outputs=[output]
    )

# 🚀 Launch App
if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)), share=True)

