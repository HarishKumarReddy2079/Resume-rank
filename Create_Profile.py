
## Needed Libraries
from gensim.models import Word2Vec
import PyPDF2
import os
import collections
from os import listdir
from os.path import isfile, join
from io import StringIO
import pandas as pd
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()
from spacy.matcher import PhraseMatcher
import docx2txt
from pyresparser import ResumeParser
#import spacy
#nlp = spacy.load("en_core_web_sm")


# Function to read resumes from the folder one by one
def pdfextract(file):
    fileReader = PyPDF2.PdfFileReader(open(file,'rb'))
    countpage = fileReader.getNumPages()
    count = 0
    text = []
    while count < countpage:    
        pageObj = fileReader.getPage(count)
        count +=1
        t = pageObj.extractText()
        text.append(t)
    return text

def create_profile(file,new_keyword_data,new_keyword_dict):

#def create_profile(file,new_keyword_skill,new_keyword_qualification,new_keyword_pastcompany,new_keyword_role):
   # modelSkill=Word2Vec.load("../TrainModel/Skill.model")
   # modelQualification=Word2Vec.load("../TrainModel/Qualification.model")
   # modelPastcompany=Word2Vec.load("../TrainModel/Pastcompany.model")
    text = ''
    
    if file.endswith('.pdf'):
      text = pdfextract(file) 
      text = str(text)
      text = text.replace("\\n", "")
      text = text.lower()
      resume_data = ResumeParser(file).get_extracted_data()
      experience = resume_data['total_experience']

    if file.endswith('.docx'):
      text = docx2txt.process(file)
      text = str(text)
      text = text.replace("\\n", "")
      text = text.lower()
      resume_data = ResumeParser(file).get_extracted_data()
      experience = resume_data['total_experience']

    matcher = PhraseMatcher(nlp.vocab)

    print(new_keyword_dict)
   # for key, value in new_keyword_dict:
   #    print(key)
   #     print(new_keyword_dict)



    for key in new_keyword_dict:
        if len(new_keyword_dict[key]) == 1:
            modelSkill=Word2Vec.load("../TrainModel/"+key+".model")

            Skill = [nlp(text[0]) for text in modelSkill.wv.most_similar(new_keyword_dict[key])]
        else:
            skill_path = open("../Preprocess-JD/"+key+".txt", "rt")
            data = skill_path.read()
            words = data.split()
            skill_words = [] 
            for word in words:
                word = word.lower()
                skill_words.append(word)
                Skill = [nlp(text) for text in skill_words]

        matcher.add(key, None, *Skill)


    ## Skill
   # if len(new_keyword_skill) == 1:
   #     Skill = [nlp(text[0]) for text in modelSkill.wv.most_similar(new_keyword_skill)]

   # else:
   #     skill_path = open("../Preprocess-JD/Skill.txt", "rt")
   #     data = skill_path.read()
    #    words = data.split()
    #    skill_words = [] 
    #    for word in words:
    #        word = word.lower()
    #        skill_words.append(word)
    #    Skill = [nlp(text) for text in skill_words]

    ## Qualification
    #if len(new_keyword_qualification) == 1:
    #    Qualification = [nlp(text[0]) for text in modelQualification.wv.most_similar(new_keyword_qualification)]
    #else:
    #    qualification_path = open("../Preprocess-JD/Qualification.txt", "rt")
    #    data = qualification_path.read()
    #    words = data.split()
    #    qualification_words = [] 
    #    for word in words:
    #        word = word.lower()
    #        qualification_words.append(word)
    #    Qualification = [nlp(text) for text in qualification_words]



    ## Past Company
   # if len(new_keyword_pastcompany) == 1:
    #    Pastcompany = [nlp(text[0]) for text in modelPastcompany.wv.most_similar(new_keyword_pastcompany)]
    #else:
    #    company_path = open("../Preprocess-JD/Pastcompany.txt", "rt")
    #    data = company_path.read()
    #    words = data.split()
    #    company_words = [] 
    #    for word in words:
    #        word = word.lower()
    #        company_words.append(word)
    #    Pastcompany = [nlp(text) for text in company_words]

    # Role

    #role_path = open("../Preprocess-JD/Role.txt", "rt")
    #data = role_path.read()
    #words = data.split()
    #role_words = [] 
    #for word in words:
    #    word = word.lower()
    #    role_words.append(word)
    #Role = [nlp(text) for text in role_words]

   # matcher = PhraseMatcher(nlp.vocab)
  
   # matcher.add('Skill', None, *Skill)
   # matcher.add('Qualification', None, *Qualification)
   # matcher.add('Pastcompany', None, *Pastcompany)
   # matcher.add('Role', None, *Role)


    doc = nlp(text)

    d = []  
    matches = matcher(doc)
    for match_id, start, end in matches:
        rule_id = nlp.vocab.strings[match_id]  # get the unicode I

        span = doc[start : end]               # get the matched slice of the doc

        d.append((rule_id, span.text))      
    keywords = "\n".join(f'{i[0]} {i[1]} ({j})' for i,j in Counter(d).items())
    
    
    ## convertimg string of keywords to dataframe
    df = pd.read_csv(StringIO(keywords),names = ['Keywords_List'])
    df1 = pd.DataFrame(df.Keywords_List.str.split(' ',1).tolist(),columns = ['Subject','Keyword'])
    df2 = pd.DataFrame(df1.Keyword.str.split('(',1).tolist(),columns = ['Keyword', 'Count'])
    df3 = pd.concat([df1['Subject'],df2['Keyword'], df2['Count']], axis =1) 
    df3['Count'] = df3['Count'].apply(lambda x: x.rstrip(")"))
    

    base = os.path.basename(file)
    filename = os.path.splitext(base)[0]
    
       
    name = filename.split('_')
    name2 = name[0]
    name2 = name2.lower()
    name3 = pd.read_csv(StringIO(name2),names = ['Candidate Name'])
    
    dataf = pd.concat([name3['Candidate Name'], df3['Subject'], df3['Keyword'], df3['Count']], axis = 1)
    dataf['Candidate Name'].fillna(dataf['Candidate Name'].iloc[0], inplace = True)
    return(dataf,experience,name2)

