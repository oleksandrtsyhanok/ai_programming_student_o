from environment import TicTacToe
from q_agent import QAgent
from minimax import minimax
from opponent import random_opponent


def play_game(agent, opponent_func, training=True):
    env = TicTacToe()

    while True:
        # --- Agent (O) ---
        state = agent.get_state(env)
        action = agent.choose_action(env)

        env.make_move(action, "O")
        winner = env.check_winner()

        if winner:
            reward = 1 if winner == "O" else -1 if winner == "X" else 0
            if training:
                agent.update(state, action, reward, (), [])
            return winner

        # --- Opponent (X) ---
        opp_action = opponent_func(env)
        env.make_move(opp_action, "X")

        winner = env.check_winner()

        next_state = agent.get_state(env)
        next_actions = env.available_actions()

        if training:
            reward = 1 if winner == "O" else -1 if winner == "X" else 0 if winner else 0
            agent.update(state, action, reward, next_state, next_actions)

        if winner:
            return winner


def minimax_opponent(env):
    _, move = minimax(env, "X")
    return move


if __name__ == "__main__":
    agent = QAgent()

    # --- Training phase --- adaptieve agent speelt tegen random tegenstander en leert van de resultaten
    print("Training agent...")
    for i in range(5000):
        play_game(agent, random_opponent, training=True)

        if i % 1000 == 0:
            print(f"Game {i}")

    # reduce exploration
    agent.epsilon = 0.05

    # --- Evaluation vs random ---
    print("\nTesting vs random opponent")
    results = {"O":0, "X":0, "draw":0}

    for _ in range(200):
        w = play_game(agent, random_opponent, training=False)
        results[w] += 1

    print("Results:", results)

    # --- Evaluation vs minimax ---
    print("\nTesting vs minimax")
    results = {"O":0, "X":0, "draw":0}

    for _ in range(100):
        w = play_game(agent, minimax_opponent, training=False)
        results[w] += 1

    print("Results:", results)