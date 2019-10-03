import firebase_admin
from firebase_admin import credentials, db
import flask
from flask import Flask, request, jsonify

app = Flask(__name__)

# Fetch the service account key JSON file contents
cred = credentials.Certificate('./service-account-key.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://<db-name>.firebaseio.com'
})

# As an admin, the app has access to read and write all data, regradless of Security Rules
CARS = db.reference('cars')

@app.route('/cars', methods=['GET','POST'])
def create_or_get_cars():
    if request.method == 'GET':
        # Retrieve all cars
        return jsonify( CARS.get()), 200
    if request.method == 'POST':
        # Create a new car
        req = request.json
        car = CARS.push(req)
        return jsonify({'id': car.key}), 201

# retrieve info about a specific car by id
@app.route('/cars/<id>', methods=['GET'])
def read_car(id):
    return jsonify(_ensure_car(id))

#update a car
@app.route('/cars/<id>', methods=['PUT'])
def update_car(id):
    _ensure_car(id)
    req = request.json
    CARS.child(id).update(req)
    return jsonify({'info': 'car updated'})

#delete a car
@app.route('/cars/<id>', methods=['DELETE'])
def delete_car(id):
    _ensure_car(id)
    CARS.child(id).delete()
    return jsonify({'info':'Car deleted'})

# verify that exist a car's id
def _ensure_car(id):
    car = CARS.child(id).get()
    if not car:
        flask.abort(404)
    return car

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)