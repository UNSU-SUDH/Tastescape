from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

db = mysql.connector.connect(
    host="localhost", user="root", password="unsu@123", database="tastescape"
)
cursor = db.cursor(dictionary=True)

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    cursor.execute("SELECT * FROM restaurants")
    return jsonify(cursor.fetchall())

@app.route('/restaurants', methods=['POST'])
def add_restaurant():
    data = request.json
    cursor.execute("INSERT INTO restaurants (name) VALUES (%s)", (data['name'],))
    db.commit()
    return jsonify({'status': 'added'})

@app.route('/reviews/<int:restaurant_id>', methods=['GET'])
def get_reviews(restaurant_id):
    cursor.execute("SELECT * FROM reviews WHERE restaurant_id = %s", (restaurant_id,))
    return jsonify(cursor.fetchall())

@app.route('/reviews', methods=['POST'])
def add_review():
    data = request.json
    cursor.execute("INSERT INTO reviews (restaurant_id, user, rating, comment) VALUES (%s, %s, %s, %s)",
                   (data['restaurant_id'], data['user'], data['rating'], data['comment']))
    db.commit()
    return jsonify({'status': 'review added'})

@app.route('/dishes', methods=['GET'])
def get_dishes():
    cursor.execute("SELECT * FROM dishes")
    return jsonify(cursor.fetchall())

if __name__ == '__main__':
    app.run(debug=True)
