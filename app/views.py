from flask import Flask, request, jsonify
from app.models import RideOffer
from . import app

users = []

@app.route('/api/v1/rides', methods=['POST'])
def create_rideoffer():
    """ This endpoint creates a ride offer """

    data = request.get_json()
    try:
        if isinstance(data['driver'], str) and isinstance(data['destination'], str):
            ride_id = len(users)
            ride_id += 1
            Ride = RideOffer(ride_id, data['driver'], data['destination'])
            users.append(Ride)
        return jsonify(Ride.get_dict()), 201

    except AttributeError:
        return jsonify({
            'status': 'fail',
            'message': 'failed to create a request. Invalid data'
        }), 400


@app.route('/api/v1/rides', methods=['GET'])
def fetch_all_rides():
    """This endpoint fetches all rides"""
    rides = [ride.get_dict() for ride in users]
    return jsonify({'Rides': rides}), 200


@app.route('/api/v1/rides/<int:ride_id>', methods=['GET'])
def fetch_ride_id(ride_id):
    fetch_rides = []
    data = users
    for obj in users:
        if int(ride_id) > len(data):
            return jsonify({
                'status': 'fail',
                'message': 'ID not found. Please add a valid ID'
            }), 400
        obj = data[int(ride_id)-1]
        fetch_rides.append(obj.get_dict())
        return jsonify({
            'status': 'Success',
            'request': fetch_rides
        }), 200


@app.route('/api/v1/rides/<int:ride_id>/requests', methods=['POST'])
def request_ride_id(ride_id):
    request_ride = []
    if ride_id == 0 or ride_id > len(users):
        return jsonify({"Message":"Index out of range"}), 400
    
    if ride_id !=0 and ride_id <= len(users):
        ride = users[ride_id-1]
        request_ride.append(ride.get_dict())
        return jsonify({"requested_ride":request_ride,"status":"ride" + str(ride_id)+"successfully requested"}),200
