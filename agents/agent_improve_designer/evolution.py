import random
from environment import TicTacToe


def play_game(agent1, agent2):
    env = TicTacToe()
    players = [("O", agent1), ("X", agent2)]

    turn = 0

    while True:
        symbol, agent = players[turn % 2]

        action = agent.choose_action(env)
        env.make_move(action, symbol)

        winner = env.check_winner()
        if winner:
            return winner

        turn += 1


def evaluate(agent, population, games=5):
    score = 0
    for _ in range(games):
        opponent = random.choice(population)
        result = play_game(agent, opponent)

        if result == "O":
            score += 1
        elif result == "X":
            score -= 1
    return score


def evolve(population, generations=20, retain=0.3):
    for gen in range(generations):
        scored = [(evaluate(agent, population), agent) for agent in population]
        scored.sort(reverse=True, key=lambda x: x[0])

        print(f"\nGeneration {gen}")
        print("Best score:", scored[0][0])

        # selection
        retain_length = int(len(scored) * retain)
        parents = [agent for _, agent in scored[:retain_length]]

        # reproduction
        children = []
        while len(children) < len(population) - retain_length:
            p1, p2 = random.sample(parents, 2)
            child = p1.crossover(p2)

            if random.random() < 0.3:
                child = child.mutate()

            children.append(child)

        population = parents + children

    return population