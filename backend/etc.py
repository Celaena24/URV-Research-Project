import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linear_sum_assignment
import time


class Ad:
    def __init__(self, name, genre, age_restriction, score):
        self.name = name
        self.genre = genre
        self.age_restriction = age_restriction
        self.score = score
        self.reward_distribution = 0  # Placeholder for reward distribution


class Agent:
    def __init__(self, name, date_of_birth, location, agent_type):
        self.name = name
        self.date_of_birth = date_of_birth
        self.location = location
        self.agent_type = agent_type
        self.reward_distributions = []

    def generate_reward_distributions(self, ads):
        self.reward_distributions = [np.random.uniform(0, 1) for _ in ads]
        for ad, reward in zip(ads, self.reward_distributions):
            ad.reward_distribution = reward

    # Default way for generating optimal reward for agent - 1st slot = highest reward, 2nd slot = 2nd highest reward, etc.
    def optimal_reward_sort(self, ads, num_slots):
        sorted_ads = sorted(ads, key=lambda x: x.reward_distribution, reverse=True)
        optimal_combination = [
            sorted_ads[i].reward_distribution for i in range(num_slots)
        ]
        return optimal_combination


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



def ETC(ads, num_slots, total_steps, delta, agent):
    
    num_ads = len(ads)
    optimal_combination = agent.optimal_reward_sort(ads, num_slots)
    print("Optimal combo: ", optimal_combination)
    print("-------------------")
    regret = np.zeros(total_steps)
    emp_means = np.zeros((num_slots, num_ads))
    num_pulls = np.zeros((num_slots, num_ads))
    num_steps = 0
    m = int(
        np.ceil(max(1, (9 / (4 * delta**2)) * np.log((total_steps * delta**2) / 4)))
    )
    print("m: ", m)
    print("-------------------")

    # Pure Exploration Phase
    for slot in range(num_slots):
        for ad in range(num_ads):
            for _ in range(m):
                if num_steps >= total_steps:
                    break
                num_pulls[slot][ad] += 1
                reward = np.random.binomial(1, ads[ad].reward_distribution)
                emp_means[slot][ad] += (reward - emp_means[slot][ad]) / num_pulls[slot][
                    ad
                ]
                regret[num_steps] += (
                    optimal_combination[slot] - ads[ad].reward_distribution
                )
                # NOTE: these print definitions show how ads/slots can be chosen at each time step for website connection
                # Print the selected ad/edge and two arbitrary ads for other slots
                # print(f"Step {num_steps}: Slot {slot+1}: {ads[ad].name} (playing), "
                #       f"Slot {((slot+1)%num_slots)+1}: {ads[np.random.randint(num_ads)].name} (arbitrary), "
                #       f"Slot {((slot+2)%num_slots)+1}: {ads[np.random.randint(num_ads)].name} (arbitrary)")
                num_steps += 1
        if num_steps >= total_steps:
            break

    # Pure Exploitation Phase
    cost_matrix = -emp_means  # We need to maximize the reward
    print("cost_matrix ", cost_matrix)
    print("-------------------")
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    selected_combination = col_ind[:num_slots]

    # Print selected combination
    for ad_index in selected_combination:
        print(ads[ad_index].name + ", " + str(ads[ad_index].reward_distribution)) 
    print(selected_combination)
    print("-------------------")
    print("Total steps used for exploration:", num_steps)
    print("-------------------")

    while num_steps < total_steps:
        for slot in range(num_slots):
            if num_steps >= total_steps:
                break
            selected_ad = selected_combination[slot]
            regret[num_steps] += (
                optimal_combination[slot] - ads[selected_ad].reward_distribution
            )
            num_steps += 1

    return [regret, selected_combination]


if __name__ == "__main__":
    
    # Print ads
    print("-------------------")
    sorted_ads = sorted(ads, key=lambda obj: obj.reward_distribution, reverse=True)
    print("Ads sorted by highest reward distribution:")
    for ad in sorted_ads:
        print(ad.name + " " + str(ad.reward_distribution))
    print("-------------------")

    # Simulation parameters
    num_slots = 3
    num_steps_list = [20000]  # Horizon or total number of steps in the experiment
    delta = 0.2  # gap, higher value = lower m

    # Measure execution time
    start_time = time.time()

    # Plot the regret curves
    fig, ax = plt.subplots(figsize=(10, 5))

    for n in num_steps_list:
        regret, selected_combination = ETC(ads, num_slots, n, delta, agent)
        cum_regret = np.cumsum(regret)
        ax.plot(np.arange(n), cum_regret, label=f"n={n}, delta={delta}")

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



    