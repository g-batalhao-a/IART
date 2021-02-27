class Node:
    parent = None

    def __init__(self, mcleft, mcright, boat):
        self.mcleft = mcleft
        self.mcright = mcright
        self.boat = boat

    def __eq__(self, o):
        return o.mcright == self.mcright and o.mcleft == self.mcleft and self.boat == o.boat

    def __hash__(self):
        return self.mcleft[0] + self.mcleft[1] - self.mcright[0] - self.mcright[1]

    def print(self):
        print(self.mcleft, " - ", self.boat, " - ", self.mcright)

    def valid(self):
        return self.mcleft[0] >= 0 and self.mcright[0] >= 0 \
               and self.mcleft[1] >= 0 and self.mcright[1] >= 0 \
               and (self.mcleft[0] == 0 or self.mcleft[0] >= self.mcleft[1]) \
               and (self.mcright[0] == 0 or self.mcright[0] >= self.mcright[1])


def print_solution(path: list):
    [x.print() for x in path]


class Graph:
    visited = []

    def __init__(self, depth=[]):
        self.depth = depth

    def new_depth(self):
        self.depth.append([])

    def add_node(self, node: Node, level):
        self.depth[level - 1].append(node)

    def visit(self, node: Node):
        self.visited.append(node)

    def find_goals(self, goal, level):
        sol = []
        for state in self.depth[level - 1]:
            if state.mcleft == goal:
                sol.append(state)
        return sol

    def path(self, dest):
        node = dest
        path = [dest]
        while node != self.depth[0][0]:
            path.append(node.parent)
            node = node.parent
        path.reverse()
        return path


def expand(state):
    expansion = []
    (missl, canl) = state.mcleft
    (missr, canr) = state.mcright
    if state.boat == 'left':
        ## Two missionaries cross left to right
        new_state = Node((missl - 2, canl), (missr + 2, canr), 'right')
        if new_state.valid():
            expansion.append(new_state)

        ## Two cannibals cross left to right.
        new_state = Node((missl, canl - 2), (missr, canr + 2), 'right')
        if new_state.valid():
            expansion.append(new_state)

        ## One missionary and one cannibal cross left to right.
        new_state = Node((missl - 1, canl - 1), (missr + 1, canr + 1), 'right')
        if new_state.valid():
            expansion.append(new_state)

        ## One missionary crosses left to right.
        new_state = Node((missl - 1, canl), (missr + 1, canr), 'right')
        if new_state.valid():
            expansion.append(new_state)

        ## One cannibal crosses left to right.
        new_state = Node((missl, canl - 1), (missr, canr + 1), 'right')
        if new_state.valid():
            expansion.append(new_state)

    else:
        ## Two missionaries cross left to right
        new_state = Node((missl + 2, canl), (missr - 2, canr), 'left')
        if new_state.valid():
            expansion.append(new_state)

        ## Two cannibals cross left to right.
        new_state = Node((missl, canl + 2), (missr, canr - 2), 'left')
        if new_state.valid():
            expansion.append(new_state)

        ## One missionary and one cannibal cross left to right.
        new_state = Node((missl + 1, canl + 1), (missr - 1, canr - 1), 'left')
        if new_state.valid():
            expansion.append(new_state)

        ## One missionary crosses left to right.
        new_state = Node((missl + 1, canl), (missr - 1, canr), 'left')
        if new_state.valid():
            expansion.append(new_state)

        ## One cannibal crosses left to right.
        new_state = Node((missl, canl + 1), (missr, canr - 1), 'left')
        if new_state.valid():
            expansion.append(new_state)

    for children in expansion:
        children.parent = state

    return expansion


def found_goal(states, goal: tuple):
    for state in states:
        if state.mcright == goal:
            return True
    return False


def bfs(state: Node, max_depth: int = 100, goal: tuple = (0, 0)):
    states = [state]

    graph = Graph()
    graph.new_depth()
    graph.add_node(state, 1)

    for depth in range(1, max_depth + 1):
        expanded_states = []
        for s in states:
            if s in graph.visited:
                continue
            aux = expand(s)
            for e in aux:
                expanded_states.append(e)
            graph.visit(s)
        states = expanded_states

        graph.new_depth()
        [graph.add_node(x, depth + 1) for x in states]

        if found_goal(states, goal):
            print("Found Goal. Depth:", depth + 1)
            return graph, depth + 1


def dfs(state: Node, max_depth: int = 100, goal: tuple = (0, 0)):
    tree = Graph()
    stack = [state]

    visited = []
    tree.new_depth()
    tree.add_node(state, 1)

    depth = 1
    while depth != max_depth and len(stack) != 0:
        tree.new_depth()
        node = stack.pop(0)
        visited.append(node)

        if node.mcright == goal:
            print("For goal:", node.mcleft, "Depth: ", depth)
            return tree, depth
        else:
            expanded = expand(node)
            [tree.add_node(x, depth + 1) for x in expanded]
            [stack.insert(0, x) for x in expanded if x not in visited]
        depth += 1


if __name__ == "__main__":
    print("--- BFS ---")
    graph, depth = bfs(Node((0, 0), (3, 3), 'right'))
    goal = graph.find_goals((3, 3), depth)
    for x in goal:
        print("For goal: (3,3) - (0,0)")
        path = graph.path(x)
        print_solution(path)

    print("--- DFS ---")
    graph, depth = dfs(Node((0, 0), (3, 3), 'right'))
    goal = graph.find_goals((3, 3), depth)
    for x in goal:
        path = graph.path(x)
        print_solution(path)

    print("--- IDS ---")
    i = 2
    found = False
    while not found and i < 20:
        graph, depth = dfs(Node((0, 0), (3, 3), 'right'), i) or (None, None)
        if depth is None:
            i += 1
            continue
        goal = graph.find_goals((3, 3), depth)
        for x in goal:
            path = graph.path(x)
            print_solution(path)
            found = True
            break
        i += 1
