from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy import inspect

import os
from dotenv import load_dotenv

load_dotenv()

MASTER_PASSWD = os.getenv('MASTER_PASSWD')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWD = os.getenv('MYSQL_PASSWD')
MYSQL_DB = os.getenv('MYSQL_DB')
MYSQL_SERVER = os.getenv('MYSQL_SERVER')

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# connect DB
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{MYSQL_USER}:{MYSQL_PASSWD}@{MYSQL_SERVER}/{MYSQL_DB}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    sexe = db.Column(db.Integer)

    def as_dict(self):
        inst = inspect(self.__class__)
        attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
        fields = {}
        for field in attr_names:
            data = self.__getattribute__(field)
            try:
                    #json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
            except TypeError:
                fields[field] = None
        return fields

# Link types:
# 0 = Conjoint
# 1 = Enfant
#       dest_user est l'enfant de base_user
class Links(db.Model):
    link_id = db.Column(db.Integer, primary_key = True)
    base_user = db.Column(db.Integer)
    link_type = db.Column(db.Integer)
    dest_user = db.Column(db.Integer)

    def as_dict(self):
        inst = inspect(self.__class__)
        attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
        fields = {}
        for field in attr_names:
            data = self.__getattribute__(field)
            try:
                    #json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
            except TypeError:
                fields[field] = None
        return fields

db.create_all()

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

#login route
@app.route('/login' , methods = [ 'POST'])
def Login():
    # if request.form == {}:
    #     return jsonify({'Result':False})
    if request.form.get('password','') == MASTER_PASSWD:
        return jsonify({'Result':True})

#get all users
@app.route('/get_users' , methods = [ 'GET'])
def Get_users():
    # return jsonify(Users.query.all().as_dict())
    return jsonify(list(map(lambda x:x.as_dict(),Users.query.all())))

# get all links
@app.route('/get_links' , methods = [ 'GET'])
def Get_links():
    # return jsonify(Users.query.all().as_dict())
    return jsonify(list(map(lambda x:x.as_dict(),Links.query.all())))

#add user
@app.route('/add_user' , methods = [ 'POST'])
def Add_user():
    if request.form == {}:
        return jsonify({'Result':False})

    inst = inspect(Users)
    attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
    attr_names.remove('user_id')
    new_user = Users()
    for field in attr_names:
        if request.form.get(field,''):
            setattr(new_user, field, request.form[field])

    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'Result':True})

@app.route('/add_link' , methods = [ 'POST'])
def Add_link():
    if request.form == {}:
        return jsonify({'Result':False})

    inst = inspect(Links)
    attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
    attr_names.remove('link_id')
    new_link = Links()
    for field in attr_names:
        if request.form.get(field,'') and request.form.get(field,'').isnumeric():
            setattr(new_link, field, request.form[field])
        else:
            return jsonify({'Result':False})
    
    db.session.add(new_link)
    db.session.commit()

    return jsonify({'Result':True})

# Debug route
@app.route('/test' , methods = [ 'GET','POST'])
def Test_route():
    new_user = Users()
    new_user.first_name = 'Toto'

    return jsonify(new_user.as_dict())

    return jsonify(fields)

if __name__ == '__main__':
    app.run()
