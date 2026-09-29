import gym
import numpy as np
import matplotlib.pyplot as plt

# Initialize the Gym environment
env = gym.make('Taxi-v3', render_mode="ansi")
state = env.reset()

# Initialize the Q-table
Q_table = np.zeros([env.observation_space.n, env.action_space.n])

# Q-learning parameters
learning_rate = 0.1
discount_factor = 0.9
num_episodes = 1000
max_steps_per_episode = 99

# For plotting metrics
rewards_all_episodes = []

# Q-learning algorithm
for episode in range(num_episodes):
    initial_state = env.reset()
    state = initial_state[0] if isinstance(initial_state, tuple) else initial_state  # Extract the integer part
    total_rewards = 0

    for step in range(max_steps_per_episode):
        # Exploration vs exploitation
        exploration_rate = 1 - episode / num_episodes
        if np.random.uniform(0, 1) < exploration_rate:
            action = env.action_space.sample()
        else:
            action = np.argmax(Q_table[state, :])

        # Take action and observe the result
        new_state, reward, terminated, truncated, _ = env.step(action)
        env.render()

        # Update Q-table
        Q_table[state, action] = Q_table[state, action] * (1 - learning_rate) + \
                                 learning_rate * (reward + discount_factor * np.max(Q_table[new_state, :]))

        total_rewards += reward
        state = new_state

        if terminated or truncated:
            break

    rewards_all_episodes.append(total_rewards)

# Calculate and print the average reward
average_reward = sum(rewards_all_episodes) / num_episodes
print(f"Average Reward: {average_reward}")

# Plotting the learning progress
plt.plot(rewards_all_episodes)
plt.xlabel('Episodes')
plt.ylabel('Rewards')
plt.title('Rewards per Episode Over Time')
plt.show()
