import gradio as gr
import os
from pyngrok import ngrok
from resume_parser import parse_resumes
from similarity import compute_similarity
from utils import remove_duplicate_resumes, merge_resumes
from email_fetch import fetch_email_resumes

# Function to handle email fetching + file upload
def process_resumes(email, password, job_description, uploaded_files):
    resumes = []

    # If HR enters email & password, fetch resumes from email
    if email and password:
        email_resumes = fetch_email_resumes(email, password)
        resumes.extend(email_resumes)  

    # If HR uploads files, process them
    if uploaded_files:
        uploaded_paths = [file.name for file in uploaded_files]
        resumes.extend(uploaded_paths)

    if not resumes:
        return "No resumes found. Please upload or fetch from email."

    # Merge resumes into a single folder
    merge_resumes(resumes, "resume_documents")

    # Remove duplicates
    unique_resumes = remove_duplicate_resumes("resume_documents")

    # Parse resumes
    fixed_resumes = parse_resumes(unique_resumes)

    # Compute similarity
    shortlisted = compute_similarity(job_description, fixed_resumes, 0.4)

    # Format output
    return [(res[0], f"{res[1]*100:.2f}%") for res in shortlisted[:5]]  # Convert score to percentage

# Define Gradio UI
demo = gr.Interface(
    fn=process_resumes,
    inputs=[
        gr.Textbox(label="HR Email Address", placeholder="Optional: Enter email to fetch resumes"),
        gr.Textbox(label="HR Email Password", type="password", placeholder="Optional: Enter password"),
        gr.Textbox(lines=4, label="Job Description", placeholder="Enter job requirements here..."),
        gr.File(file_types=[".pdf", ".docx"], label="Upload Resumes", multiple=True)
    ],
    outputs=gr.Dataframe(headers=["Resume", "Similarity Score"]),
    title="AI Resume Screener",
    description="Upload resumes or fetch them via email, then shortlist candidates based on similarity."
)

# Open a tunnel to the Gradio app
port = int(os.getenv("PORT", 7860))  # Use PORT from environment variables or default to 7860
public_url = ngrok.connect(port).public_url
print(f"🌍 Public URL: {public_url}")

# Launch Gradio app
demo.launch(server_name="0.0.0.0", server_port=port)




