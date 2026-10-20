import heapq
from collections import deque


class RiverCrossing:
    def __init__(self):
        self.initial_state = (3, 3, 0)  # (boeren_links, wolven_links, boot_kant)
        self.goal_state = (0, 0, 1)
        # Mogelijke overtochten (boeren, wolven)
        # een 'move' is een tuple (aantal_boeren, aantal_wolven) dat aangeeft hoeveel van elk type de boot overzet
        self.moves = [
            (1, 0),
            (2, 0),  # 1 of 2 boeren
            (0, 1),
            (0, 2),  # 1 of 2 wolven
            (1, 1),  # 1 boer en 1 wolf
        ]

        # je kan hier items als volgt uithalen:
        # for b, w in self.moves:
        #     print(f"Boeren: {b}, Wolven: {w}")

    def is_valid_state(self, boeren_links, wolven_links):
        # deze functie controleert of een staat geldig is. Geeft True terug als de staat geldig is, anders False.

        boeren_rechts = 3 - boeren_links
        wolven_rechts = 3 - wolven_links

        # Controleer of waarden binnen bereik liggen
        # TODO
        if boeren_links not in range(3) or wolven_links not in range(3):
            return False

        if boeren_rechts not in range(3) or wolven_rechts not in range(3):
            return False

        # Controleer of boeren niet worden opgegeten
        # TODO
        if wolven_links - boeren_links > 0:
            return False
        if wolven_rechts - boeren_rechts > 0:
            return False

        return True

    def get_new_states(self, state):
        # deze functie genereert alle mogelijke opvolgerstaten vanuit de huidige staat
        # TODO
        new_states = []

        for b, w in self.moves:
            new = ()
            if state[2] == 0:
                new = (state[0] - b, state[1] - w, 1 if state[2] == 0 else 0)
            else:
                new = (state[0] + b, state[1] + w, 1 if state[2] == 0 else 0)
            if self.is_valid_state(new[0], new[1]):
                new_states.append(new)

        # Tips:
        # - maak een onderscheid tussen de kant van de boot waar de boot vertrekt (0 of 1)
        # - maak gebruik van functies hierboven indien nodig
        return new_states

    def solve(self):
        # deze functie lost het probleem
        # TODO
        initial_node = self.initial_state
        if initial_node == self.goal_state:
            return [initial_node]

        frontier = deque([initial_node])
        nodes = 
        parent: dict = {_puzzel_sleutel(start_puzzle): None}
        explored = {_puzzel_sleutel(start_puzzle)}

        while frontier:
            current = frontier.popleft()
            for kind in current.possible_new_configurations():
                k = _puzzel_sleutel(kind)
                if k in explored:
                    continue
                explored.add(k)
                parent[k] = _puzzel_sleutel(current)
                nodes[k] = kind
                if kind.is_goal():
                    pad = [kind]
                    stap = k
                    while parent[stap] is not None:
                        stap = parent[stap]
                        pad.append(nodes[stap])
                    pad.reverse()
                    return pad
                frontier.append(kind)
        return None


# Testcode
rc = RiverCrossing()
start = rc.initial_state
print("Startstaat:", start)
print("Mogelijke eerste zetten:")
for s in rc.get_new_states(start):
    print(s)

print("Oplossing?")
solution = rc.solve()
# TODO: print de oplossing als die er is, anders geef aan dat er geen oplossing is
