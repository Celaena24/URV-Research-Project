from flask import Flask, jsonify, request
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


# Sample ad data
ads = [
    { 'id': 1, 'content': 'Ad 1: Horror Movie!', 'user_rating': None },
    { 'id': 2, 'content': 'Ad 2: Romance Movie!', 'user_rating': None },
    { 'id': 3, 'content': 'Ad 3: Comedy Movie!', 'user_rating': None },
    { 'id': 4, 'content': 'Ad 4: Romantic Comedy Movie!', 'user_rating': None },
    { 'id': 5, 'content': 'Ad 5: Adventure Movie!', 'user_rating': None },
    { 'id': 6, 'content': 'Ad 6: Thriller Movie!', 'user_rating': None },
    { 'id': 7, 'content': 'Ad 7: Award Winning Movie!', 'user_rating': None },
    { 'id': 8, 'content': 'Ad 8: KDrama!', 'user_rating': None },
    { 'id': 9, 'content': 'Ad 9: Critically aclaimed TV show!', 'user_rating': None },
    { 'id': 10, 'content': 'Ad 10: Movie with a strong female lead!', 'user_rating': None }
]



@app.route('/ads', methods=['GET'])
def get_ads():
    selected_ads = random.sample(ads, 3)
    return jsonify(selected_ads)

@app.route('/submit-rating', methods=['POST'])
def submit_rating():
    data = request.json
    ad_id = data.get('id')
    rating = data.get('rating')
    for ad in ads:
        if ad['id'] == ad_id:
            ad['user_rating'] = rating
            break
    return jsonify({"message": "Rating submitted successfully", "ad_id": ad_id, "rating": rating})


if __name__ == '__main__':
    app.run(debug=True)