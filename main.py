from flask import Flask, request, jsonify
# from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

#connects to the database
db = PostgresqlDatabase('people', user='buccolt45', password='12345',
                        host='localhost', port=5432)

#creates a base model class that specifies which database to use
class BaseModel(Model):
    class Meta:
        database = db

#creates a person class that inherits from the base model
class Person(BaseModel):
    name = CharField()
    phone = IntegerField()

#connects to the database, drops the table if it exists, and creates a new table
db.connect()
db.drop_tables([Person])
db.create_tables([Person])

#creates a list of people
for person in Person:
    Person (
        name = Person['name'],
        phone = Person['phone']
    ).save()

#creates a flask app
app = Flask(__name__)

#creates a route for the root of the api
@app.route('/')
def index():
    return jsonify({'message': 'This is the API root'})

#creates a route for the people endpoint
@app.route('/person', methods=['GET', 'PUT'])

#creates a function for the people endpoint
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

#runs the app
app.run(port=3030, debug=True)