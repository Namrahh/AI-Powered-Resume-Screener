import os
import pdfplumber
import docx
import hashlib
import shutil

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
    return text.strip()

def extract_text_from_docx(docx_path):
    """Extract text from a DOCX file."""
    doc = docx.Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs]).strip()

def extract_resume_text(file_path):
    """Determine file type and extract text accordingly."""
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    return None

def remove_duplicate_resumes(folder_path="resume_documents"):
    """Remove duplicate resume files based on content hash."""
    unique_files = {}
    duplicate_files = []

    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)

        with open(filepath, "rb") as f:
            file_hash = hashlib.md5(f.read()).hexdigest()

        if file_hash not in unique_files:
            unique_files[file_hash] = filepath
        else:
            duplicate_files.append(filepath)

    for dup_file in duplicate_files:
        os.remove(dup_file)
        print(f"🗑 Deleted duplicate: {dup_file}")

    print(f"✅ Total unique resumes: {len(unique_files)}")
    return list(unique_files.values())

def merge_resumes(source_folders, destination_folder):
    """Merge resumes from multiple folders into one."""
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for source_folder in source_folders:
        if os.path.exists(source_folder):
            for filename in os.listdir(source_folder):
                source_path = os.path.join(source_folder, filename)
                destination_path = os.path.join(destination_folder, filename)

                if not os.path.exists(destination_path):
                    shutil.copy(source_path, destination_path)
                    print(f"✅ Merged: {filename}")
                else:
                    print(f"⚠️ Duplicate skipped: {filename}")
def save_uploaded_resumes(uploaded_files, save_dir="resume_documents"):
    """Save uploaded resumes to a directory."""
    os.makedirs(save_dir, exist_ok=True)
    
    saved_paths = []
    for uploaded_file in uploaded_files:
        file_path = os.path.join(save_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(uploaded_file, f)
        saved_paths.append(file_path)
    
    return saved_paths
