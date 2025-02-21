from sentence_transformers import SentenceTransformer, util

# Load Sentence Transformer Model
model = SentenceTransformer('all-MiniLM-L6-v2')

def preprocess_text(text):
    """Preprocess text by removing extra spaces and newlines."""
    return " ".join(str(text).split()).strip()  # Ensure it's a string

def compute_similarity(job_desc, resumes, threshold=0.1):
    """Compute similarity between a job description and resumes."""
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
            print(f"⚠️ Empty text for {filename}! Skipping.")
            continue
        
        resume_embedding = model.encode(resume_text, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(job_embedding, resume_embedding).item()
        
        results.append((filename, similarity, filepath))

    # Debugging: Print all similarity scores
    print("\n🔍 All Similarity Scores (Before Filtering):")
    for res in results:
        print(f"{res[0]} - Similarity: {res[1]:.4f}")

    # Apply threshold filtering
    shortlisted = [res for res in results if res[1] > threshold]
    
    if not shortlisted:
        print("🚨 No resumes met the similarity threshold!")

    return shortlisted
