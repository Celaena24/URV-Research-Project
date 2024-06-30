class Agent:
    def __init__(self, name, dob, location, agent_type):
        self.name = name
        self.dob = dob
        self.location = location
        self.agent_type = agent_type
        self.reward_distributions = [self.generate_reward_distribution() for _ in range(10)]
        
    def generate_reward_distribution(self):
        pass


class Rewards:
    def additive(self):
        pass
    
    def multiplicative(self):
        pass
    
    def linear(self):
        pass
    
    
class Ad:
    def __init__(self, name, genre, age_restriction, score):
        self.name = name
        self.genre = genre
        self.age_restriction = age_restriction
        self.score = zmelb_score