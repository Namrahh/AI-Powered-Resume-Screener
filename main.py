import os
import gradio as gr
from resume_parser import parse_resumes
from similarity import compute_similarity
from utils import remove_duplicate_resumes, merge_resumes
from email_fetch import fetch_email_resumes

# 🔹 Function to process resumes
def process_resumes(job_description, threshold, hr_email, uploaded_resumes):
    # 🔹 Fetch resumes from HR email (if provided)
    email_resumes = fetch_email_resumes(hr_email) if hr_email else []

    # 🔹 Save uploaded resumes to "resume_documents" folder
    uploaded_resumes = uploaded_resumes or []
    upload_folder = "resume_documents"
    os.makedirs(upload_folder, exist_ok=True)
    for file_path in uploaded_resumes:
        os.rename(file_path, os.path.join(upload_folder, os.path.basename(file_path)))

    # 🔹 Merge resumes from multiple sources
    merge_resumes(["resume_documents"], "resume_documents")

    # 🔹 Remove duplicate resumes
    unique_resumes = remove_duplicate_resumes("resume_documents")

    # 🔹 Parse resumes
    fixed_resumes = parse_resumes(unique_resumes)

    # 🔹 Compute similarity scores
    shortlisted = compute_similarity(job_description, fixed_resumes, threshold)

    # 🔹 Format results
    results = "\n".join([f"📄 {res[0]} | Score: {res[1]:.4f} | Path: {res[2]}" for res in shortlisted[:5]])

    return results if results else "No suitable candidates found."

# ✅ Gradio Web App
with gr.Blocks() as app:
    gr.Markdown("# 📝 AI-Powered Resume Screener")

    # 🔹 HR Email Input
    hr_email = gr.Textbox(label="HR Email (optional)", placeholder="Enter HR email for fetching resumes")

    # 🔹 Job Description Input
    job_desc = gr.Textbox(label="Enter Job Description", lines=5, placeholder="Enter job requirements here...")

    # 🔹 Similarity Threshold Slider
    threshold = gr.Slider(minimum=0.1, maximum=1.0, value=0.4, label="Similarity Threshold")

    # 🔹 Upload Resumes from Computer
    uploaded_resumes = gr.File(label="Upload Resumes (PDF/DOCX)", type="file", interactive=True, file_types=[".pdf", ".docx"])

    # 🔹 Submit Button
    submit_btn = gr.Button("Analyze Resumes")

    # 🔹 Output Display
    output_text = gr.Textbox(label="Shortlisted Candidates", interactive=False)

    # 🔹 Click Event
    submit_btn.click(process_resumes, inputs=[job_desc, threshold, hr_email, uploaded_resumes], outputs=output_text)

# ✅ Deploy on Railway (Uses the correct port)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))  # Railway assigns a dynamic port
    app.launch(server_name="0.0.0.0", server_port=port)




