# Agentic Programming in Games & Puzzles

## Inleiding

In deze les verschuiven we van het bestuderen van **individuele algoritmes** naar het bouwen van **agenten**: systemen die zelfstandig beslissingen nemen, leren uit ervaring en verschillende technieken combineren. Waar eerdere delen van de cursus focusten op specifieke methodes (zoals breadth-first search, minimax of Q-learning), bekijken we nu hoe deze methodes geïntegreerd kunnen worden in één coherent systeem.

Het centrale idee is dat intelligent gedrag vaak niet voortkomt uit één algoritme, maar uit de manier waarop meerdere technieken worden gecombineerd, aangestuurd en aangepast.

We bekijken vier concrete benaderingen:
1. Tool-using agents  
2. Self-improving agents (RL + minimax)  
3. LLM-gebaseerde agents  
4. Evolutionaire agents  

Deze sluiten rechtstreeks aan bij de thema’s van de cursus: **games en puzzels**.


## Wat is een agent?

Een **agent** is een systeem dat:
- een **omgeving waarneemt**
- beslissingen neemt (acties)
- een doel probeert te bereiken
- en vaak leert of zich aanpast

De klassieke agent-loop ziet er als volgt uit:

```
perceptie → beslissing → actie → observatie → herhaal

```

In termen van AIMA (Russell & Norvig) bestaat een probleem/agent uit:
- **state**: beschrijving van de huidige situatie  
- **actions**: mogelijke acties  
- **transition model**: wat gebeurt er na een actie  
- **goal / reward**: wat willen we bereiken  

### Wat is géén agent?

Niet elk algoritme is een agent:
- BFS alleen = geen agent  
- A* alleen = geen agent  
- een formule of functie zonder feedback = geen agent  

Een agent vereist **interactie en besluitvorming**.
> Een agent is een **controller die beslissingen neemt over hoe algoritmes worden gebruikt**.

---
## Agenten als orchestratoren

In deze les bekijken we agenten als een extra laag boven bestaande technieken:

| Niveau | Voorbeeld |
|------|----------|
| Algoritme | BFS, minimax, Q-learning |
| Agent | kiest wanneer/welke techniek te gebruiken |

Dit is een belangrijke stap in AI:
- van **algoritme-implementatie**
- naar **systeemontwerp**

# 1. Tool-Using Agents

## Idee

Een tool-using agent beschikt over meerdere algoritmes en kiest:
> *welk algoritme best geschikt is voor het huidige probleem*

Bijvoorbeeld:
- BFS → kleine problemen  
- A* → middelgrote problemen  
- simulated annealing → grote problemen  

De agent voert dus een vorm van **meta-besluitvorming** uit.

## Architectuur


Probleem → Agent → Tool → Oplossing
De *tool* is hier een algoritme zoals BFS of A*.

## Basisimplementatie

```python
self.tools = {
    "bfs": bfs,
    "dfs": dfs,
    "astar": astar,
    "annealing": simulated_annealing
}
```

De kern ligt in:

```python
def choose_tool(problem):
    if problem.size < 10:
        return "bfs"
    return "astar"
```

***

## Link met eerdere leerstof

Deze agent bouwt verder op:

*   breadth-first search
*   depth-first search
*   heuristische search (A\*)
*   optimalisatie (simulated annealing)

Nieuw concept:

> **Algorithm selection problem**



## Uitbreidingen: leren kiezen

In plaats van vaste regels kan de agent leren via:

*   bandits (ε-greedy)
*   reinforcement learning

Bijvoorbeeld:

```python
if random.random() < epsilon:
    return random_tool()
else:
    return best_tool_so_far
```
Dit gaan we bekijken in de oefeningen


## Intuïtie

Niet elk algoritme werkt best in elke situatie.
De agent leert:

> “Welke techniek werkt wanneer?”


# 2. Self-Improving Agents (RL + Minimax)

## Idee

Een self-improving agent leert uit ervaring (reinforcement learning), maar kan ook gebruik maken van exacte redeneermethoden zoals minimax.
We combineren:

*   **Q-learning** (leren)
*   **minimax** (planning / adversarial reasoning)

## Architectuur

    Environment ↔ Agent
          ↓
        Reward
          ↑
        Learning (Q-values)

## Q-learning recap

De update regel:

    Q(s,a) ← Q(s,a) + α (r + γ max_a' Q(s',a') − Q(s,a))

Interpretatie:
*   leer hoe goed een actie is
*   op basis van toekomstige beloningen

## Hybride strategie

```python
if critical_state:
    use minimax
else:
    use Q-learning
```

**kritieke toestand:**
*   weinig zetten over
*   winst/verlies dichtbij


## Waarom werkt dit?

| Methode    | Sterkte                                  |
| ---------- | ---------------------------------------- |
| Q-learning | lange termijn leren                      |
| minimax    | perfecte besluitvorming in kleine states |

Samen:

> adaptief + accuraat


## Link met cursus

*   reinforcement learning
*   Q-learning
*   adversarial search
*   minimax

Nieuw concept:

> **hybride agenten**

## Intuïtie

De agent leert:

*   algemene strategie via RL
*   perfecte beslissingen in moeilijke situaties via minimax

vergelijkbaar met menselijke spelers:

*   intuïtie + berekening


# 3. LLM Agents

## Idee

Een LLM-agent gebruikt een taalmodel als **algemene redeneercomponent**.
In plaats van expliciete logica:

*   geeft men een prompt
*   model genereert een beslissing

***

## Architectuur (ReAct)

    State → Prompt → LLM → Action → Environment → nieuwe State

Vaak expliciet:

    Thought → Action → Observation → repeat



## Prompt als gedrag

Voorbeeld:

    State: 23
    Available actions: minus1, minus3, div2
    Goal: reach 0

    Thought:
    Action:

Het model beslist:
*   hoe te redeneren
*   welke actie te kiezen


## Code structuur

```python
prompt = build_prompt(state)
response = llm(prompt)
action = parse(response)
```



## Belangrijk inzicht

> De “intelligentie” zit in de prompt, niet in de code.


## Link met cursus

*   verwant aan heuristieken
*   lijkt op planning

maar:

*   geen expliciete algoritmes
*   flexibel en generiek

## Sterktes

*   flexibel
*   weinig expliciete programmeerlogica nodig
*   werkt op verschillende problemen

## Zwaktes

*   niet gegarandeerd correct
*   gevoelig voor prompt
*   minder efficiënt

## Intuïtie

De agent:

*   “begrijpt” het probleem via tekst
*   kiest acties zoals een menselijke probleemoplosser

# 4. Evolutionaire Agents

## Idee

In plaats van een agent te programmeren:

> **evolueren we een agent**

We gebruiken:
*   populaties
*   selectie
*   mutatie
*   crossover


## Architectuur

    Population → Evaluation → Selection → Mutation → nieuwe Population


## Genotype = gedrag

Een agent wordt voorgesteld door parameters:

```python
weights = {
    "win": 8.2,
    "block": 5.1,
    "center": 1.7
}
```

Deze bepalen de beslissingen.


## Evolutieloop

```python
for generation:
    evaluate population
    select best
    create offspring
```


## Link met cursus

*   genetic algorithms
*   optimalisatie

Nieuw:

> **agents als geëvolueerde entiteiten**


## Intuïtie

*   goede strategie → meer nakomelingen
*   slechte strategie → verdwijnt

👉 gedrag ontstaat vanzelf


## Voorbeeld

In Tic-Tac-Toe leert de agent:

*   centrum kiezen
*   blokkeren
*   winnen afmaken

zonder expliciete regels.


# Vergelijking van de vier agents

| Type           | Sterkte              | Zwakte          |
| -------------- | -------------------- | --------------- |
| Tool agent     | efficiënt, duidelijk | weinig flexibel |
| Self-improving | leert goed           | training nodig  |
| LLM agent      | flexibel             | onbetrouwbaar   |
| Evolution      | ontdekt strategie    | traag           |

# Integratie met cursus

Deze vier vormen bouwen op eerdere onderdelen:

| Thema cursus       | Agent          |
| ------------------ | -------------- |
| BFS / DFS / A\*    | tool agent     |
| RL (Q-learning)    | self-improving |
| minimax            | self-improving |
| heuristiek         | LLM            |
| genetic algorithms | evolution      |


# Belangrijk concept: meta-niveau

Tot nu toe:

*   “Hoe werkt BFS?”
*   “Hoe werkt minimax?”

Nu:

> “Wanneer gebruik ik BFS? Wanneer minimax?”


# Trade-offs

Geen enkele agent is perfect. Er moeten altijd afwegingen worden gemaakt.

Belangrijke keuzes:

*   snelheid vs optimaliteit
*   flexibiliteit vs controle
*   leren vs zekerheid

# Voorbeelden in games & puzzels

*   doolhoven → tool agent
*   tic-tac-toe → RL + minimax
*   numerieke puzzels → LLM
*   strategieën → evolutionair

# Belangrijkste inzichten

1.  **Agents combineren technieken**
2.  Beslissingen gebeuren op meerdere niveaus
3.  Er is geen “beste” methode
4.  Ontwerp is cruciaal


# Reflectievragen

*   Wanneer kies je voor search?
*   Wanneer voor RL?
*   Wanneer voor LLM?
*   Wanneer voor evolution?


# Conclusie

Agentic programming is een stap verder dan klassieke AI:

Niet:
> “welk algoritme is correct?”
Maar:
> “hoe ontwerp je een systeem dat zelfstandig goede keuzes maakt?”

Dit sluit sterk aan bij moderne AI-systemen:

*   autonome agents
*   LLM-gebaseerde systemen
*   hybride AI

