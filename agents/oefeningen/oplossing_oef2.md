# Oefening 2 — hybride spelagent

## Stappenplan

1.  **Start van je Q-agent**
    *   Je hebt al:
    ```python
    choose_action()
    update()
    ```

2.  **Implementeer een “kritieke toestand”**
    *   Idee: in late fase → minimax beter
    *   eenvoudig criterium:
    ```python
    len(env.available_actions()) <= 3
    ```

3.  **Importeer minimax**
    *   je hebt:
    ```python
    from minimax import minimax
    ```

4.  **Pas besluitvorming aan**
    *   voeg hybride keuze toe:
        *   soms Q-learning
        *   soms minimax

5.  **Test tegen verschillende tegenstanders**

***

# Voorbeeldoplossing (hybride agent)

### Aanpassing in `q_agent.py`

```python
from minimax import minimax

class HybridAgent:
    def __init__(self, q_agent, threshold=3):
        self.q_agent = q_agent
        self.threshold = threshold

    def choose_action(self, env):
        # aantal lege vakken
        remaining = len(env.available_actions())

        # --- kritieke situatie → minimax ---
        if remaining <= self.threshold:
            _, move = minimax(env, "O")
            return move

        # --- anders → Q-learning ---
        return self.q_agent.choose_action(env)

    def update(self, *args):
        self.q_agent.update(*args)

    def get_state(self, env):
        return self.q_agent.get_state(env)
```

***

# Gebruik in `main.py`

```python
from q_agent import QAgent
from hybrid_agent import HybridAgent

q_agent = QAgent()
agent = HybridAgent(q_agent, threshold=3)
```

Training blijft hetzelfde:

```python
play_game(agent, random_opponent, training=True)
```

***

# Zvaluatie (belangrijk deel van oplossing)

Voeg test toe:

```python
def evaluate(agent, opponent, games=200):
    results = {"O":0, "X":0, "draw":0}

    for _ in range(games):
        w = play_game(agent, opponent, training=False)
        results[w] += 1

    return results
```

### Vergelijk:

```python
print("Q-agent vs random:")
print(evaluate(q_agent, random_opponent))

print("\nHybrid vs random:")
print(evaluate(agent, random_opponent))

print("\nHybrid vs minimax:")
print(evaluate(agent, minimax_opponent))
```

***

# Wat studenten moeten zien

*   tegen random:
    *   Q-agent: goed
    *   hybrid: nog beter / stabieler

*   tegen minimax:
    *   Q-agent: slecht
    *   hybrid: minder slecht (verdedigt eindspel beter)

***

# Uitbreidingen (optioneel)

## 1. Betere kritieke detectie

i.p.v. enkel lege vakken:

```python
# check of iemand 2-op-een-rij heeft
```

***

## 2. Minimax als “kostbare actie”

Gebruik kans:

```python
if remaining <= 5 and random.random() < 0.5:
```

***

## 3. Leren wanneer minimax nuttig is

Gebruik bandit (zoals oefening 1):

```python
actie = ["q", "minimax"]
```

***

# Belangrijk inzicht

Je leert hier:

> **Agent = combinatie van methodes + controle over wanneer ze te gebruiken**

Niet:

*   ofwel RL
*   ofwel search

maar:

*   **beide samen in één systeem**


