
## Needed Libraries
from PIL import Image
from gensim.models import Word2Vec
import string
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')
nltk.download('stopwords')
import gensim
from gensim.models.phrases import Phraser, Phrases
import os



def Train_model(Branch_path,JD_columns):
    ## Dataset from create JD
    with open(Branch_path,encoding="utf8") as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]

    x=[]
    for line in content:
        tokens=word_tokenize(line)
        tok=[w.lower() for w in tokens]
        table=str.maketrans('','',string.punctuation)
        strpp=[w.translate(table) for w in tok]
        words=[word for word in strpp if word.isalpha()]
        stop_words=set(stopwords.words('english'))
        words=[w for w in words if not w in stop_words]
        x.append(words)

    texts=x
    new_keyword = ''

    ## Match Keyword
    for text in texts:
        if len(text) >= 1:
            new_keyword = text


    ## Create another Dataset
    with open('../Preprocess-JD/common.txt','w+') as f:
        content2 = f.read()
    ntexts=[]
    l=len(texts)
    for j in range(l):
        s=texts[j]
        res = [i for i in s if i not in content2]
        ntexts.append(res)
    os.remove('../Preprocess-JD/common.txt')



    common_terms = ["of", "with", "without", "and", "or", "the", "a"]
    x=ntexts
    # Create the relevant phrases from the list of sentences:
    phrases = Phrases(x, min_count=1,common_terms=common_terms)
    # The Phraser object is used from now on to transform sentences
    bigram = Phraser(phrases)
    # Applying the Phraser to transform our sentences
    all_sentences = list(bigram[x])
    model=gensim.models.Word2Vec(all_sentences,size=5000,min_count=1,workers=4,window=4)
    model.save("../TrainModel/"+JD_columns+".model")

   # if Branchflag == 1:
   #     model.save("../TrainModel/Skill.model")
   # if Branchflag == 2:
   #     model.save("../TrainModel/Qualification.model")
   # if Branchflag == 3:
   #     model.save("../TrainModel/Pastcompany.model")


    wrds=list(model.wv.vocab)
    return new_keyword


