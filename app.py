from flask import Flask, request, jsonify, render_template
import csv
import os

app = Flask(__name__)

FOOD_FILE = 'food.csv'
POINTS_FILE = 'points.csv'

# Read CSV data
def read_csv(file):
    data = []
    with open(file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

# Write CSV data
def write_csv(file, data, fieldnames):
    with open(file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/food', methods=['GET', 'POST', 'DELETE', 'PUT'])
def manage_food():
    if request.method == 'GET':
        food_data = read_csv(FOOD_FILE)
        return jsonify(food_data)
    
    elif request.method == 'POST':
        new_entry = request.json
        food_data = read_csv(FOOD_FILE)
        food_data.append(new_entry)
        write_csv(FOOD_FILE, food_data, fieldnames=['food', 'quantity', 'price'])
        return jsonify({'message': 'Entry added successfully!'}), 201
    
    elif request.method == 'DELETE':
        food_to_remove = request.json['food']
        food_data = read_csv(FOOD_FILE)
        food_data = [item for item in food_data if item['food'] != food_to_remove]
        write_csv(FOOD_FILE, food_data, fieldnames=['food', 'quantity', 'price'])
        return jsonify({'message': 'Entry removed successfully!'})
    
    elif request.method == 'PUT':
        updated_entry = request.json
        food_to_update = updated_entry['food']
        food_data = read_csv(FOOD_FILE)
        for item in food_data:
            if item['food'] == food_to_update:
                item['quantity'] = updated_entry['quantity']
                item['price'] = updated_entry['price']
        write_csv(FOOD_FILE, food_data, fieldnames=['food', 'quantity', 'price'])
        return jsonify({'message': 'Entry updated successfully!'})

@app.route('/points', methods=['GET'])
def get_points():
    points_data = read_csv(POINTS_FILE)
    return jsonify(points_data)

if __name__ == '__main__':
    app.run(debug=True)
