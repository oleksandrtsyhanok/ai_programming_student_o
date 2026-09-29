# Oefening 1 — oplossing + stappenplan

## Doel

De agent leert zelf kiezen tussen:

*   bfs
*   dfs
*   astar
*   annealing

m.b.v. **ε-greedy (bandit)**.

***

# Stappenplan (hoe beginnen)

1.  **Begin met bestaande Agent**
    *   Je hebt al:
    ```python
    self.tools = { ... }
    ```

2.  **Voeg statistieken toe**
    *   per methode:
    ```python
    self.values[method]     # gemiddelde score
    self.counts[method]     # aantal keer gebruikt
    ```

3.  **Definieer beloning**
    Kies iets eenvoudigs:

    *   kort pad = goed
    *   geen oplossing = slecht

    Bijvoorbeeld:

    ```python
    reward = -len(path)
    ```

4.  **Implementeer ε-greedy**
    *   met kans ε: random tool
    *   anders: beste gemiddelde score

5.  **Update na elke run**
    *   pas gemiddelde aan (incremental average)

***

# Voorbeeldoplossing (agent.py)

```python
import random
from bfs import bfs
from dfs import dfs
from astar import astar
from annealing import simulated_annealing


class LearningAgent:
    def __init__(self, epsilon=0.2):
        self.tools = {
            "bfs": bfs,
            "dfs": dfs,
            "astar": astar,
            "annealing": simulated_annealing
        }

        self.epsilon = epsilon

        # statistics
        self.values = {k: 0.0 for k in self.tools}
        self.counts = {k: 0 for k in self.tools}

    def choose_tool(self):
        # exploration
        if random.random() < self.epsilon:
            return random.choice(list(self.tools.keys()))

        # exploitation
        return max(self.values, key=self.values.get)

    def update(self, method, reward):
        self.counts[method] += 1
        n = self.counts[method]

        # incremental average update
        old = self.values[method]
        self.values[method] = old + (reward - old) / n

    def solve(self, problem):
        method = self.choose_tool()
        solver = self.tools[method]

        path = solver(problem)

        # reward
        if path is None:
            reward = -100  # heavy penalty
        else:
            reward = -len(path)

        self.update(method, reward)

        print(f"{method}: reward={reward:.2f}, avg={self.values.2f}")

        return path
```

***

# Training loop (main.py uitbreiding)

```python
agent = LearningAgent()

for i in range(100):
    problem = GridProblem(
        width=5,
        height=5,
        start=(0,0),
        goal=(4,4),
        obstacles={(1,1), (2,2)}
    )

    agent.solve(problem)

print("\nLearned values:")
print(agent.values)
```

***

# Wat je verwacht te zien

Na training:

*   BFS/A\* → betere scores (kort pad)
*   DFS → slechter
*   Annealing → wisselend

agent gaat automatisch betere tools kiezen

***

# Mogelijke verbeteringen (voor studenten)

*   maak reward:
    ```python
    reward = -len(path) - alpha * runtime
    ```
*   gebruik context:
    ```python
    state_size → aparte statistics
    ```
*   decay ε:
    ```python
    epsilon *= 0.99
    ```

***

# Belangrijk concept

Dit **is een bandit-probleem**:

*   acties = algoritmes
*   reward = performance

agent leert *welk algoritme wanneer werkt*

***

