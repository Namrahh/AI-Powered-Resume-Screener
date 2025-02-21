import os
import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv

# Load email credentials
load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
IMAP_SERVER = "imap.gmail.com"

def fetch_email_resumes():
    print("Connecting to email server...")
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")
        _, messages = mail.search(None, 'UNSEEN')
        message_ids = messages[0].split()

        resume_files = []
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
                        if filename:
                            filename = decode_header(filename)[0][0]
                            if isinstance(filename, bytes):
                                filename = filename.decode("utf-8")

                            filepath = os.path.join("resume_documents", filename)
                            with open(filepath, "wb") as f:
                                f.write(part.get_payload(decode=True))

                            print(f"Saved attachment: {filename}")
                            resume_files.append({"filename": filename, "filepath": filepath})

        mail.logout()
        return resume_files

    except Exception as e:
        print(f"Error: {e}")
        return []
