import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linear_sum_assignment
import time

start_time = time.time()


class Agent:
    def __init__(self, name, dob, location, agent_type):
        self.name = name
        self.dob = dob
        self.location = location
        self.agent_type = agent_type
        self.reward_distributions = [
            self.generate_reward_distribution() for _ in range(10)
        ]

    def generate_reward_distribution(self):
        return np.random.uniform(0, 1)


class Rewards:
    def additive(self, rewards):
        return np.sum(rewards)

    def multiplicative(self, rewards):
        return np.prod(rewards)

    def linear(self, rewards):
        pass


class Ad:
    def __init__(self, name, genre, age_restriction, score):
        self.name = name
        self.genre = genre
        self.age_restriction = age_restriction
        self.score = score


# Sample ad data
ads = [
    Ad("Ad 1: Horror Movie!", "Horror", 18, 7.5),
    Ad("Ad 2: Romance Movie!", "Romance", 13, 6.8),
    Ad("Ad 3: Comedy Movie!", "Comedy", 13, 7.2),
    Ad("Ad 4: Romantic Comedy Movie!", "Romantic Comedy", 13, 6.9),
    Ad("Ad 5: Adventure Movie!", "Adventure", 13, 7.8),
    Ad("Ad 6: Thriller Movie!", "Thriller", 18, 7.0),
    Ad("Ad 7: Award Winning Movie!", "Drama", 18, 8.5),
    Ad("Ad 8: KDrama!", "Drama", 13, 7.3),
    Ad("Ad 9: Critically acclaimed TV show!", "TV Show", 18, 8.0),
    Ad("Ad 10: Movie with a strong female lead!", "Drama", 13, 7.6),
]

# Initialize an agent
agent = Agent(name="Test Agent", dob="1990-01-01", location="USA", agent_type="test")

# Assign reward distributions to each ad
for i, ad in enumerate(ads):
    ad.reward_distribution = agent.reward_distributions[i]

for ad in ads:
    print(ad.name + " " + str(ad.reward_distribution))


# Function to calculate ETC regret with Hungarian algorithm
def ETC(ads, num_slots, total_steps, m, reward_function):
    num_ads = len(ads)
    optimal_combination = np.argmax([ad.reward_distribution for ad in ads])
    regret = np.zeros(total_steps)
    emp_means = np.zeros((num_slots, num_ads))
    num_pulls = np.zeros((num_slots, num_ads))
    num_steps = 0

    # Pure Exploration Phase
    for slot in range(num_slots):
        for ad in range(num_ads):
            for _ in range(m):
                if num_steps >= total_steps:
                    break
                num_pulls[slot][ad] += 1
                reward = reward_function([np.random.binomial(1, ads[ad].reward_distribution)])
                emp_means[slot][ad] += (reward - emp_means[slot][ad]) / num_pulls[slot][ad]
                regret[num_steps] += (
                    ads[optimal_combination].reward_distribution
                    - ads[ad].reward_distribution
                )
                num_steps += 1
        if num_steps >= total_steps:
            break

    # Pure Exploitation Phase
    cost_matrix = -emp_means  # We need to maximize the reward
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    selected_combination = col_ind[:num_slots]

    while num_steps < total_steps:
        for slot in range(num_slots):
            if num_steps >= total_steps:
                break
            selected_ad = selected_combination[slot]
            regret[num_steps] += (
                ads[optimal_combination].reward_distribution
                - ads[selected_ad].reward_distribution
            )
            num_steps += 1

    return regret


# Simulation parameters
num_slots = 3
num_steps_list = [20000]  # Horizon or total number of steps in the experiment
m_exp = [100, 500, 1000]  # Number of times each arm is pulled in pure exploration phase

rewards = Rewards()

# Plot the regret curves
fig, ax = plt.subplots(figsize=(10, 5))

for n in num_steps_list:
    for m in m_exp:
        regret = ETC(ads, num_slots, n, m, rewards.additive)
        cum_regret = np.cumsum(regret)
        ax.plot(np.arange(n), cum_regret, label=f"n={n}, m={m}")

ax.set_title(f"Number of slots={num_slots}")
ax.legend()
ax.set_xlabel("Number of time steps")
ax.set_ylabel("Cumulative Regret")
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontsize(8)

fig.suptitle("ETC Algorithm with Hungarian Optimization")

end_time = time.time()
print(f"Execution time: {end_time - start_time} seconds")

plt.show()
