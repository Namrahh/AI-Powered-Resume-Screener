# AI-Powered-Resume-Screener
An AI-powered resume screening tool using NLP and machine learning.

# AI-Powered Resume Screener

## Overview
This project is an **AI-powered resume screening tool** that automates the process of shortlisting candidates based on job descriptions. It uses **Natural Language Processing (NLP)** and **machine learning** to extract information from resumes, compute semantic similarity, and rank candidates. The system is designed to improve the efficiency and fairness of the hiring process by reducing manual effort and minimizing human bias.

## Features
- **Resume Parsing**: Extracts text from resumes in PDF and DOCX formats.
- **Job Description Matching**: Computes semantic similarity between resumes and job descriptions.
- **Gradio UI**: Provides an interactive interface for uploading resumes and viewing results.
- **Email Integration**: Fetches resumes directly from email attachments.
- **Scalable**: Handles a large volume of resumes efficiently.

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Namrahh/AI-Powered-Resume-Screener.git
   cd AI-Resume-Screener

Install Dependencies:
Install the required Python packages:
pip install -r requirements.txt

Download Pre-trained Models:
Download the all-MiniLM-L6-v2 model for semantic similarity:
python -m sentence_transformers download all-MiniLM-L6-v2

Download spaCy Model:
Download the spaCy model for text processing:
python -m spacy download en_core_web_sm
