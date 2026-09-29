Hier is **Oefening 3 — oplossing + stappenplan** (LLM-agent verbeteren via prompting).

***

# Oefening 3 — LLM agent verbeteren

## Stappenplan

1.  **Start van bestaande LLM-agent**
    *   je hebt:
    ```python
    build_prompt()
    parse_output()
    ```

2.  **Identificeer problemen**
    Typisch:
    *   neemt te veel stappen
    *   loopt in lussen
    *   kiest slechte acties

3.  **Pas de prompt aan**
    → dit is de kern van de oefening

4.  **Voeg geheugen toe**
    *   geef vorige states mee

5.  **Test systematisch**
    *   vergelijk verschillende prompts

***

# Basisoplossing (verbeterde agent)

### Aangepaste `agent.py`

```python
class LLMAgent:
    def __init__(self, llm):
        self.llm = llm
        self.history = []

    def build_prompt(self, state, actions):
        previous_states = [h["state"] for h in self.history[-5:]]

        return f"""
You are solving a number puzzle.

Goal: reach 0 as fast as possible.

Current state: {state}
Available actions: {actions}

Previous states: {previous_states}

Rules:
- minus1 → subtract 1
- minus3 → subtract 3
- div2 → divide by 2 (only if even)

Instructions:
- Minimize number of steps
- Avoid repeating previous states
- Prefer large reductions

Respond STRICTLY in this format:

Thought: <short reasoning>
Action: <one of {actions}>
"""

    def parse_output(self, text, actions):
        thought = ""
        action = None

        for line in text.split("\n"):
            if line.lower().startswith("thought"):
                thought = line.split(":",1)[1].strip()
            if line.lower().startswith("action"):
                action = line.split(":",1)[1].strip()

        if action not in actions:
            action = actions[0]

        return thought, action

    def run(self, env, max_steps=30):
        step = 0

        while not env.is_goal() and step < max_steps:
            state = env.get_state()
            actions = env.available_actions()

            prompt = self.build_prompt(state, actions)
            response = self.llm.complete(prompt)

            thought, action = self.parse_output(response, actions)

            env.apply_action(action)

            print(f"\nState: {state}")
            print("Thought:", thought)
            print("Action:", action)

            self.history.append({
                "state": state,
                "action": action
            })

            step += 1

        return env.get_state()
```

***

# Experiment (belangrijk!)

Laat studenten **varianten vergelijken**.

## Variant A — baseline prompt

Geen geheugen, geen optimalisatie.

## Variant B — met doel

    Minimize number of steps

## Variant C — met geheugen

    Previous states: [...]
    Avoid repeating them

## Variant D — planning

Voeg toe:

    Before acting, think about the next 2 steps

***

# Evaluatiecode

```python
def evaluate(agent, starts):
    results = []

    for s in starts:
        env = NumberPuzzle(s)
        steps_before = len(agent.history)

        agent.run(env, max_steps=30)

        steps_after = len(agent.history)
        steps_used = steps_after - steps_before

        success = (env.get_state() == 0)

        results.append((s, success, steps_used))

    return results
```

Print:

```python
print(evaluate(agent, [10, 15, 23, 30]))
```

***

# Wat studenten moeten observeren

*   met betere prompt:
    *   minder stappen
    *   minder lussen
    *   hogere success rate

*   met slechte prompt:
    *   willekeurig gedrag

directe impact van prompt design

***

# Belangrijk inzicht

Dit toont:

> Bij LLM-agents zit “intelligentie” in **de prompt**, niet in de code

***

# Sterke uitbreidingen

## 1. Feedback in prompt

```python
Last action result: ...
```

***

## 2. Straf voor loops

Voeg toe:

    You are repeating states → change strategy

***

## 3. Multi-step output

Laat model antwoorden:

    Plan: ...
    Action: ...

***

## 4. Vergelijk met niet-LLM agent

*   wie gebruikt minder stappen?
*   wie is robuuster?

***

# Wat dit didactisch oplevert

Studenten leren:

*   prompt engineering
*   agent loops
*   limits van LLM reasoning

