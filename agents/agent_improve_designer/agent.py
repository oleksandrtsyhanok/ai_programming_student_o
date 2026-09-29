import random

class EvoAgent:
    def __init__(self, weights=None):
        # weights define behavior
        self.weights = weights or {
            "win": random.uniform(5, 10),
            "block": random.uniform(3, 7),
            "center": random.uniform(0, 3),
            "random": random.uniform(0, 1)
        }

    def evaluate_move(self, env, action):
        score = 0
        temp = env.copy()
        temp.make_move(action, "O")

        winner = temp.check_winner()
        if winner == "O":
            score += self.weights["win"]

        # blocking behavior
        temp2 = env.copy()
        temp2.make_move(action, "X")
        if temp2.check_winner() == "X":
            score += self.weights["block"]

        if action == 4:
            score += self.weights["center"]

        score += random.random() * self.weights["random"]

        return score

    def choose_action(self, env):
        actions = env.available_actions()
        scores = [(self.evaluate_move(env, a), a) for a in actions]
        return max(scores)[1]

    def mutate(self, rate=0.2):
        new_weights = self.weights.copy()
        for k in new_weights:
            if random.random() < rate:
                new_weights[k] += random.uniform(-1, 1)
        return EvoAgent(new_weights)

    def crossover(self, other):
        new_weights = {}
        for k in self.weights:
            new_weights[k] = random.choice([self.weights[k], other.weights[k]])
        return EvoAgent(new_weights)