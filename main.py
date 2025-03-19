import gradio as gr
import os
import concurrent.futures
import shutil
import socket
from resume_parser import parse_resumes
from similarity import compute_similarity
from utils import remove_duplicate_resumes, save_uploaded_resumes, download_resumes_from_email

# 🔹 Define folder for shortlisted resumes
SHORTLISTED_FOLDER = "shortlisted_resumes"
os.makedirs(SHORTLISTED_FOLDER, exist_ok=True)  # Ensure the directory exists

# 🔹 Check if IMAP Port 993 is Open
def check_imap_port():
    test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = test_socket.connect_ex(("imap.gmail.com", 993))
    if result == 0:
        print("✅ Port 993 is Open")
    else:
        print("❌ Port 993 is Blocked")
    test_socket.close()

# 🔹 Save Shortlisted Resumes
def save_shortlisted_resumes(shortlisted, destination_folder=SHORTLISTED_FOLDER):
    """Save shortlisted resumes for downloading."""
    shortlisted_files = []
    for res in shortlisted:
        source_path = res["filepath"]
        destination_path = os.path.join(destination_folder, os.path.basename(source_path))
        shutil.copy(source_path, destination_path)
        shortlisted_files.append(destination_path)
    return shortlisted_files

# 🔹 Process Resumes
def process_resumes(email, password, job_description, uploaded_resumes):
    """Fetch, process, and shortlist resumes based on job description."""
    
    print("📩 Fetching resumes from email...")
    email_resumes = download_resumes_from_email(email, password)
    print(f"📥 {len(email_resumes)} resumes fetched from email.")

    print("📂 Saving uploaded resumes...")
    uploaded_paths = save_uploaded_resumes(uploaded_resumes)
    print(f"📂 {len(uploaded_paths)} resumes uploaded.")

    print("🔍 Removing duplicate resumes...")
    all_resumes = remove_duplicate_resumes(email_resumes + uploaded_paths)
    print(f"✅ {len(all_resumes)} unique resumes remain.")

    print("📊 Parsing resumes...")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        parsed_resumes = list(executor.map(parse_resumes, all_resumes))

    print("📈 Computing similarity scores...")
    shortlisted = compute_similarity(job_description, parsed_resumes, threshold=0.4)

    print(f"🏆 {len(shortlisted)} resumes shortlisted.")
    
    # 🔹 Save shortlisted resumes
    shortlisted_files = save_shortlisted_resumes(shortlisted)

    # 🔹 Return formatted shortlist & download links
    shortlist_text = [f"📄 {res['filename']} | Score: {res['score']:.4f}" for res in shortlisted[:5]]
    return shortlist_text, shortlisted_files  # Returns text & file paths for download

# 🎨 **UI with Gradio**
with gr.Blocks() as app:
    gr.Markdown("# 📄 AI-Powered Resume Screener")

    # 🔹 Email & Password Fields
    email_input = gr.Textbox(label="Enter Your Email", type="text", placeholder="example@gmail.com")
    password_input = gr.Textbox(label="Enter Your Email Password", type="password", placeholder="••••••••")

    # 🔹 Job Description Field
    job_description = gr.Textbox(label="Enter Job Description", lines=5)

    upload_button = gr.Files(
    label="Upload Resumes",
    file_types=[".pdf", ".doc", ".docx"], 
    interactive=True
)


    # 🔹 Process Button
    process_button = gr.Button("Process Resumes")

    # 🔹 Output Section
    output = gr.Textbox(label="Shortlisted Candidates", interactive=False)

    # 🔹 Download Button
    download_files = gr.File(label="📥 Download Shortlisted Resumes", interactive=True)

    # 🔹 Button Click Event
    process_button.click(
        process_resumes,  
        inputs=[email_input, password_input, job_description, upload_button],  
        outputs=[output, download_files]  # Downloads shortlisted resumes
    )

# 🚀 **Launch App**
if __name__ == "__main__":
    check_imap_port()  # Check IMAP port availability before launching
    app.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))


