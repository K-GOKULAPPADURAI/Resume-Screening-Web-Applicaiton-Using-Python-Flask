# Resume-Screening-Web-Applicaiton-Using-Python-Flask

# Resume Screening Web Application

The Resume Screening web application is a Flask-based application that predicts the category of a given resume file. It supports PDF, DOCX, and TXT formats for resume files. The application uses pre-trained models to classify the resumes into different categories.

## Features

- Upload a resume file in PDF, DOCX, or TXT format.
- Predict the category of the uploaded resume.
- Display the predicted category on the same page.
- Supports multiple file formats for resume upload.

## Prerequisites

- Python 3.10.11 or 3.10.x

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/K-GOKULAPPADURAI/Resume-Screening-Web-Applicaiton-Using-Python-Flask
   
   ```
Install the required dependencies:

```
pip install -r requirements.txt
```

The above command will install Flask, PyPDF2, pdfplumber, python-docx, and scikit-learn packages.

Usage
Place the pre-trained model files (model.pkl, vectorizer.pkl, and label_encoder.pkl) in the same directory as app.py.

Run the Flask application:

```
python app.py
```
Access the application in your web browser at http://localhost:5000.

Select a resume file (in PDF, DOCX, or TXT format) using the "Choose File" button.

Click the "Predict" button to initiate the prediction process.

The predicted category of the resume will be displayed on the same page.

File Structure
app.py: The Flask application file containing the main code for the web application.
templates/index.html: The HTML template for the user interface.
model.pkl: The pre-trained machine learning model for resume classification.
vectorizer.pkl: The pre-trained TF-IDF vectorizer for feature extraction.
label_encoder.pkl: The pre-trained label encoder for category mapping.
Notes
Make sure the model files (model.pkl, vectorizer.pkl, and label_encoder.pkl) are present in the same directory as app.py.
The application supports resume files in PDF, DOCX, and TXT formats.
The application uses PyPDF2 and pdfplumber libraries for PDF file processing, python-docx library for DOCX file processing, and scikit-learn library for machine learning tasks.

Make sure to replace `<repository_url>` with the actual URL of your repository.




