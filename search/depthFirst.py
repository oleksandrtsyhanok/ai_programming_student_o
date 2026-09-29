class State:
    def __init__(self, name):
        self.Name = name

class Node:
    def __init__(self, state):
        self.State = state
        self.Actions = []

    def add_action(self, action):
        self.Actions.append(action)

class Edge:
    def __init__(self, from_node, to_node, cost):
        self.FromNode = from_node
        self.ToNode = to_node
        self.Cost = cost

class Problem:
    @staticmethod
    def read_from_file(filepath):
        known_nodes = {}

        with open(filepath, 'r') as file:
            from_node = file.readline().strip()
            to_node = file.readline().strip()

            initial_node = Problem.get_or_create(known_nodes, from_node)
            goal_node = Problem.get_or_create(known_nodes, to_node)

            for line in file:
                line = line.strip()
                node_description_parts = line.split(": ")

                node_name = node_description_parts[0]
                node = Problem.get_or_create(known_nodes, node_name)

                transitions = node_description_parts[1]
                transitions_arr = transitions.split(" ")
                for i in range(0, len(transitions_arr), 2):
                    transition_node_name = transitions_arr[i]
                    transition_cost = float(transitions_arr[i + 1])

                    transition_node = Problem.get_or_create(known_nodes, transition_node_name)
                    node.add_action(Edge(node, transition_node, transition_cost))

        problem = Problem()
        problem.InitialState = initial_node
        problem.GoalState = goal_node

        return problem

    @staticmethod
    def get_or_create(nodes, node_name):
        if node_name in nodes:
            return nodes[node_name]
        else:
            node = Node(State(node_name))
            nodes[node_name] = node
            return node

    def goal_reached(self, path):
        return path.Nodes[-1] == self.GoalState

class Path:
    def __init__(self, initial_state):
        self.Nodes = [initial_state]
        self.LeafNode = initial_state
        self.Cost = 0

    def __str__(self):
        node_names = [node.State.Name for node in self.Nodes]
        return "->".join(node_names) + "=" + str(self.Cost)

class SearchAlgorithm:
    def search(self, problem):
        pass

class DepthFirstSearch(SearchAlgorithm):
    def search(self, problem):
        explored_items = []
        return self.search_recursive(problem, Path(problem.InitialState), explored_items)

    def search_recursive(self, problem, path, explored_items):
        if problem.goal_reached(path):
            return path
        else:
            print("TMP", path)
            explored_items.append(path.LeafNode)

            for action in path.LeafNode.Actions:
                child_node = action.ToNode
                if not self.redundant(explored_items, child_node):
                    path_after_following_action = Path(path.Nodes[0])
                    path_after_following_action.Nodes.extend(path.Nodes[1:])
                    path_after_following_action.Nodes.append(child_node)
                    path_after_following_action.LeafNode = child_node
                    path_after_following_action.Cost = path.Cost + action.Cost
                    found_solution = self.search_recursive(problem, path_after_following_action, explored_items)
                    if found_solution is not None:
                        return found_solution

            return None  # No path found

    def redundant(self, explored_items, child_node):
        return child_node in explored_items

if __name__ == "__main__":
    algorithm = DepthFirstSearch()
    problem = Problem.read_from_file(args[0])
    solution = algorithm.search(problem)
    print("FINAL", solution)
