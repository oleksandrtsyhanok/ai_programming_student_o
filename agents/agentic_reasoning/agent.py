import random
from tools import TOOLS


class ReasoningAgent:
    def __init__(self, llm):
        self.llm = llm
        self.history = []

    def reason(self, state, actions):
        """
        This replaces an LLM.
        You can later swap this with GPT or another model.
        """

        thoughts = []

        # Heuristic reasoning examples
        if state % 2 == 0 and state > 4:
            thoughts.append("Even number: division is efficient")

        if state <= 3:
            thoughts.append("Close to goal: subtract directly")

        if not thoughts:
            thoughts.append("Try reducing the number")

        return thoughts
    
    
    def build_prompt(self, state, actions):
        return f"""
You are solving a puzzle.

State: {state}
Goal: reach 0
Available actions: {actions}

Rules:
- minus1 → subtract 1
- minus3 → subtract 3
- div2 → divide by 2 (only if even)

Respond STRICTLY in this format:

Thought: <brief reasoning>
Action: <one of {actions}>

Choose the best action to reach 0 efficiently.
"""

    def parse_output(self, text, actions):
        thought = ""
        action = None

        lines = text.split("\n")
        for line in lines:
            if line.lower().startswith("thought"):
                thought = line.split(":",1)[1].strip()
            if line.lower().startswith("action"):
                action = line.split(":",1)[1].strip()

        if action not in actions:
            action = actions[0]  # fallback

        return thought, action


    def decide(self, state, actions):
        """
        Decision rule based on reasoning.
        Acts like a primitive policy.
        """

        # heuristic policy
        if "div2" in actions and state % 2 == 0 and state > 4:
            return "div2"

        if "minus3" in actions and state >= 3:
            return "minus3"

        return "minus1"

    def act(self, state, action):
        return TOOLS[action](state)

    def run(self, env, max_steps=50, verbose=True, llm_mode=False):
        step = 0

        while not env.is_goal() and step < max_steps:
            state = env.get_state()
            actions = env.available_actions()

            if (llm_mode):

                # --- LLM REASON and DECIDE(optional) ---
                prompt = self.build_prompt(state, actions)
                response = self.llm.complete(prompt)

                thought, action = self.parse_output(response, actions)

                
                next_state = TOOLS[action](state)
                env.apply_action(action)

                print(f"\nState: {state}")
                print("LLM Thought:", thought)
                print("Action:", action)
                print("Next:", next_state)

                self.history.append({
                    "state": state,
                    "thought": thought,
                    "action": action
                })

                step += 1
            else:
                # --- REASON ---
                thoughts = self.reason(state, actions)

                # --- DECIDE ---
                action = self.decide(state, actions)

                # --- ACT ---
                new_state = self.act(state, action)

                # update environment
                env.apply_action(action)

                # store trace
                self.history.append({
                    "state": state,
                    "thoughts": thoughts,
                    "action": action,
                    "next_state": new_state
                })

                if verbose:
                    print(f"\nState: {state}")
                    print("Thoughts:", thoughts)
                    print("Action:", action)
                    print("Next:", new_state)

                step += 1

        return env.get_state()