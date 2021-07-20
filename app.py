import glob
import os
import warnings
from flask import (Flask,session,flash, redirect, render_template, request,
                   url_for, send_from_directory)
import pandas as pd
import NLP_matching
import operator
import re

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

app = Flask(__name__)

app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    USERNAME='admin',
    PASSWORD='admin',
    SECRET_KEY='development key',
))


app.config['UPLOAD_FOLDER'] = 'Upload-Resume'
app.config['UPLOAD_JD_FOLDER'] = 'Upload-JD'
app.config['ALLOWED_EXTENSIONS'] = set(['pdf', 'doc', 'docx'])

class jd:
    def __init__(self, name):
        self.name = name

def getfilepath(loc):
    temp = str(loc).split('\\')
    return temp[-1]
"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))
"""

@app.route('/')
def home():
    error = None
    x = os.listdir(app.config['UPLOAD_FOLDER'])
    """
    if len(x) == 0:
        error = "Please Add Resume"
    """
    return render_template('index.html', name = x,error=error)

@app.route('/results', methods=['GET', 'POST'])
def addcvJD():

    if request.method =='POST' :
        #addcvJD1 = request.form.get("addcvJD",None)
        uploadResume1 = request.form.get("uploadResume",None)
        UploadJD1 = request.form.get("Upload-JD",None)
        Calculate_rank = request.form.get("Calculate_Rank",None)
        Resume_id = request.form.get("RemoveResume",None)

        if uploadResume1 == "uploadResume":
            #session.pop('add_cv_JD', None)
            return redirect(url_for('uploadResume'))


        if UploadJD1 == "Upload-JD":
            #session.pop('add_cv_JD', None)
            return redirect(url_for('uploadjdDesc'))

        if Calculate_rank == "Calculate_Rank":
            return redirect(url_for('SELECTJD'))

        if Resume_id != "None":
            Resume_id = request.form["RemoveResume"]
            os.remove("."+Resume_id)
            x = os.listdir(app.config['UPLOAD_FOLDER'])
            return redirect(url_for('home'))

    return redirect(url_for('home'))


@app.route('/results1', methods=['GET', 'POST'])
def res():
    if request.method == 'GET':

       Prioritylist = session.get('Prioritylist', None)
       selectJD_id = session.get('selectJD_id', None)
       JD_columns  = session.get('JD_columns',None)
       JD_columns_data = session.get('JD_columns_data')
       selectJD_id1 = os.path.basename(selectJD_id)

       print(Prioritylist)

       JD_data = pd.read_excel ("."+selectJD_id)

       os.chdir(app.config['UPLOAD_JD_FOLDER'])

       flask_return,csv_data = NLP_matching.res(selectJD_id1,Prioritylist)
       df = pd.DataFrame(columns = JD_columns)
       df = df.append(JD_columns_data, ignore_index=True)

       os.chdir('..') 
       return render_template('result.html', results = flask_return,jd = df)
    return render_template("index.html")

@app.route('/uploadjdDesc1', methods=['GET', 'POST'])
def SELECTJD():
    x = os.listdir(app.config['UPLOAD_JD_FOLDER'])
    error = None
    if len(x) == 0:
        error = "Please add JD"
    return render_template('SELECTJD.html',name = x,error=error)


@app.route('/uploadResume', methods=['GET', 'POST'])
def uploadResume():
    x = os.listdir(app.config['UPLOAD_FOLDER'])


    return render_template('uploadresume.html',name = x)

"""
@app.route('/RemoveResume', methods=['GET', 'POST'])
def RemoveResume():

    if request.method == 'POST':
        Resume_id = request.form["RemoveResume"]
        os.remove("."+Resume_id)

       # x = os.listdir(app.config['UPLOAD_FOLDER'])

        return render_template('uploadresume.html')
    return render_template('uploadresume.html')
"""



@app.route("/upload", methods=['POST'])
def upload_file():
    Error = None
    if request.method=='POST' and 'customerfile' in request.files:
        x = os.listdir(app.config['UPLOAD_FOLDER'])

        for f in request.files.getlist('customerfile'):
            if f.filename in x:
                Error = "All Ready "+f.filename +" Existed"
                return render_template("uploadresume.html",error=Error)
            else:
                res = bool(re.search(r"\s", f.filename))
                if res == True:
                    Error = "Please Rename your file "+f.filename
                    return render_template("uploadresume.html",error=Error)
                else:
                    f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))

        return redirect(url_for('home'))
    

@app.route('/uploadjdDesc', methods=['GET', 'POST'])
def uploadjdDesc():
    x = os.listdir(app.config['UPLOAD_JD_FOLDER'])

    return render_template('uploadjd.html',name = x)


@app.route("/uploadjd", methods=['POST'])
def upload_jd_file():
    
    Error = None

    if request.method=='POST' and 'customerfile' in request.files:
        filelist = [ f for f in os.listdir(app.config['UPLOAD_JD_FOLDER']) if f.endswith(".xlsx") ]
          
        x = os.listdir(app.config['UPLOAD_JD_FOLDER'])

        for f in request.files.getlist('customerfile'):
            if f.filename in x:
                Error = "All Ready "+f.filename +" Existed"
                return render_template("uploadjd.html",error=Error)

            else:
                res = bool(re.search(r"\s", f.filename))
                if res == True:
                    Error = "Please Rename your file "+f.filename
                    return render_template("uplodjd.html",error=Error)
                else:
                    f.save(os.path.join(app.config['UPLOAD_JD_FOLDER'], f.filename))
            
        return redirect(url_for('home'))


@app.route('/RemoveJD', methods=['GET', 'POST'])
def RemoveJD():

    if request.method == 'POST':
        JD_id = request.form["RemoveJD"]
        os.remove("."+JD_id)

        #os.remove()
        x = os.listdir(app.config['UPLOAD_JD_FOLDER'])

        return redirect(url_for('SELECTJD'))
    return redirect(url_for('SELECTJD'))

@app.route('/SelectJD', methods=['GET', 'POST'])
def SelectJD():
    session['Prioritylist'] = []
    return redirect(url_for('res'))

@app.route('/ViewJD', methods=['GET', 'POST'])
def ViewJD():

    if request.method == 'POST':
        ViewJD_id = request.form["ViewJD"]
        session['selectJD_id'] = ViewJD_id

        JD_columns = []
        JD_columns_data = {}
        JD_data = pd.read_excel ("."+ViewJD_id)
        UserDataPath = 'Preprocess-JD/ShowJD.csv'
        JD_data.to_csv (UserDataPath, index = None, header=True)
        user_data = pd.read_csv(UserDataPath, squeeze = True)
        for data_column in user_data.columns:
            JD_columns.append(data_column)
            JD_columns_data[data_column] = user_data[data_column].dropna().unique().tolist()

        session['JD_columns'] = JD_columns
        session['JD_columns_data'] = JD_columns_data

        df = pd.DataFrame(columns = JD_columns)
        df = df.append(JD_columns_data, ignore_index=True)
        return render_template('ShowJD.html',jd = df)

    return redirect(url_for('SELECTJD'))




@app.route('/SetPriority', methods=['GET', 'POST'])
def SetPriority():
    
    JD_id_priority= session.get('selectJD_id', None)
    JD_data = pd.read_excel ("."+JD_id_priority)
    UserDataPath = 'Preprocess-JD/ShowJD.csv'
    JD_data.to_csv (UserDataPath, index = None, header=True)
    user_data = pd.read_csv(UserDataPath, squeeze = True)
    Priority_name =[]
    for name in user_data.columns:
        Priority_name.append(name)
    session['user_data_priority'] = Priority_name

 
    return render_template('SetPriority.html',name = user_data.columns)

@app.route('/SetPriority1', methods=['GET', 'POST'])
def SetPriority1():
    FinalPriority = {}
    if request.method == 'POST':
        Priority_value = request.form.getlist("Priority_number")
        Priority_name = session.get('user_data_priority', None)
        
        for name in Priority_name:
            for value in Priority_value:
                FinalPriority[name] = value
                Priority_value.remove(value) 
                break
        
        FinalPriority = {key:val for key, val in FinalPriority.items() if val != ""} 

        FinalPriority = sorted(FinalPriority.items(), key=operator.itemgetter(1))
        Prioritylist = []

        for pri in FinalPriority:
            Prioritylist.append(pri[0])
        print(Prioritylist)

        session['Prioritylist'] = Prioritylist
    
    return redirect(url_for('res'))


@app.route('/Upload-Resume/<path:filename>')
def custom_static(filename):
    return send_from_directory('./Upload-Resume', filename)


@app.route('/Upload-JD/<path:filename>')
def custom_static1(filename):
    return send_from_directory('./Upload-JD', filename)

if __name__ == '__main__':
   # app.run(debug = True) 
    # app.run('127.0.0.1' , 5000 , debug=True)
    app.run(host='0.0.0.0', debug=True , threaded=True, port=int(os.environ.get('PORT',3000)))
    
