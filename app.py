import cPickle as c
import cPickle as c
import os
from sklearn import *
from collections import Counter
from flask import Flask, request, render_template
from sqlalchemy.orm import sessionmaker
from flask import Flask, flash, redirect, render_template, request, session, abort
from tabledef import *
engine = create_engine('sqlite:///tutorial.db', echo=True)
from werkzeug import secure_filename
#un="sakilbhai"
#ps="sakil123"
status=""
list1=(os.listdir('/home/sakil/Desktop/project1/sakil/emails'))
str1 = ''.join(list1) 
UPLOAD_FOLDER = '/home/sakil/Desktop/project1/sakil/emails'

def load(classifier_file):
    with open(classifier_file) as fp:
        classifier=c.load(fp)
    return classifier
def make_dict():
    directory = "emails/"
    root = os.listdir(directory)
    emails = [directory + email for email in root]
    words = []

    count = len(emails)
    for email in emails:
        y = open(email)
        z = y.read()
        words += z.split(" ")
        print count
        count -= 1

    for j in range(len(words)):
        if not words[j].isalpha():
            words[j] = ""

    dictionary = Counter(words)
    del dictionary[""]
    return dictionary.most_common(3000)





app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
@app.route('/')
def my_form():
    return render_template('hello.html')
@app.route('/', methods=['POST'])
def my_form_post():

    text = request.form['mail']
    classifier = load("model.mdl")
    dict = make_dict()
    
    features = []
    user = text.split()
        
    for word in dict:
        features.append(user.count(word[0]))
    res = classifier.predict([features])
    
    a=["Not Spam", "Spam!"][res[0]]
    return render_template('hello.html',result=a)

@app.route('/login')
#def loginpage():
def home():
    pass
     #return render_template('home.html')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
         lisst=(os.listdir('/home/sakil/Desktop/project1/sakil/emails')) 
         return render_template('filelist.html',resul=lisst)


    

@app.route('/loginauth',methods=['POST'])
#def ifsuccess():
def do_admin_login():
    #uname=request.form['uname']
    #passw=request.form['psw']
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]))
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()



    #if request.form['password'] == 'password' and request.form['username'] == 'admin':
      #  session['logged_in'] = True
    #else:
     #   flash('wrong password!')
    #return home()
    #if un==uname and passw==ps:
     #   lisst=(os.listdir('/home/sakil/Desktop/project1/sakil/emails')) 
      #  return render_template('filelist.html',resul=lisst)
        
     
        

    #else:
        #return "LOGIN FAILED PLEASE CHECK YOUR USERNAME AND PASSWORD!! PLEASE GO BACK AND TRY AGAIN"
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))
      lisst=(os.listdir('/home/sakil/Desktop/project1/sakil/emails')) 
      return render_template('filelist.html',status="success",resul=lisst)





    
if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug = True)



