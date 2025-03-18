import os
import imaplib
import email
from dotenv import load_dotenv

# Load credentials
load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
IMAP_SERVER = "imap.gmail.com"

SAVE_FOLDER = "resume_documents"

def fetch_email_resumes():
    """Fetch resume attachments from unread emails."""
    
    # 🚨 Debugging: Check if email variables are loaded
    print(f"🔍 EMAIL_USER: {EMAIL_USER}")
    print(f"🔍 EMAIL_PASS: {EMAIL_PASS}")

    if not EMAIL_USER or not EMAIL_PASS:
        print("❌ EMAIL_USER or EMAIL_PASS is missing! Check your .env file.")
        return []

    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)

    resume_files = []
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")

        _, messages = mail.search(None, 'UNSEEN')
        message_ids = messages[0].split()

        if not message_ids:
            print("🚫 No unread emails with resumes found.")
        else:
            for msg_id in message_ids:
                _, msg_data = mail.fetch(msg_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        for part in msg.walk():
                            if part.get_content_maintype() == "multipart":
                                continue
                            if part.get("Content-Disposition") is None:
                                continue

                            filename = part.get_filename()
                            if filename and filename.lower().endswith((".pdf", ".doc", ".docx")):
                                filepath = os.path.join(SAVE_FOLDER, filename)

                                with open(filepath, "wb") as f:
                                    f.write(part.get_payload(decode=True))

                                print(f"✅ Saved resume: {filename}")
                                resume_files.append(filepath)

        mail.logout()
    except Exception as e:
        print(f"❌ Error fetching emails: {e}")

    return resume_files
