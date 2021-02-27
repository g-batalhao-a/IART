class Node:
    parent = None

    def __init__(self, start, end, action):
        self.start = start
        self.end = end
        self.action = action

    def __eq__(self, o):
        return o.end == self.end and o.start == self.start

    def __hash__(self):
        return self.start[0] + self.start[1] - self.end[0] - self.end[1]

    def print(self):
        print(self.start, " - ", self.action, " - ", self.end)


def print_solution(path: list):
    [x.print() for x in path]


class Graph:
    def __init__(self, depth=[]):
        self.depth = depth

    def new_depth(self):
        self.depth.append([])

    def add_node(self, node, level):
        self.depth[level - 1].append(node)

    def find_goals(self, goal, level):
        sol = []
        for state in self.depth[level - 1]:
            if state.end == goal:
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
    (b_4, b_3) = state.end

    expansion = []

    if b_4 + b_3 >= 4 and b_3 > 0:
        if b_4 != 4:
            expansion.append(Node(state.end, (4, b_3 - (4 - b_4)), "From 3L bucket to 4L bucket (full)"))
    if b_4 + b_3 >= 3 and b_4 > 0:
        if b_3 != 3:
            expansion.append(Node(state.end, (b_4 - (3 - b_3), 3), "From 4L bucket to 3L bucket (full)"))
    if b_4 + b_3 <= 4 and b_3 > 0:
        if b_4 != b_4 + b_3 or b_3 != 0:
            expansion.append(Node(state.end, (b_4 + b_3, 0), "From 3L bucket to 4L bucket"))
    if b_4 + b_3 <= 3 and b_4 > 0:
        if b_4 != 0 or b_3 != b_4 + b_3:
            expansion.append(Node(state.end, (0, b_4 + b_3), "From 4L bucket to 3L bucket"))
    if b_4 < 4:
        expansion.append(Node(state.end, (4, b_3), "Fill 4L bucket"))
    if b_3 < 3:
        expansion.append(Node(state.end, (b_4, 3), "Fill 3L bucket"))
    if b_4 > 0:
        expansion.append(Node(state.end, (0, b_3), "Empty 4L bucket"))
    if b_3 > 0:
        expansion.append(Node(state.end, (b_4, 0), "Empty 3L bucket"))

    for children in expansion:
        children.parent = state

    return expansion


def found_goal(states, goal):
    for state in states:
        if state.end[0] == goal:
            return True
    return False


def bfs(state: Node, max_depth: int = 1000, goal: int = 2):
    states = [state]

    graph = Graph()
    graph.new_depth()
    graph.add_node(state, 1)

    for depth in range(1, max_depth + 1):
        expanded_states = []
        for s in states:
            aux = expand(s)
            for e in aux:
                expanded_states.append(e)
        states = expanded_states

        graph.new_depth()
        [graph.add_node(x, depth + 1) for x in states]

        if found_goal(states, goal):
            print("Found Goal. Depth:", depth + 1)
            return graph, depth + 1


def dfs(state: Node, max_depth: int = 15, goal: int = 2):
    tree = Graph()
    stack = [state]

    visited = []
    tree.new_depth()
    tree.add_node(state, 1)

    depth = 1
    while depth != max_depth and len(stack) != 0:
        tree.new_depth()
        node = stack.pop(0)
        visited.append(node.start)

        if node.end[0] == goal:
            goals = []
            for i in range(0, 4):
                [goals.append(x) for x in graph.find_goals((2, i), depth)]
            for _goal in goals:
                print("For goal:", _goal.end, "Depth: ",depth)
                _path = graph.path(_goal)
                print_solution(path)
        else:
            expanded = expand(node)
            [tree.add_node(x, depth + 1) for x in expanded]
            [stack.insert(0, x) for x in expanded if x.end not in visited]
        depth += 1
    return graph, depth


if __name__ == "__main__":
    print("--- BFS ---")
    graph, depth = bfs(Node((0, 0), (0, 0), "start"))
    goals = []
    for i in range(0, 4):
        [goals.append(x) for x in graph.find_goals((2, i), depth)]
    for goal in goals:
        print("For goal:", goal.end)
        path = graph.path(goal)
        print_solution(path)

    print("--- DFS ---")
    graph, depth = dfs(Node((0, 0), (0, 0), "start"))

    print("--- IDS ---")
    goals=[]
    tries=0
    for i in range(2,25):
        graph, depth = dfs(Node((0, 0), (0, 0), "start"),i)
        temp=[]
        for i in range(0, 4):
            [temp.append(x) for x in graph.find_goals((2, i), depth)]
        if temp == goals:
            tries+=1
            if tries==6:
                break
            continue
        tries=0
        for i in range(0,len(temp)):
            if temp[i] not in goals:
                goals.append(temp[i])
