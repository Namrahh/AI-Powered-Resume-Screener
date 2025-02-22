from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def preprocess_text(text):
    """Clean and normalize text."""
    return " ".join(str(text).split()).strip()

def compute_similarity(job_desc, resumes, threshold=0.4):
    """Compute similarity between job description and resumes."""
    if not resumes:
        print("⚠️ No resumes found for similarity check!")
        return []

    job_desc = preprocess_text(job_desc)
    job_embedding = model.encode(job_desc, convert_to_tensor=True)
    results = []

    for resume in resumes:
        filename = resume.get("filename", "Unknown")
        resume_text = preprocess_text(resume.get("text", ""))
        filepath = resume.get("filepath", "")

        if not resume_text:
            continue

        resume_embedding = model.encode(resume_text, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(job_embedding, resume_embedding).item()

        results.append((filename, similarity, filepath))

    shortlisted = [res for res in results if res[1] > threshold]
    return sorted(shortlisted, key=lambda x: x[1], reverse=True)
