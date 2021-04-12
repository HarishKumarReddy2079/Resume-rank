import csv
import re
import numpy as np
import pandas as pd

def Ranking(df5,UserData,rank):

    OutputCSV = ["Candidate Name"]
    experience3 = UserData['Experience'].dropna().unique().tolist()
    for exp in experience3:
      experience3 = exp

    for columns in UserData.columns:
      OutputCSV.append(columns)
      if columns not in df5:
        df5[columns] = float("0.0")
    OutputCSV.append("file_path")

   

     
    # Qualification
   # if "Qualification" not in df5:
    #  df5['Qualification'] = float("0.0")

    # Skill
    #if "Skill" not in df5:
    #  df5['Skill'] = float("0.0")

    # Role
    #if "Role" not in df5:
    #  df5['Role'] = float("0.0")

    # Pastcompany
    #if "Pastcompany" not in df5:
    #  df5['Pastcompany'] = float("0.0")


      
    # Experience
    if re.compile(r'[0-9]-[0-9]').search(experience3):
      experience = experience3.split("-")
      if experience[0] != "0":
        df5['Experience'] = df5['Experience'].apply(lambda x: np.where(x <= float(experience[0]),0,x))
      else:
        df5['Experience'] = df5['Experience'].apply(lambda x: np.where(x >= float(experience[0]),x+1.0,x))

     # df5['Experience'] = df5['Experience'].apply(lambda x: np.where(x >= float(experience[1]),0,x))

    elif re.compile(r'[0-9]+').search(experience3):

      if "+" in experience3:

        experience = experience3.split("+")
        if experience[0] != "0":
          df5['Experience'] = df5['Experience'].apply(lambda x: np.where(x <= float(experience[0]),0,x))
        else:
          df5['Experience'] = df5['Experience'].apply(lambda x: np.where(x >= float(experience[0]),x+1.0,x))

      else:
        experience = re.sub("\D", "", experience3)
        if experience != "0":
          df5['Experience'] = df5['Experience'].apply(lambda x: np.where(x <= float(experience),0,x))
        else:
          df5['Experience'] = df5['Experience'].apply(lambda x: np.where(x >= float(experience),x+1.0,x))


    elif re.compile(r'[a-zA-Z]').search(experience3):
      df5['Experience'] = df5['Experience'].apply(lambda x: np.where(x > 0.0,0.1,x))
      df5['Experience'] = df5['Experience'].apply(lambda x: np.where(x == 0.0,1,x))
      df5['Experience'] = df5['Experience'].apply(lambda x: np.where(x == 0.1,0.0,x))


    else:
      df5['Experience'] = float("0.0")

    #OutputCSV = ['Candidate Name','Skill','Experience','Pastcompany','Role','Qualification',"file_path"]

    df5 = pd.DataFrame(df5, columns = OutputCSV)  


    df5.rename(columns = {'Unnamed: 0':'Index'}, inplace = True) 
    #rank = ["Skill","Company","Role","Qualification","Experience"]
   # rank = ["Qualification","Experience"]

    rank_value = []
    rank_flag =  []
    for criteria in rank:

      rank_value.append(criteria)
      rank_flag.append(False)

      for columns in UserData.columns:
        if criteria == columns:
          df5 = df5.loc[(df5[columns] >= 1.0)]

      #if criteria == "Skill":
      #  df5 = df5.loc[(df5['Skill'] >= 1.0)]
       # df5 = df5.loc[(df5['AnyOtherSkill'] >= 1.0)]
     # if criteria == "Pastcompany":
     #   df5 = df5.loc[(df5['Pastcompany'] >= 1.0)] 
     # if criteria == "Role":
     #   df5 = df5.loc[(df5['Role'] >= 1.0)] 
     # if criteria == "Qualification":
     #   df5 = df5.loc[(df5['Qualification'] >= 1.0)]
     # if criteria == "Experience":
      #  df5 = df5.loc[(df5['Experience'] >= 1.0)] 

    df5["Total"] = df5.sum(axis = 1, skipna = True) 


    #df5["Total"] = df5["Skill"] + df5["Qualification"] +df5["Experience"] + df5["Pastcompany"] + df5["Role"] 
    df5["Ranking"] = (df5["Total"]/df5["Total"].sum())*100
    df5["Ranking"] = df5["Ranking"].round(4)


    if len(rank) >= 1:
      df5.sort_values(rank_value, axis=0,
                     ascending=rank_flag,
                     inplace=True) 
    else:
      df5.sort_values("Ranking", axis = 0, ascending = False, inplace = True)

    df5.to_csv('../Preprocess-JD/Result.csv')
 

   # os.remove("Result.csv")
    #os.remove(ResumeData)
    #os.remove(UserDataPath)
    return(df5["file_path"].values.tolist())

