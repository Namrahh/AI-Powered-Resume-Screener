import gradio as gr
import os
from resume_parser import parse_resumes
from similarity import compute_similarity
from utils import remove_duplicate_resumes, merge_resumes
from email_fetch import fetch_email_resumes

# Fetch resumes from email
email_resumes = fetch_email_resumes()

# Merge resumes
merge_resumes(["/content/drive/MyDrive/Resumes", "/content/drive/MyDrive/archive (1)"], "resume_documents")

# Remove duplicates
unique_resumes = remove_duplicate_resumes("resume_documents")

# Parse resumes
fixed_resumes = parse_resumes(unique_resumes)

# Define job description
job_description = """
Looking for a Python Developer with experience in data analysis.
Required skills: Python, Pandas, NumPy, Data Cleaning, Data Visualization, SQL,
Machine Learning, Jupyter Notebook, Data Science.
"""

# Compute similarity
shortlisted = compute_similarity(job_description, fixed_resumes, 0.4)

# Display results
for res in shortlisted[:5]:
    print(f"📄 {res[0]} | Score: {res[1]:.4f} | Path: {res[2]}")
