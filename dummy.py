import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *
from flask import Flask
app = Flask(__name__)
engine = create_engine('sqlite:///tutorial.db', echo=True)
 
# create a Session
Session = sessionmaker(bind=engine)
session = Session()
 
user = User("sakil","sakil123")
session.add(user)
 
user = User("athira","athira123")
session.add(user)
 
user = User("chowta","chowta123")
session.add(user)
 
# commit the record the database
session.commit()
 
session.commit()
@app.route('/test')
def test():
 
    POST_USERNAME = "python"
    POST_PASSWORD = "python"
 
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        return "Object found"
    else:
        return "Object not found " + POST_USERNAME + " " + POST_PASSWORD