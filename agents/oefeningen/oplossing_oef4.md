
# Oefening 4 — benchmarking

## Stappenplan

1.  **Zorg dat alle agenten werken**
    *   tool-agent
    *   hybride RL/minimax agent
    *   LLM agent
    *   evolutionaire agent

2.  **Definieer één gemeenschappelijke taak**
    → bv. number puzzle of grid puzzle  
    (voor eenvoud: number puzzle)

3.  **Bepaal metriek**
    Minstens:
    *   success rate
    *   aantal stappen
    *   runtime

4.  **Genereer testcases**

```python
starts = [10, 15, 20, 25, 30]
```

5.  **Run experimenten**
    *   meerdere runs per agent
    *   gemiddelde nemen

6.  **Visualiseer**
    *   print tabel of maak grafiek

***

# Voorbeeldoplossing

## Benchmark module

```python
import time

def run_agent(agent, start, runs=5):
    successes = 0
    steps_list = []
    times = []

    for _ in range(runs):
        env = NumberPuzzle(start)

        t0 = time.time()
        final = agent.run(env, max_steps=30)
        t1 = time.time()

        success = (final == 0)

        successes += int(success)
        steps_list.append(len(agent.history))
        times.append(t1 - t0)

        # reset geschiedenis indien nodig
        agent.history = []

    return {
        "success_rate": successes / runs,
        "avg_steps": sum(steps_list) / runs,
        "avg_time": sum(times) / runs
    }
```

***

## Alle agenten vergelijken

```python
agents = {
    "tool": tool_agent,
    "hybrid": hybrid_agent,
    "llm": llm_agent,
    "evolution": evo_agent
}

starts = [10, 15, 20, 25]

results = {}

for name, agent in agents.items():
    results[name] = {}

    for s in starts:
        res = run_agent(agent, s)
        results[name][s] = res
```

***

## Resultaten printen

```python
for name in results:
    print(f"\n=== {name} ===")
    for s in resultsr = results[name][s]
        print(f"start={s} | success={r['success_rate']:.2f} "
              f"| steps={r['avg_steps']:.1f} "
              f"| time={r['avg_time']:.4f}s")
```

***

# (Optioneel) Visualisatie

```python
import matplotlib.pyplot as plt

for name in results:
    xs = []
    ys = []

    for s in starts:
        xs.append(s)
        ys.append(results[name][s]["avg_steps"])

    plt.plot(xs, ys, label=name)

plt.xlabel("startwaarde")
plt.ylabel("gemiddeld aantal stappen")
plt.legend()
plt.show()
```

***

# Wat studenten moeten zien

Typisch patroon:

| Agent        | Verwachte gedrag           |
| ------------ | -------------------------- |
| tool-agent   | stabiel, snel              |
| hybride      | sterk in games             |
| LLM          | flexibel maar inconsistent |
| evolutionair | afhankelijk van training   |

***

# Belangrijk inzicht

Dit maakt duidelijk:

> Verschillende agent-paradigma’s hebben **andere sterktes**  
> → er is geen “beste” agent

***

# 🔍 Analysevragen (deel van oplossing)

Laat studenten antwoorden:

*   Welke agent is het snelst?
*   Welke schaalt het best met moeilijkheid?
*   Wanneer faalt de LLM?
*   Welke is het meest stabiel?

***

# Sterke uitbreidingen

## 1. Moeilijkheid verhogen

```python
starts = [10, 20, 40, 80]
```

***

## 2. Variantie meten

niet enkel gemiddelde, maar ook spreiding

***

## 3. Kosten meenemen

LLM → duurder  
→ voeg “cost per run” toe

***

## 4. Combineer agents

test:

```python
meta-agent chooses best one
```

***

# 🧑Didactisch belangrijk

Dit is misschien de **belangrijkste oefening** omdat studenten hier:

*   leren vergelijken
*   leren meten
*   begrijpen dat AI engineering = trade-offs
