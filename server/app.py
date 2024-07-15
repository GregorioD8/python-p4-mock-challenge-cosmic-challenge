#!/usr/bin/env python3

from models import db, Scientist, Mission, Planet
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

# Initialize FLASK-RESTful for creating REST APIs
api = Api(app)

@app.route('/')
def home():
    return ''

# GET /scientists
# Return JSON data in the format below. Note: you should return a JSON response in this format, 
# without any additional nested data related to each scientist.

# [
#   {
#     "id": 1,
#     "name": "Mel T. Valent",
#     "field_of_study": "xenobiology"
#   },
#   {
#     "id": 2,
#     "name": "P. Legrange",
#     "field_of_study": "orbital mechanics"
#   }

class Scientists(Resource):

    def get(self):
        # Handle GET request to retrieve all Scientists
        try:
            scientists = Scientist.query.all()

            #convert each scientist object to dict
            new_scientists = [s.to_dict(only=('id', 'name', 'field_of_study')) for s in scientists]

            return new_scientists, 200
        except:
            return {'error': 'Bad request'}, 400

    # POST /scientists
    # This route should create a new Scientist. It should accept an object with the following properties in the body of the request:

    # {
    # "name": "Evan Horizon",
    # "field_of_study": "astronavigation"
    # }
    # If the Scientist is created successfully, send back a response with the new Scientist:

    # {
    # "id": 3,
    # "name": "Evan Horizon",
    # "field_of_study": "astronavigation",
    # "missions": []
    # }
    # If the Scientist is not created successfully due to validation errors, return the following JSON data, along with the appropriate HTTP status code:

    # {
    # "errors": ["validation errors"]
    # }

    def post(self):
        # Handle POST request  to create a new scientist
        try:
            new_scientist = Scientist(
                name=request.json['name'], 
                field_of_study=request.json['field_of_study'] 
            )
            db.session.add(new_scientist)
            db.session.commit()
            
            return new_scientist.to_dict(only=('id', 'name', 'field_of_study')), 201
        except:
            return { 'errors': ['validation errors']}, 400

# Add the Scientists resource to the API at the /scientists endpoint
api.add_resource(Scientists, '/scientists')


# GET /scientists/int:id
# If the Scientist exists, return JSON data in the format below. 
# Make sure to include a list of missions for the scientist.

# "field_of_study": "Orbits",
#     "id": 1,
#     "name": "Joseph Richard",
#     "missions": [
#         {
#             "id": 1,
#             "name": "Explore Planet X.",
#             "planet": {
#                 "distance_from_earth": 302613474,
#                 "id": 8,
#                 "name": "X",
#                 "nearest_star": "Shiny Star"
#             },
#             "planet_id": 8,
#             "scientist_id": 1
#         },
#         {
#             "id": 10,
#             "name": "Explore Planet Y.",
#             "planet": {
#                 "distance_from_earth": 1735242898,
#                 "id": 14,
#                 "name": "Y",
#                 "nearest_star": "Dim Star"
#             },
#             "planet_id": 14,
#             "scientist_id": 1
#         }
#     ]
# }

class ScientistsById(Resource):

    def get(self, id):
        # Handle GET request to retrieve a scientist by ID
        try:
            scientist = Scientist.query.filter_by(id=id).first()
            if not scientist:
                return {'error': 'Scientist not found'}, 404
            return scientist.to_dict(only=('id', 'name', 'field_of_study', 'missions')), 200
        except:
            return {'error': 'Scientist not found'}, 404
        
    def patch(self, id):
        # Handle PATCH request to update a camper by ID
        try:
            scientist = Scientist.query.filter_by(id=id).first()
            if not scientist:
                return {'error': 'Scientist not found'}, 404
            
            if 'name' in request.json:
                scientist.name = request.json['name']
            if 'field_of_study' in request.json:
                scientist.field_of_study = request.json['field_of_study']
            db.session.add(scientist)
            db.session.commit()
            return scientist.to_dict(only=('id', 'name', 'field_of_study')), 202
        except:
            return {'errors': ['validation errors']}, 400
        
    def delete(self, id):
        try:
            scientist = Scientist.query.filter_by(id=id).first()
            if not scientist:
                return {'error': 'Scientist not found'}, 404
            db.session.delete(scientist)
            db.session.commit()
            return {}, 204
        except:
            return {'error': 'Scientist not found'}, 404

# Add the ScientistbById resource to the API at the /scientists endpoint
api.add_resource(ScientistsById, '/scientists/<int:id>')

# GET /planets
# Return JSON data in the format below. Note: you should return a JSON response in this format, 
# without any additional nested data related to each planet.

# [
#   {
#     "id": 1,
#     "name": "TauCeti E",
#     "distance_from_earth": 1234567,
#     "nearest_star": "TauCeti"
#   },
#   {
#     "id": 2,
#     "name": "Maxxor",
#     "distance_from_earth": 99887766,
#     "nearest_star": "Canus Minor"
#   }
# ]


class Planets(Resource):
    def get(self):
        # Handle  GET request to retrieve all planets
        try:
            planets = [planet.to_dict(only=('id', 'name', 'distance_from_earth', 'nearest_star')) for planet in Planet.query.all()]
            return planets, 200
        except:
            return {'error': 'Bad request'}, 400
# Add the Activities resource to the API at the /activities endpoint
api.add_resource(Planets, '/planets')        


# POST /missions
# This route should create a new Missions. 
# It should accept an object with the following properties in the body of the request:

# {
#   "name": "Project Terraform",
#   "scientist_id": 1,
#   "planet_id": 2
# }
# If the Mission is created successfully, send back a response about the new mission:

# {
#   "id": 21,
#   "name": "Project Terraform",
#   "planet": {
#     "distance_from_earth": 9037395591,
#     "id": 2,
#     "name": "Planet X",
#     "nearest_star": "Krystal"
#   },
#   "planet_id": 2,
#   "scientist": {
#     "field_of_study": "Time travel.",
#     "id": 1,
#     "name": "Jeremy Oconnor"
#   },
#   "scientist_id": 1
# }
# If the Mission is not created successfully, return the following JSON data, along with the appropriate HTTP status code:

# {
#   "errors": ["validation errors"]
# }

class Missions(Resource):
    def  post(self):
        # Handle POST request to create a new signup
        try:
            mission = Mission(
                name=request.json['name'],
                scientist_id=request.json['scientist_id'],
                planet_id=request.json['planet_id']
            )
            db.session.add(mission)
            db.session.commit()
            
            return mission.to_dict(), 201
        except:
            return {'errors': ['validation errors']}, 400
        
# Add the Signups resource to the API at the /missions endpoint
api.add_resource(Missions, '/missions')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
