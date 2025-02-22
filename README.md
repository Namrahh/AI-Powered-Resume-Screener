# AI-Powered-Resume-Screener
An automated resume screening tool that parses resumes, matches them against job descriptions, and shortlists candidates based on relevance. It leverages LLMs, sentence-transformers, and Gradio for an interactive interface.

## Overview
This project is an **AI-powered resume screening tool** that automates the process of shortlisting candidates based on job descriptions. It uses **Natural Language Processing (NLP)** and **machine learning** to extract information from resumes, compute semantic similarity, and rank candidates. The system is designed to improve the efficiency and fairness of the hiring process by reducing manual effort and minimizing human bias.

## Features
✅ Resume Parsing – Extracts text from PDFs and DOCX files using pdfplumber and docx
✅ Automated Email Integration – Fetches resumes from an email inbox (Gmail IMAP)
✅ Similarity Scoring – Uses sentence-transformers to rank resumes based on job descriptions
✅ Duplicate Removal – Ensures unique resumes are processed
✅ Download Shortlisted Resumes – Provides only the most relevant CVs
✅ User Interface – Gradio-based interface for easy interaction

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Namrahh/AI-Powered-Resume-Screener.git
   cd AI-Resume-Screener

# Install Dependencies:
Install the required Python packages:
pip install -r requirements.txt

# Download Pre-trained Models:
Download the all-MiniLM-L6-v2 model for semantic similarity:
python -m sentence_transformers download all-MiniLM-L6-v2

# Download spaCy Model:
Download the spaCy model for text processing:
python -m spacy download en_core_web_sm

# Usage
1. Run the Gradio App:
Start the Gradio interface:
python app/main.py

2. Access the UI:
Open the provided link in your browser to access the AI Resume Screener UI.

3. Upload Resumes and Job Descriptions:

Enter a job description in the text box.

Upload resumes in PDF or DOCX format.

View the ranked results based on semantic similarity.

4. Fetch Resumes from Email

# Dependencies
The project requires the following Python packages:

Python 3.8+: The project is built using Python 3.8 or higher.

# Libraries:

gradio: For building the user interface.

sentence-transformers: For computing semantic similarity.

pdfplumber: For extracting text from PDF files.

python-docx: For extracting text from DOCX files.

pandas: For data manipulation (if needed).

scikit-learn: For machine learning utilities (if needed).

torch: For deep learning (required by sentence-transformers).

python-dotenv: For loading environment variables from .env.

spacy: For advanced text processing.

All dependencies are listed in the requirements.txt file. You can install them using:
pip install -r requirements.txt

# Contributing
Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.

2. Create a new branch for your feature or bugfix.

3. Commit your changes.

4. Submit a pull request.

# License
This project is licensed under the MIT License. See the LICENSE file for details.

# Future Improvements
- Multilingual Support: Extend the system to support resumes in multiple languages.

- Advanced Resume Parsing: Integrate OCR for scanned resumes and handwritten documents.

- Bias Reduction: Implement techniques to mitigate biases related to gender, ethnicity, and age.

- ATS Integration: Enable seamless integration with Applicant Tracking Systems (ATS).

- Real-Time Feedback: Provide candidates with AI-driven insights on resume optimization.

# Contact
For questions or feedback, please contact:

Your Name: namraaftab8@gmail.com

GitHub: Namrahh
