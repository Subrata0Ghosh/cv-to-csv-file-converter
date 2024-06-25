import os
import pandas as pd
from PyPDF2 import PdfReader
from docx import Document
from flask import Flask, render_template, request, send_file
import skills  # Import skills list from skills.py
import re

app = Flask(__name__)

def extract_info_from_cv(text):
    # Regular expressions to extract information
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'\b(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})\b'
    experience_pattern = r'Experience[:\-]?(.*?)\n'
    
    # Extract skills based on keyword matching
    skills_matched = []
    for skill in skills.skills_list:
        if re.search(r'\b{}\b'.format(skill), text, re.IGNORECASE):
            skills_matched.append(skill)

    # Additional fields
    name_pattern = r'(?i)(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)(?:\s*[:-]\s*)(.*?)\n'
    education_pattern = r'Education[:\-]?(.*?)\n'
    certifications_pattern = r'Certifications[:\-]?(.*?)\n'
    languages_pattern = r'Languages[:\-]?(.*?)\n'
    projects_pattern = r'Projects[:\-]?(.*?)\n'
    achievements_pattern = r'Achievements[:\-]?(.*?)\n'
    linkedin_pattern = r'LinkedIn[:\-]?(.*?)\n'
    github_pattern = r'GitHub[:\-]?(.*?)\n'
    references_pattern = r'References[:\-]?(.*?)\n'
    cover_letter_pattern = r'Cover\s*Letter[:\-]?(.*?)\n'

    # Extract information
    emails = re.findall(email_pattern, text)
    phones = [''.join(phone) for phone in re.findall(phone_pattern, text)]
    name = re.search(name_pattern, text).group(1).strip() if re.search(name_pattern, text) else ""
    experience = re.search(experience_pattern, text, re.IGNORECASE).group(1).strip() if re.search(experience_pattern, text, re.IGNORECASE) else ""
    education = re.search(education_pattern, text, re.IGNORECASE).group(1).strip() if re.search(education_pattern, text, re.IGNORECASE) else ""
    certifications = re.search(certifications_pattern, text, re.IGNORECASE).group(1).strip() if re.search(certifications_pattern, text, re.IGNORECASE) else ""
    languages = re.search(languages_pattern, text, re.IGNORECASE).group(1).strip() if re.search(languages_pattern, text, re.IGNORECASE) else ""
    projects = re.search(projects_pattern, text, re.IGNORECASE).group(1).strip() if re.search(projects_pattern, text, re.IGNORECASE) else ""
    achievements = re.search(achievements_pattern, text, re.IGNORECASE).group(1).strip() if re.search(achievements_pattern, text, re.IGNORECASE) else ""
    linkedin_profile = re.search(linkedin_pattern, text, re.IGNORECASE).group(1).strip() if re.search(linkedin_pattern, text, re.IGNORECASE) else ""
    github_profile = re.search(github_pattern, text, re.IGNORECASE).group(1).strip() if re.search(github_pattern, text, re.IGNORECASE) else ""
    references = re.search(references_pattern, text, re.IGNORECASE).group(1).strip() if re.search(references_pattern, text, re.IGNORECASE) else ""
    cover_letter = re.search(cover_letter_pattern, text, re.IGNORECASE).group(1).strip() if re.search(cover_letter_pattern, text, re.IGNORECASE) else ""
    
    # Calculate resume score based on skills and experience
    resume_score = len(skills_matched) * 10 + int(experience) if experience.isdigit() else len(skills_matched) * 10

    return {
        # 'Name': name,
        'Email': emails[0] if emails else "",
        'Phone': ', '.join(phones),
        'Experience': experience,
        'Skills': ', '.join(skills_matched),
        'Education': education,
        'Certifications': certifications,
        'Languages': languages,
        'Projects': projects,
        'Achievements': achievements,
        'LinkedIn_Profile': linkedin_profile,
        'GitHub_Profile': github_profile,
        'References': references,
        'Cover_Letter': cover_letter,
        'Resume_Score': resume_score
    }

def read_docx(file_path):
    text = ""
    doc = Document(file_path)
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text

def read_cv(file_path):
    _, file_extension = os.path.splitext(file_path)
    if file_extension == '.pdf':
        with open(file_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            text = ''
            for page in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page].extract_text()
    elif file_extension == '.docx':
        text = read_docx(file_path)
    else:
        text = ''
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part'
    files = request.files.getlist('file')  # Retrieve all uploaded files
    if not files:
        return 'No selected file'
    
    all_cv_info = []
    for file in files:
        if file.filename == '':
            return 'No selected file'
        if file:
            folder_path = 'uploads'
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            file_path = os.path.join(folder_path, file.filename)
            file.save(file_path)
            cv_text = read_cv(file_path)
            cv_info = extract_info_from_cv(cv_text)
            cv_info['File_Name'] = file.filename  # Add file name to extracted info
            all_cv_info.append(cv_info)
    
    df = pd.DataFrame(all_cv_info)
    output_file_path = 'output/all_cv_info.xlsx'
    df.to_excel(output_file_path, index=False)
    return send_file(output_file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
