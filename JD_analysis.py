
##Run ::  python3 JD_analysis.py --file_ext pdf --file_path sample1.pdf 


import io
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
import pandas as pd
#from pandas import ExcelWriter

# Docx resume
import docx2txt

#Wordcloud
import re
import operator
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords
set(stopwords.words('english'))
from wordcloud import WordCloud
from nltk.probability import FreqDist
import matplotlib.pyplot as plt
import xlsxwriter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import argparse


# construct argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-e", "--file_ext", type=str, required=True,
	help="please add file_ext")
ap.add_argument("-f", "--file_path", type=str, required=True,
	help="please add file path")
args = vars(ap.parse_args())


ext = args["file_ext"]
file_path  = args["file_path"]

def read_pdf_resume(pdf_doc):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    
    with open(pdf_doc, 'rb') as fh:
        for page in PDFPage.get_pages(fh, 
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
            
        text = fake_file_handle.getvalue()
    
    # close open handles
    converter.close()
    fake_file_handle.close()
    
    if text:
        return text

def read_word_resume(word_doc):
    #resume = docx2txt.process(word_doc)
    #text = ''.join(resume)
    resume = docx2txt.process(word_doc)
    resume = str(resume)
    #print(resume)
    text =  ''.join(resume)
    text = text.replace("\n", "")
    
    if text:
        return text
def clean_job_decsription(jd):
    ''' a function to create a word cloud based on the input text parameter'''
    ## Clean the Text
    # Lower
    clean_jd = jd.lower()
    # remove punctuation
    #clean_jd = re.sub(r'[^\w\s]', '', clean_jd)
    # remove trailing spaces
    clean_jd = clean_jd.strip()
    # remove numbers
    clean_jd = re.sub('[0-9]+', '', clean_jd)
    # tokenize 
    clean_jd = word_tokenize(clean_jd)
    # remove stop words
    stop = stopwords.words('english')
    #stop.extend(["AT_USER","URL","rt","corona","coronavirus","covid","amp","new","th","along","icai","would","today","asks"])
    clean_jd = [w for w in clean_jd if not w in stop] 
    
    return(clean_jd)

"""
def create_word_cloud(jd):
    corpus = jd
    fdist = FreqDist(corpus)
    #print(fdist.most_common(100))
    words = ' '.join(corpus)
    words = words.split()

    # create a empty dictionary
    data = dict()
    #  Get frequency for each words where word is the key and the count is the value
    for word in (words):
        word = word.lower()
        data[word] = data.get(word, 0) + 1
    # Sort the dictionary in reverse order to print first the most used terms    
    dict(sorted(data.items(), key=operator.itemgetter(1),reverse=True))
    word_cloud = WordCloud(width = 800, height = 800, background_color ='white',max_words = 500)
    word_cloud.generate_from_frequencies(data)
    # plot the WordCloud image                        
    plt.figure(figsize = (10, 8), edgecolor = 'k') 
    plt.imshow(word_cloud,interpolation = 'bilinear') 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 
    plt.show()
"""
"""
def get_resume_score(text):
    cv = CountVectorizer(stop_words='english')
    count_matrix = cv.fit_transform(text)
    #Print the similarity scores
    print("\nSimilarity Scores:")
    #print(cosine_similarity(count_matrix))
    #get the match percentage
    matchPercentage = cosine_similarity(count_matrix)[0][1] * 100
    matchPercentage = round(matchPercentage, 2) # round to two decimal
    print("Your resume matches about "+ str(matchPercentage)+ "% of the job description.")
"""


if __name__ == '__main__':
    
    workbook = xlsxwriter.Workbook('output.xlsx')
    worksheet = workbook.add_worksheet()  
    
    row = 1
    column = 0
    rows = 1
    rowsQ = 1

    
    title = ['Skills', 'Qualification', 'Roles']

    #extn = input("Enter File Extension: ")
    #print(extn)
    if ext == "pdf":
        job_description = read_pdf_resume(file_path)
    else:
        job_description = read_word_resume(file_path)
    #print(job_description)
    
    #job_description = input("\nEnter the Job Description: ")

    ## Get a Keywords Cloud
    clean_jd = clean_job_decsription(job_description)
    #print(clean_jd)

    ## read csv
    skills = pd.read_csv("JD_anlaysis/skills.csv")
    roles = pd.read_csv("JD_anlaysis/roles.csv")
    qualification = pd.read_csv("JD_anlaysis/qualification.csv")
    
    j = 0
    #print(clean_jd)
    #worksheet.write(0,j,title[j])
    for a in title:
        worksheet.write(0,j,title[j])
        j = j + 1
    # iterating through content list
    for item in clean_jd :

        if item in skills:
            #print(item) 
            # write operation perform
            worksheet.write(row, column, item)
  
            # incrementing the value of row by one
            # with each iteratons.
            row += 1
        
        if item in roles:
            #print(item.lower) 
            # write operation perform
            worksheet.write(rows, 1, item)
            # incrementing the value of row by one
            # with each iteratons.
            rows += 1

        if item in qualification:
            #print(item.lower) 
            # write operation perform
            worksheet.write(rowsQ, 2, item)
            # incrementing the value of row by one
            # with each iteratons.
            rowsQ += 1

    workbook.close()
    #create_word_cloud(clean_jd)
    
    
   # text = [resume, job_description]
    
    ## Get a Match
   ## get_resume_score(text)
