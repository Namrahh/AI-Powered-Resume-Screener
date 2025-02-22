import os
from utils import extract_resume_text

def parse_resumes(file_paths):
    """Extract text from resumes and return structured data."""
    resumes = []

    for file_path in file_paths:
        text = extract_resume_text(file_path)

        if not text:
            print(f"⚠️ No text extracted from {file_path}. Skipping.")
            continue

        resume_data = {
            "filename": os.path.basename(file_path),
            "text": text,
            "filepath": file_path
        }

        resumes.append(resume_data)

    return resumes
