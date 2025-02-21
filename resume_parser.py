import pdfplumber
import docx

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()

def extract_resume_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    return None

def parse_resumes(file_paths):
    """Extract text from resumes and return structured data."""
    resumes = []
    
    for file_path in file_paths:
        text = extract_resume_text(file_path)  # Extract text
        
        if not text:  # Skip if text extraction fails
            print(f"⚠️ No text extracted from {file_path}. Skipping.")
            continue
        
        resume_data = {
            "filename": file_path.split("/")[-1],  # Extract filename
            "text": text,  # Extracted text
            "filepath": file_path  # Original file path
        }
        
        resumes.append(resume_data)
    
    return resumes
