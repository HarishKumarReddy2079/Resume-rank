
## Needed Libraries

import os
import pandas as pd
from pandas import DataFrame
import csv
from Ranking_algo import Ranking
from Train import Train_model
from Create_Profile import create_profile




def check_length_data(filepath):

    filewords = open(filepath, "rt")
    data = filewords.read()
    words = data.split()

    return len(words)

def remove_extra_symbol(data):
    chars = [';', ':', '!', "*","#","%",","] 
    for i in chars : 
        data = data.replace(i, '') 
    return data


def convert_csv_to_text(filepath,user_data,header):
    f = open(filepath, "w")
    for data in user_data[header]:
        if str(data) != 'nan':
            data = remove_extra_symbol(data)
            f.write(data+"\n")
    f.close()


## Main code
def res(JD_path,rank):

    
    #Path for the files
    resume_path = '../Upload-Resume' #enter your path here where you saved the resumes

    onlyfiles = [os.path.join(resume_path, f) for f in os.listdir(resume_path) if os.path.isfile(os.path.join(resume_path, f))]

    JD_data = pd.read_excel (JD_path)
    UserDataPath = '../Preprocess-JD/user_data.csv'
    JD_data.to_csv (UserDataPath, index = None, header=True)
    user_data = pd.read_csv(UserDataPath, squeeze = True) 
     
    user_data_path = "../Preprocess-JD/" 
    new_keyword = []
    new_keyword_dict = {}
    for columns in user_data.columns:
        convert_csv_to_text(user_data_path+columns+".txt",user_data,columns)
        len_words = check_length_data(user_data_path+columns+".txt")
        new_keyword_dict[columns] = ''
        if len_words >= 4:
            new_keyword.append(Train_model(user_data_path+columns+".txt",columns))
            new_keyword_dict[columns] = Train_model(user_data_path+columns+".txt",columns)
    #print(new_keyword_dict)



    #skill_path = "../Preprocess-JD/Skill.txt"
    #qualification_path = "../Preprocess-JD/Qualification.txt"
    #pastcompany_path = "../Preprocess-JD/Pastcompany.txt"
    #Role_path = "../Preprocess-JD/Role.txt"

    #convert_csv_to_text(skill_path,user_data,'Skill')
    #convert_csv_to_text(qualification_path,user_data,'Qualification')
    #convert_csv_to_text(pastcompany_path,user_data,'Pastcompany')
    #convert_csv_to_text(Role_path,user_data,'Role')


        

    # Code to execute the above functions 
    final_db=pd.DataFrame()
    i=0
    experience1 ={}
    file_path = {}


   # skill_flag = 1
   # qualification_flag = 2
   # pastcompany_flag = 3

    #len_words_skill = check_length_data(skill_path)
    #len_words_qualification = check_length_data(qualification_path)
    #len_words_pastcompany = check_length_data(pastcompany_path)


    #new_keyword_skill = ''
    #new_keyword_qualification = ''
    #new_keyword_pastcompany = ''
    #new_keyword_role = ''

    #if len_words_skill >= 4:
    #new_keyword_skill = Train_model(skill_path,"Skill")
    #print(new_keyword_skill)

    #if len_words_qualification >= 4:
    #new_keyword_qualification = Train_model(qualification_path,"Qualification")

    #if len_words_pastcompany >= 4:
    #new_keyword_pastcompany = Train_model(pastcompany_path,"Pastcompany")



    while i < len(onlyfiles):
        file=onlyfiles[i]

        
        #dat,experience,Can_name = create_profile(file,new_keyword_skill,new_keyword_qualification,new_keyword_pastcompany,new_keyword)
        dat,experience,Can_name = create_profile(file,new_keyword,new_keyword_dict)
        final_db=final_db.append(dat)
        i+=1

        head, tail = os.path.split(file)
        experience1[Can_name] = experience
        file_path[Can_name] = tail


    #Code to count words under each category and visualize it through MAtplotlib
    final_db2 = final_db['Keyword'].groupby([final_db['Candidate Name'], final_db['Subject']]).count().unstack()
    final_db2.reset_index(inplace = True)
    final_db2.fillna(0,inplace=True)
    candidate_data = final_db2.iloc[:,1:]
    candidate_data.index = final_db2['Candidate Name']
    #the candidate profile in a csv format
    cand=candidate_data.to_csv('../Preprocess-JD/candidate_profile.csv')
    df5 = pd.read_csv('../Preprocess-JD/candidate_profile.csv', squeeze = True) 

    # Add a experience in frame
    df6 = DataFrame(list(experience1.items()),columns = ['Can_name','Experience']) 
    df5['Experience'] = df5['Candidate Name'].apply(lambda x: df6[df6['Can_name']==x]['Experience'].values[0])

    df7 = DataFrame(list(file_path.items()),columns = ['Can_name','file_path']) 

    df5['file_path'] = df5['Candidate Name'].apply(lambda x: df7[df7['Can_name']==x]['file_path'].values[0])
    cand=df5.to_csv('../Preprocess-JD/candidate_profile.csv')

    ## Ranking
    #rank = ["Skill"]

    ranking = Ranking(df5,user_data,rank)
     
    return(ranking,user_data)
