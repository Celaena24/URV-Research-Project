from flask import Flask, jsonify, request
from flask_cors import CORS
from etc import Ad, Agent, ETC
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


# Sample ad data
ads = [
    Ad("Ad 0: Horror Movie!", "Horror", 18, 7.5),
    Ad("Ad 1: Romance Movie!", "Romance", 13, 6.8),
    Ad("Ad 2: Comedy Movie!", "Comedy", 13, 7.2),
    Ad("Ad 3: Romantic Comedy Movie!", "Romantic Comedy", 13, 6.9),
    Ad("Ad 4: Adventure Movie!", "Adventure", 13, 7.8),
    Ad("Ad 5: Thriller Movie!", "Thriller", 18, 7.0),
    Ad("Ad 6: Award Winning Movie!", "Drama", 18, 8.5),
    Ad("Ad 7: KDrama!", "Drama", 13, 7.3),
    Ad("Ad 8: Critically acclaimed TV show!", "TV Show", 18, 8.0),
    Ad("Ad 9: Movie with a strong female lead!", "Drama", 13, 7.6),
]

# Sample agent data
agent = Agent(
    name="Test Agent", date_of_birth="1990-01-01", location="USA", agent_type="test"
)

# Generate reward distributions
agent.generate_reward_distributions(ads)

ads_json = []
for ad in ads:
    dic = {}
    dic["name"] = ad.name
    dic["genre"] = ad.genre
    dic["age_restriction"] = ad.age_restriction
    dic["score"] = ad.score
    dic["reward"] = ad.reward_distribution
    ads_json.append(dic)

sorted_ads = sorted(ads_json, key=lambda obj: obj["reward"], reverse=True)
print(sorted_ads)

num_slots = 3
n = 20000
delta = 0.2


@app.route('/ads', methods=['GET'])
def get_ads():
    regret, selected_combination = ETC(ads, num_slots, n, delta, agent)
    selected_ads = []
    for index in selected_combination:
        selected_ads.append(ads_json[index])
    return jsonify(selected_ads)

@app.route('/all_ads', methods=['GET'])
def all_ads():
    return jsonify(sorted_ads)


if __name__ == '__main__':
    app.run(debug=True)