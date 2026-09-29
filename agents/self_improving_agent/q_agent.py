import random

class QAgent:
    def __init__(self, alpha=0.5, gamma=0.9, epsilon=0.2):
        self.q = {}  # (state, action) → value
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def get_state(self, env):
        return tuple(env.board)

    def get_q(self, state, action):
        return self.q.get((state, action), 0.0)

    def choose_action(self, env):
        state = self.get_state(env)
        actions = env.available_actions()

        if random.random() < self.epsilon:
            return random.choice(actions)

        qs = [self.get_q(state, a) for a in actions]
        max_q = max(qs)
        best = [a for a, q in zip(actions, qs) if q == max_q]
        return random.choice(best)

    def update(self, state, action, reward, next_state, next_actions):
        max_future = max([self.get_q(next_state, a) for a in next_actions], default=0)

        old = self.get_q(state, action)
        new = old + self.alpha * (reward + self.gamma * max_future - old)

        self.q[(state, action)] = new