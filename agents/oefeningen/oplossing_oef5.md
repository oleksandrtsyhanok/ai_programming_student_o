Hier is **Oefening 5 — oplossing + stappenplan** (evolutionaire agent verbeteren).

***

# Oefening 5 — evolutionaire agent verbeteren

## Stappenplan

1.  **Start van bestaande EvoAgent**
    *   huidige features:
    ```python
    "win", "block", "center", "random"
    ```

2.  **Breid het genotype uit**
    *   voeg nieuwe strategische features toe
    *   denk: “wat maakt een goede Tic-Tac-Toe speler?”

3.  **Pas evaluatiefunctie aan**
    *   gebruik nieuwe features bij scoring

4.  **Verbeter selectieproces**
    *   vervang random tegenstanders door **tournament selection**

5.  **Meet evolutie**
    *   track beste en gemiddelde fitness per generatie

***

# Voorbeeldoplossing

## Stap 1 — uitgebreid genotype (`agent.py`)

```python
class EvoAgent:
    def __init__(self, weights=None):
        self.weights = weights or {
            "win": random.uniform(5, 10),
            "block": random.uniform(3, 7),
            "center": random.uniform(0, 3),
            "corner": random.uniform(0, 3),
            "two_in_row": random.uniform(1, 5),
            "random": random.uniform(0, 1)
        }
```

***

## Stap 2 — extra features gebruiken

```python
def count_two_in_row(board, player):
    lines = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]

    count = 0
    for a, b, c in lines:
        line = [board[a], board[b], board[c]]
        if line.count(player) == 2 and line.count(" ") == 1:
            count += 1
    return count
```

***

### Aangepaste evaluatie

```python
def evaluate_move(self, env, action):
    score = 0

    temp = env.copy()
    temp.make_move(action, "O")

    winner = temp.check_winner()
    if winner == "O":
        score += self.weights["win"]

    temp2 = env.copy()
    temp2.make_move(action, "X")
    if temp2.check_winner() == "X":
        score += self.weights["block"]

    if action == 4:
        score += self.weights["center"]

    if action in [0,2,6,8]:
        score += self.weights["corner"]

    # nieuwe feature
    two = count_two_in_row(temp.board, "O")
    score += self.weights["two_in_row"] * two

    score += random.random() * self.weights["random"]

    return score
```

***

## Stap 3 — tournament selectie (`evolution.py`)

```python
def tournament_selection(population, k=3):
    participants = random.sample(population, k)
    scored = [(evaluate(agent, population), agent) for agent in participants]
    scored.sort(reverse=True, key=lambda x: x[0])
    return scored[0][1]
```

***

## Stap 4 — aangepaste evolutie

```python
def evolve(population, generations=20):
    history = []

    for gen in range(generations):
        scores = [evaluate(agent, population) for agent in population]

        best = max(scores)
        avg = sum(scores) / len(scores)

        history.append((best, avg))

        print(f"Gen {gen} | best={best:.2f} avg={avg:.2f}")

        # selectie
        new_pop = []

        # elitisme (beste blijft)
        best_agent = population[scores.index(best)]
        new_pop.append(best_agent)

        while len(new_pop) < len(population):
            p1 = tournament_selection(population)
            p2 = tournament_selection(population)

            child = p1.crossover(p2)

            if random.random() < 0.3:
                child = child.mutate()

            new_pop.append(child)

        population = new_pop

    return population, history
```

***

## Stap 5 — visualisatie (main.py)

```python
import matplotlib.pyplot as plt

population = [EvoAgent() for _ in range(20)]
population, history = evolve(population, generations=20)

best_scores = [h[0] for h in history]
avg_scores = [h[1] for h in history]

plt.plot(best_scores, label="best")
plt.plot(avg_scores, label="avg")
plt.xlabel("generatie")
plt.ylabel("fitness")
plt.legend()
plt.show()
```

***

# Wat studenten moeten zien

*   fitness stijgt over generaties
*   agent leert:
    *   winnen afmaken
    *   blokkeren
    *   centrum/corners kiezen
*   minder random gedrag

***

# Belangrijk inzicht

Dit toont:

> Je programmeert geen strategie — je **laat ze ontstaan**

***

# 🔍 Analysevragen

Laat studenten beantwoorden:

*   Welke features zijn het belangrijkst?
*   Wat gebeurt er zonder “block”?
*   Hoe beïnvloedt mutatie de evolutie?
*   Zie je overfitting tegen populatie?

***

# Sterke uitbreidingen

## 1. Minimax + evolution

Gebruik:

```python
heuristic(state) = weighted sum
```

in een minimax agent

***

## 2. Self-play competitie

Laat:

```python
population split → compete
```

***

## 3. Noise verminderen

haal `"random"` weight weg → stabieler gedrag

***

## 4. Grotere spelruimte

*   connect-4 (sterk!)
*   4x4 tic-tac-toe

***

# Didactisch eindpunt

Na deze oefening begrijpen studenten:

*   evolution ≠ randomness
*   ontwerpen van features is cruciaal
*   agentgedrag kan ontstaan zonder expliciete logica

