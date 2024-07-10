# Resume Analyzer and Organizer

## Project Overview

Resume Analyzer and Organizer is a web application that processes resumes (CVs) in PDF and DOCX formats. It extracts relevant information, evaluates the resumes based on certain criteria, and compiles the extracted data into an Excel file. This tool streamlines candidate evaluation for recruiters by organizing key details from multiple resumes into an easy-to-review format.

## Features

- **File Upload**: Upload multiple resumes in PDF or DOCX format.
- **Resume Parsing**: Extracts email, phone number, experience, skills, education, certifications, languages, projects, achievements, LinkedIn profile, GitHub profile, references, and cover letter.
- **Skills Matching**: Matches skills mentioned in the resume against a predefined list of skills.
- **Resume Scoring**: Calculates a resume score based on the number of matched skills and years of experience.
- **Excel Export**: Compiles extracted information into an Excel file for easy review and analysis.
- **File Management**: Handles file uploads and ensures temporary files are deleted after processing.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/resume-analyzer-organizer.git
   cd resume-analyzer-organizer
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `skills.py`**:
   Create a `skills.py` file in the root directory with a list of skills to be matched. For example:
   ```python
   skills_list = ['Python', 'JavaScript', 'HTML', 'CSS', 'SQL']
   ```

## Usage

1. **Run the Application**:
   ```bash
   flask run
   ```

2. **Access the Application**:
   Open your web browser and go to `http://127.0.0.1:5000/`.

3. **Upload Resumes**:
   Upload one or multiple resume files in PDF or DOCX format.

4. **Download Extracted Data**:
   After processing, download the generated Excel file containing all the extracted information.

## Project Structure

- `app.py`: Main application file containing routes and processing logic.
- `templates/`: Folder containing HTML templates.
  - `index.html`: Main page for uploading resumes.
- `uploads/`: Folder for storing uploaded resumes (created at runtime).
- `output/`: Folder for storing the generated Excel file (created at runtime).
- `requirements.txt`: List of dependencies required for the project.
- `skills.py`: Contains the list of skills to be matched (to be created).

## Dependencies

- Flask
- pandas
- PyPDF2
- python-docx
- openpyxl (for Excel file generation)

Install these dependencies via pip:
```bash
pip install Flask pandas PyPDF2 python-docx openpyxl
```

## License

This project is licensed under the MIT License.

## Acknowledgments

Special thanks to the developers of Flask, pandas, PyPDF2, and python-docx for their excellent libraries.
