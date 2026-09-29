import gymnasium as gym
import numpy as np

# Create the environment
env = gym.make('CartPole-v1')

# Hyperparameters
alpha = 0.1  # Learning rate
gamma = 0.99  # Discount factor
epsilon = 1.0  # Exploration rate
epsilon_decay = 0.995
epsilon_min = 0.01
num_bins = 10  # Number of bins for discretization

# Discretize the state space
state_bins = [
    np.linspace(-4.8, 4.8, num_bins),  # Cart position
    np.linspace(-4, 4, num_bins),       # Cart velocity
    np.linspace(-0.418, 0.418, num_bins),  # Pole angle
    np.linspace(-4, 4, num_bins)        # Pole angular velocity
]

# Initialize Q-table
Q = np.zeros([num_bins, num_bins, num_bins, num_bins, env.action_space.n])

def discretize_state(state):
    state_idx = []
    for i in range(len(state)):
        state_idx.append(np.digitize(state[i], state_bins[i]) - 1)
    return tuple(state_idx)

# Training loop
for episode in range(1000):
    state, _ = env.reset()
    state = discretize_state(state)
    done = False

    while not done:
        if np.random.rand() < epsilon:
            action = env.action_space.sample()  # Explore
        else:
            action = np.argmax(Q[state])  # Exploit

        next_state, reward, terminated, truncated, _ = env.step(action)
        next_state = discretize_state(next_state)
        done = terminated or truncated

        # Q-Learning update
        Q[state + (action,)] = (1 - alpha) * Q[state + (action,)] + alpha * (reward + gamma * np.max(Q[next_state]))

        state = next_state

        # Decay epsilon
        epsilon = max(epsilon_min, epsilon * epsilon_decay)

    if episode % 100 == 0:
        print(f"Episode {episode} completed")

# Close the environment
env.close()
