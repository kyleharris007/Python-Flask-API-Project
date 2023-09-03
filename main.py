from flask import Flask, request, jsonify
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model
from people import Person

db = PostgresqlDatabase('people', user='buccolt45', password='12345',
                        host='localhost', port=5432)

class BaseModel(Model):
    class Meta:
        database = db

class Person(BaseModel):
    name = CharField()
    phone = IntegerField()

db.connect()
db.drop_tables([Person])
db.create_tables([Person])

for person in Person:
    Person (
        name = Person['name'],
        phone = Person['phone']
    ).save()

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'message': 'This is the API root'})

@app.route('/person', methods=['GET', 'PUT'])

@app.route('/person/<id>', methods=['GET', 'PUT', 'DELETE'])
def person(id=None):
    if request.method == 'GET':
        if id:
            try:
                return jsonify(model_to_dict(Person.get(Person.id == id)))
            except Person.DoesNotExist:
                return jsonify({'error': 'Person not found'})
            
        else:
            person = []

            for person in Person.select():
                person.append(model_to_dict(person))

            return jsonify(person)
        
    elif request.method == 'POST':
        try:
            new_person = dict_to_model(Person, request.get_json())
            new_person.save()
            return jsonify(model_to_dict(new_person))

        except IntegrityError:
            return jsonify({'error: Invalid'})
        
    elif request.method == 'PUT':
        Person.update(request.get_json()).where(Person.id).execute()
        return jsonify(model_to_dict(Person.get(Person.id == id)))
    
    elif request.method == 'DELETE':
        try:
            Person.get(Person.id == id)
            Person.delete().where(Person.id == id).execute()
            return jsonify({'message': 'Person deleted'})
    
        except DoesNotExist:
            return jsonify({'error': 'Person not found'})

    






# def endpoint():
#     if request.method == 'GET':
#         return 'GET request'
#     if request.method == 'PUT':
#         return 'PUT request'
#     if request.method == 'POST':
#         return 'POST request'
#     if request.method == 'DELETE':
#         return 'DELETE request'
    
# @app.route('/get-json')
# def get_json():
#     return jsonify({
#         "name": "Garfield",
#         "hatesMondays": True,
#         "friends": ["Sheldon", "wade", "Orson", "Squeak"]
#     })


app.run(port=3030, debug=True)