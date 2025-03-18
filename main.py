import gradio as gr
import os
from resume_parser import parse_resumes
from similarity import compute_similarity
from utils import remove_duplicate_resumes, merge_resumes
from email_fetch import fetch_email_resumes

# Ensure resume directory exists
RESUME_FOLDER = "resume_documents"
os.makedirs(RESUME_FOLDER, exist_ok=True)

def process_resumes(job_description):
    """Fetch emails, merge resumes, remove duplicates, parse, and compute similarity."""
    
    # Fetch resumes from email
    email_resumes = fetch_email_resumes()

    # Merge uploaded resumes
    merge_resumes(["/content/drive/MyDrive/Resumes", "/content/drive/MyDrive/archive (1)"], RESUME_FOLDER)

    # Remove duplicates
    unique_resumes = remove_duplicate_resumes(RESUME_FOLDER)

    # Parse resumes
    fixed_resumes = parse_resumes(unique_resumes)

    # Compute similarity
    shortlisted = compute_similarity(job_description, fixed_resumes, 0.4)

    # Format results for UI
    results = []
    for res in shortlisted[:5]:
        similarity_percentage = res[1] * 100  # Convert to percentage
        results.append(f"📄 {res[0]} | Similarity: {similarity_percentage:.2f}%")
    
    return "\n".join(results) if results else "❌ No matching resumes found!"

# Define Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# 🏢 AI Resume Screener")
    
    job_desc_input = gr.Textbox(label="Enter Job Description", placeholder="Looking for a Python Developer with SQL skills...")
    
    process_button = gr.Button("Process Resumes")
    
    output = gr.Textbox(label="Shortlisted Candidates", interactive=False)

    process_button.click(process_resumes, inputs=[job_desc_input], outputs=[output])

# Launch UI
demo.launch(server_name="0.0.0.0", server_port=7860)


