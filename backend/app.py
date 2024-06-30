from flask import Flask, jsonify, request
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


# Sample ad data
ads = [
    { 'id': 1, 'content': 'Ad 1: Horror Movie!' },
    { 'id': 2, 'content': 'Ad 2: Romance Movie!' },
    { 'id': 3, 'content': 'Ad 3: Comedy Movie!' },
    { 'id': 4, 'content': 'Ad 4: Romantic Comedy Movie!' },
    { 'id': 5, 'content': 'Ad 5: Adventure Movie!' },
    { 'id': 6, 'content': 'Ad 6: Thriller Movie!' },
    { 'id': 7, 'content': 'Ad 7: Award Winning Movie!' },
    { 'id': 8, 'content': 'Ad 8: KDrama!' },
    { 'id': 9, 'content': 'Ad 9: Critically aclaimed TV show!' },
    { 'id': 10, 'content': 'Ad 10: Movie with a strong female lead!' }
]


@app.route('/ads', methods=['GET'])
def get_ads():
    selected_ads = random.sample(ads, 3)
    return jsonify(selected_ads)


if __name__ == '__main__':
    app.run(debug=True)