# -*- coding: utf-8 -*-
"""Resume_Screening.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OdVUXiS56RMxNLKZeJJdB2UhKxY3Iw7N
"""

import numpy as np

import pandas as pd

import matplotlib.pyplot as plt

import warnings

warnings.filterwarnings('ignore')

from sklearn.naive_bayes import MultinomialNB

from sklearn.multiclass import OneVsRestClassifier

from sklearn import metrics

from sklearn.metrics import accuracy_score

from pandas.plotting import scatter_matrix

from sklearn.neighbors import KNeighborsClassifier

from sklearn import metrics

resumeDataSet = pd.read_csv('resume_dataset.csv' ,encoding='utf-8')
resumeDataSet['cleaned_resume'] = ''
resumeDataSet.head()

print ("Displaying the distinct categories of resume -")
print (resumeDataSet['Category'].unique())

print ("Displaying the distinct categories of resume and the number of records belonging to each category -")
print (resumeDataSet['Category'].value_counts())

import seaborn as sns

plt.figure(figsize=(15,15))
plt.xticks(rotation=90)
sns.countplot(y="Category", data=resumeDataSet)

from matplotlib.gridspec import GridSpec

targetCounts = resumeDataSet['Category'].value_counts()
targetLabels  = resumeDataSet['Category'].unique()
# Make square figures and axes
plt.figure(1, figsize=(25,25))
the_grid = GridSpec(2, 2)


cmap = plt.get_cmap('coolwarm')
colors = [cmap(i) for i in np.linspace(0, 1, 6)]
plt.subplot(the_grid[0, 1], aspect=1, title='CATEGORY DISTRIBUTION')

source_pie = plt.pie(targetCounts, labels=targetLabels, autopct='%1.1f%%', shadow=True, colors=colors)
plt.show()

import re
def cleanResume(resumeText):
    resumeText = re.sub('http\S+\s*', ' ', resumeText)  # remove URLs
    resumeText = re.sub('RT|cc', ' ', resumeText)  # remove RT and cc
    resumeText = re.sub('#\S+', '', resumeText)  # remove hashtags
    resumeText = re.sub('@\S+', '  ', resumeText)  # remove mentions
    resumeText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', resumeText)  # remove punctuations
    resumeText = re.sub(r'[^\x00-\x7f]',r' ', resumeText) 
    resumeText = re.sub('\s+', ' ', resumeText)  # remove extra whitespace
    return resumeText
    
resumeDataSet['cleaned_resume'] = resumeDataSet.Resume.apply(lambda x: cleanResume(x))

import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
import string
from wordcloud import WordCloud

oneSetOfStopWords = set(stopwords.words('english')+['``',"''"])
totalWords =[]
Sentences = resumeDataSet['Resume'].values
cleanedSentences = ""
for i in range(0,160):
    cleanedText = cleanResume(Sentences[i])
    cleanedSentences += cleanedText
    requiredWords = nltk.word_tokenize(cleanedText)
    for word in requiredWords:
        if word not in oneSetOfStopWords and word not in string.punctuation:
            totalWords.append(word)
    
wordfreqdist = nltk.FreqDist(totalWords)
mostcommon = wordfreqdist.most_common(50)
print(mostcommon)

wc = WordCloud().generate(cleanedSentences)
plt.figure(figsize=(15,15))
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.show()

from sklearn.preprocessing import LabelEncoder

var_mod = ['Category']
le = LabelEncoder()
for i in var_mod:
    resumeDataSet[i] = le.fit_transform(resumeDataSet[i])

import pickle
pickle.dump(le,open("le.pkl",'wb'))

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack

requiredText = resumeDataSet['cleaned_resume'].values
requiredTarget = resumeDataSet['Category'].values

word_vectorizer = TfidfVectorizer(
    sublinear_tf=True,
    stop_words='english',
    max_features=1500)
word_vectorizer.fit(requiredText)
WordFeatures = word_vectorizer.transform(requiredText)

print ("Feature completed .....")

X_train,X_test,y_train,y_test = train_test_split(WordFeatures,requiredTarget,random_state=0, test_size=0.2)
print(X_train.shape)
print(X_test.shape)

import pickle
pickle.dump(word_vectorizer,open("wv.pkl",'wb'))

clf = OneVsRestClassifier(KNeighborsClassifier())
clf.fit(X_train, y_train)
prediction = clf.predict(X_test)
print('Accuracy of KNeighbors Classifier on training set: {:.2f}'.format(clf.score(X_train, y_train)))
print('Accuracy of KNeighbors Classifier on test set: {:.2f}'.format(clf.score(X_test, y_test)))

print("\n Classification report for classifier %s:\n%s\n" % (clf, metrics.classification_report(y_test, prediction)))

import pickle
pickle.dump(clf,open('clf.pkl','wb'))

!pip install PyPDF2 pdfplumber python-docx

import re
import pickle
from PyPDF2 import PdfReader
import pdfplumber
from docx import Document
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer

def cleanResume(resumeText):
    resumeText = re.sub('http\S+\s*', ' ', resumeText)
    resumeText = re.sub('RT|cc', ' ', resumeText)
    resumeText = re.sub('#\S+', '', resumeText)
    resumeText = re.sub('@\S+', '  ', resumeText)
    resumeText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', resumeText)
    resumeText = re.sub(r'[^\x00-\x7f]',r' ', resumeText)
    resumeText = re.sub('\s+', ' ', resumeText)
    return resumeText

# Preprocess the new resume file
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

# Load the trained model and vectorizer
with open('clf.pkl', 'rb') as file:
    clf = pickle.load(file)

with open('wv.pkl', 'rb') as file:
    word_vectorizer = pickle.load(file)

with open('le.pkl', 'rb') as file:
    le = pickle.load(file)

# Preprocess the new resume and make predictions
def predict_category(resume_text):
    cleaned_resume = cleanResume(resume_text)
    features = word_vectorizer.transform([cleaned_resume])
    prediction = clf.predict(features)
    predicted_category = le.inverse_transform(prediction)
    return predicted_category[0]

# Example usage
new_resume_text = preprocess_resume('resume.pdf')
predicted_category = predict_category(new_resume_text)
print("Predicted category:", predicted_category)