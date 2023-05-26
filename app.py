from flask import Flask, render_template, request
import re
import pickle
from PyPDF2 import PdfReader
import pdfplumber
from docx import Document
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer

app = Flask(__name__)

def cleanResume(resumeText):
    resumeText = re.sub('http\S+\s*', ' ', resumeText)
    resumeText = re.sub('RT|cc', ' ', resumeText)
    resumeText = re.sub('#\S+', '', resumeText)
    resumeText = re.sub('@\S+', '  ', resumeText)
    resumeText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', resumeText)
    resumeText = re.sub(r'[^\x00-\x7f]',r' ', resumeText)
    resumeText = re.sub('\s+', ' ', resumeText)
    return resumeText

def preprocess_resume(file_path):
    file_extension = file_path.split('.')[-1].lower()
    resume_text = ""

    if file_extension == 'pdf':
        with open(file_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            num_pages = len(pdf_reader.pages)

            for page_number in range(num_pages):
                page = pdf_reader.pages[page_number]
                text = page.extract_text()
                resume_text += text

    elif file_extension == 'doc' or file_extension == 'docx':
        document = Document(file_path)
        paragraphs = document.paragraphs

        for paragraph in paragraphs:
            text = paragraph.text
            resume_text += text

    elif file_extension == 'txt':
        with open(file_path, 'r', encoding='utf-8') as file:
            resume_text = file.read()

    return resume_text

with open('clf.pkl', 'rb') as file:
    clf = pickle.load(file)

with open('wv.pkl', 'rb') as file:
    word_vectorizer = pickle.load(file)

with open('le.pkl', 'rb') as file:
    le = pickle.load(file)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['resume']
        resume_text = file.read().decode('utf-8')
        predicted_category = predict_category(resume_text)
        return render_template('index.html', predicted_category=predicted_category)
    return render_template('index.html')

def predict_category(resume_text):
    cleaned_resume = cleanResume(resume_text)
    features = word_vectorizer.transform([cleaned_resume])
    prediction = clf.predict(features)
    predicted_category = le.inverse_transform(prediction)
    return predicted_category[0]

if __name__ == '__main__':
    app.run()

