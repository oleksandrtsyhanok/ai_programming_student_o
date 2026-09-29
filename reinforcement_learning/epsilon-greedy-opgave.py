import numpy as np
import matplotlib.pyplot as plt

def epsilon_greedy(arms, epsilon, num_iterations):
    """
    Voer het epsilon-greedy algoritme uit.

    Args:
        arms (int): Het aantal bandits.
        epsilon (float): De kans om te exploreren (tussen 0 en 1).
        num_iterations (int): Het aantal iteraties om uit te voeren.

    Returns:
        tuple: Gemiddelde beloningen per iteratie, ware beloningen, geselecteerde arm.
    """

    num_arms = arms
    true_rewards = np.random.normal(0, 1, num_arms)  # True rewards voor elke bandit
    estimated_rewards = np.zeros(num_arms)  # geschatte rewards per bandit
    arm_counts = np.zeros(num_arms)  # aantal keren dat een bandit werd gebruikt
    total_reward = 0
    average_rewards = []

    for iteration in range(0, num_iterations):
        # TODO: Kiezen tussen exploreren en exploiteren
        # Gebruik np.random.rand() en epsilon om een IF-statement op te stellen, en kies dan de selected_arm

        # TODO: Simulatie van het spelen op een bandit en update van rewards
        # Gebruik np.random.normal om de reward te simuleren (de reward is een random trekking, met de true_rewards parameter als gemiddelde)

        # TODO: Update geschatte beloningen en berekening van gemiddelde winst
        # Pas de geschatte reward voor de gekozen bandit aan
        pass

    return average_rewards, true_rewards, selected_arm

def plot_results(average_rewards, true_rewards, selected_arm):
    """
    Plot de resultaten van het epsilon-greedy algoritme.
    
    Args:
        average_rewards (list): Gemiddelde rewards over tijd.
        true_rewards (np.array): True rewards van elke arm.
        selected_arm (int): De uiteindelijk geselecteerde bandit.
    """
    plt.plot(average_rewards, label='Gemiddelde Reward')
    plt.plot(true_rewards[selected_arm] * np.ones_like(average_rewards), linestyle='--', label='True Reward (Gekozen Bandit)')
    plt.xlabel('Iteratie')
    plt.ylabel('Reward')
    plt.title('Epsilon-Greedy Algorithm voor Multi-Armed Bandit')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # Parameters
    num_arms = 5
    epsilon = 0.1
    num_iterations = 1000

    # Run epsilon-greedy algorithm
    average_rewards, true_rewards, selected_arm = epsilon_greedy(num_arms, epsilon, num_iterations)

    # Plot results
    plot_results(average_rewards, true_rewards, selected_arm)

