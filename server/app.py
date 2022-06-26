from flask import Flask, jsonify, request,render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy import inspect
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

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

# get all links
@app.route('/get_links' , methods = [ 'GET'])
def Get_links():
    # return jsonify(Users.query.all().as_dict())
    return jsonify(list(map(lambda x:x.as_dict(),Links.query.all())))


@app.route('/users' , methods = [ 'GET','POST'])
def Multiple_users():
    response = {}
    if request.method == 'POST':
        data = request.get_json()
        if data == {}:
            return jsonify({'Result':False})

        inst = inspect(Users)
        attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
        attr_names.remove('user_id')
        new_user = Users()
        for field in attr_names:
            if data.get(field,''):
                setattr(new_user, field, data[field])

        
        db.session.add(new_user)
        db.session.commit()
        response['status'] = 'success'
        response['message'] = 'Utilisateur ajouté !'
        
    else:
        response['status'] = 'success'
        response['users'] = list(map(lambda x:x.as_dict(),Users.query.all()))
    return jsonify(response)

@app.route('/users/<id>', methods=['DELETE','PUT'])
def single_user(id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        data = request.get_json()
        
        inst = inspect(Users)
        attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
        attr_names.remove('user_id')
        target_user = Users.query.filter_by(user_id=id).first()
        print(target_user)
        for field in attr_names:
            if data.get(field,''):
                setattr(target_user, field, data[field])


        db.session.commit()

        response_object['message'] = 'User updated!'
    
    if request.method == 'DELETE':
        target_user = Users.query.filter_by(user_id=id).first()
        if target_user:
            db.session.delete(target_user)
            db.session.commit()
            response_object['message'] = 'Book removed!'
        else:
            response_object['status'] = 'failure'
            response_object['message'] = "User doesn't exists"
    return jsonify(response_object)

@app.route('/links' , methods = [ 'GET','POST'])
def Multiple_links():
    response = {}
    if request.method == 'POST':
        data = request.get_json()
        if data == {}:
            return jsonify({'Result':False})

        inst = inspect(Links)
        attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
        attr_names.remove('link_id')
        new_link = Links()
        response['status'] = 'success'
        response['message'] = 'Lien ajouté !'
        for field in attr_names:
            if data.get(field,'') and data.get(field,'').isnumeric():
                setattr(new_link, field, data[field])
            else:
                response['status'] = 'failure'
                response['message'] = f'missing field {field} or non numeric'

        
        db.session.add(new_link)
        db.session.commit()

        
    else:
        response['status'] = 'success'
        response['links'] = list(map(lambda x:x.as_dict(),Links.query.all()))
    return jsonify(response)

@app.route('/links/<id>', methods=['DELETE','PUT'])
def single_link(id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        data = request.get_json()
        
        inst = inspect(Links)
        attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
        attr_names.remove('link_id')
        target_user = Links.query.filter_by(link_id=id).first()
        print(target_user)
        for field in attr_names:
            if data.get(field,''):
                setattr(target_user, field, data[field])


        db.session.commit()

        response_object['message'] = 'User updated!'
    
    if request.method == 'DELETE':
        target_user = Links.query.filter_by(link_id=id).first()
        if target_user:
            db.session.delete(target_user)
            db.session.commit()
            response_object['message'] = 'Link removed!'
        else:
            response_object['status'] = 'failure'
            response_object['message'] = "Link doesn't exists"
    return jsonify(response_object)


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

@app.route('/show_family' , methods = [ 'GET'])
def Show_family():
    plt.figure()
    g = nx.Graph() # DiGraph() pour un graphe orienté
    # g.add_nodes_from(range(5))
    # g.add_edges_from([(0,1),(3,4),(4,2),(1,3),(4,0),(1,2)])
    # options = {
    #   'node_color' : 'yellow',
    #   'node_size'  : 550,
    #   'edge_color' : 'tab:grey',
    #   'with_labels': True
    # }
    
    for user in Users.query.all():
        print(user.first_name)
        g.add_node(user.user_id, name=user.first_name)
    
    for link in Links.query.all():
        g.add_edge(link.base_user, link.dest_user)
    names = nx.get_node_attributes(g, 'name') 
    print(names)
    nx.draw(g,with_labels=True,labels=names)

    plt.savefig("./static/family.png") 
    return render_template("show.html", user_image = "./static/family.png")

@app.route('/tree' , methods = [ 'GET'])
def Make_tree():
    data = {
    'name': 'root',
    'image_url': "https://static.refined-x.com/avat.jpg",
    'class': ["rootNode"],
    'children': [
      {
        'name': 'children1',
        'image_url': "https://static.refined-x.com/avat1.jpg"
      },
      {
        'name': 'children2',
        'image_url': "https://static.refined-x.com/avat2.jpg",
        'mate': {
          'name': 'mate',
          'image_url': "https://static.refined-x.com/avat3.jpg"
        },
        'children': [
          {
            'name': 'grandchild',
            'image_url': "https://static.refined-x.com/avat.jpg"
          },
          {
            'name': 'grandchild2',
            'image_url': "https://static.refined-x.com/avat1.jpg"
          },
          {
            'name': 'grandchild3',
            'image_url': "https://static.refined-x.com/avat2.jpg"
          }
        ]
      },
      {
        'name': 'children3',
        'image_url': "https://static.refined-x.com/avat.jpg"
      }
    ]
    }
    data2 = [{
        'firstPerson': {
          'name': 'John Walker',
          'image': 'https://picsum.photos/300/300?random=1'
        },
        'secondPerson': {
          'name': 'Jannet Grem',
          'image': 'https://picsum.photos/300/300?random=2'
        },
        'children': [{
          'firstPerson': {
            'name': 'Katia'
          },
          'thirdPerson': {
            'name': 'Katia2'
          },
          'secondPerson': {
            'name': 'Oleg'
          },
          'children': [{
            'firstPerson': {
              'name': 'Gleb'
            },
            'secondPerson': {
              'name': 'Viktoriya'
            },
            'children': [{
              'firstPerson': {
                'name': 'Rim'
              },
              'secondPerson': {
                'name': 'Natasha'
              }
            },
            {
              'firstPerson': {
                'name': 'Leonid'
              }
            }]
          },
          {
            'firstPerson': {
              'name': 'Olga'
            },
            'secondPerson': {
              'name': 'Nikita'
            }
          }]
        },
        {
          'firstPerson': {
            'name': 'Vitia'
          },
          'secondPerson': {
            'name': 'Dasha'
          }
        },
        {
          'firstPerson': {
            'name': 'Antonio Wild',
            'image': 'https://picsum.photos/300/300?random=3'
          },
          'secondPerson': {
            'name': 'Olivia Olson'
          },
          'children': [{
            'firstPerson': {
              'name': 'Kristina Wild'
            }
          },
          {
            'firstPerson': {
              'name': 'Alexey Wild'
            }
          },
          {
            'firstPerson': {
              'name': 'Viktor Wild'
            }
          }]
        }]
      }]
    return jsonify(data2)


# Debug route
@app.route('/test' , methods = [ 'GET','POST'])
def Test_route():
    new_user = Users()
    new_user.first_name = 'Toto'

    return jsonify(new_user.as_dict())

    return jsonify(fields)

if __name__ == '__main__':
    app.run()
