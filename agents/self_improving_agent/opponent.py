import random

# meest simpelke tegenstander, kiest random een actie uit de beschikbare acties
def random_opponent(env):
    return random.choice(env.available_actions())