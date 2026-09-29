Excellent choice—Option 6 (evolutionary agent designer) ties beautifully into your GA week and gives a **true “agents that design agents”** flavor.

Below is a **complete, minimal working example**:

👉 Agents are **evaluation functions for Tic-Tac-Toe**  
👉 A genetic algorithm evolves them  
👉 They compete against each other  
👉 You observe improvement over generations

***

# 📁 Folder structure

    evolutionary_agent/
    │
    ├── environment.py
    ├── agent.py
    ├── evolution.py
    └── main.py

***

# 🎮 `environment.py` — Tic-Tac-Toe

```python
class TicTacToe:
    def __init__(self):
        self.board = [" "] * 9

    def copy(self):
        new = TicTacToe()
        new.board = self.board[:]
        return new

    def available_actions(self):
        return [i for i, v in enumerate(self.board) if v == " "]

    def make_move(self, action, player):
        if self.board[action] == " ":
            self.board[action] = player
            return True
        return False

    def check_winner(self):
        wins = [
            (0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)
        ]
        for a,b,c in wins:
            if self.board[a] == self.board[b] == self.board[c] != " ":
                return self.board[a]
        if " " not in self.board:
            return "draw"
        return None
```

***

# 🤖 `agent.py` — genome = evaluation function

Each agent is just **weights** for a heuristic.

```python
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
```

***

# 🧬 `evolution.py` — genetic algorithm

```python
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
```

***

# ▶️ `main.py` — run evolution

```python
from agent import EvoAgent
from evolution import evolve


if __name__ == "__main__":
    # initial population
    population = [EvoAgent() for _ in range(20)]

    # evolve
    population = evolve(population, generations=15)

    # best agent
    best = population[0]

    print("\nBest agent weights:")
    print(best.weights)
```

***

# ✅ What students will observe

### Early generations:

*   random play
*   bad strategy

### Later:

*   prefers center
*   blocks opponent
*   wins more frequently

👉 **emergent behavior from evolution**

***

# 🧠 What this teaches (very important)

| Concept               | Where                   |
| --------------------- | ----------------------- |
| genetic algorithms    | evolve()                |
| agents                | EvoAgent                |
| evaluation functions  | weights                 |
| emergent intelligence | improved play           |
| meta-design           | agents designing agents |

***

# 🚀 Powerful extensions (highly recommended)

## 🔹 1. Add minimax hybrid

Use evolved weights inside minimax:

```python
score = heuristic(board, weights)
```

***

## 🔹 2. Co-evolution

Split population:

*   attackers vs defenders

***

## 🔹 3. More features

Extend genome:

```python
"corner": weight,
"two_in_row": weight,
"fork": weight
```

***

## 🔹 4. Tournament selection

Instead of random matches → bracket tournament

***

## 🔹 5. Visualization

Print best agent playing games:

```python
env.render()
```

***

# 🎯 Why this is PERFECT for your course

It connects:

*   genetic algorithms ✅
*   adversarial games ✅
*   agent design ✅

👉 and introduces:

> *designing intelligence instead of coding it*

***

# 🏁 If you want next step


✅ upgrade to **neural network agents (neuroevolution)**  
✅ add **graphs showing improvement over generations**  
✅ build a **competition assignment for students**  
✅ combine with RL → **evolution + learning hybrid**

