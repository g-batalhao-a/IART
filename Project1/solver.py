from graph import *


def new_states(state: Node, a_star: bool = False):
    expansion = []
    moves = state.gamestate.expand()

    for move in moves:
        new_gamestate = state.gamestate.clone()
        from_i, to_i = move
        new_gamestate.move_ball(from_i, to_i) 
        node = Node(new_gamestate, 0, state.dist + 1)
        if a_star:
            node.setCost(node.better_nWrong_heuristics())
        expansion.append(node)

    for children in expansion:
        children.parent = state

    return expansion


# TODO
# Num of wrong, but wrong is defined by level of depth
def manhattan(matrix: list):
    size = len(matrix)
    col_size = len(matrix[0])
    row_i = 0
    col_i = 0
    distance = 0
    for row in matrix:
        for number in row:
            if number == 0:
                col_i += 1
                continue
            real_pos = number - 1
            real_row_i = real_pos // size
            real_col_i = real_pos % col_size
            distance += abs(real_row_i - row_i) + abs(real_col_i - col_i)
            col_i += 1
        row_i += 1

    return distance

def bfs(state: Node, max_depth: int = 10000):
    states = [state]

    graph_bfs = Graph()
    graph_bfs.new_depth()
    graph_bfs.add_node(state, 1)
    for depth in range(1, max_depth + 1):
        expanded_states = []
        for node in states:
            if node.gamestate.finished():
                print("Found Goal. Depth:", node.dist)
                return graph_bfs, node
            aux = new_states(node)
            for e in aux:
                expanded_states.append(e)
        states = expanded_states
        graph_bfs.new_depth()
        [graph_bfs.add_node(x, depth + 1) for x in states]
    return None, None


def bfs_optimized(state: Node, max_depth: int = 10000):
    states = [state]

    graph_bfs = Graph()
    graph_bfs.new_depth()
    graph_bfs.add_node(state, 1)
    for depth in range(1, max_depth + 1):
        expanded_states = []
        for node in states:
            if node.gamestate.finished():
                print("Found Goal. Depth:", node.dist)
                return graph_bfs, node
            if node in graph_bfs.visited:
                continue
            aux = new_states(node)
            for e in aux:
                expanded_states.append(e)
            graph_bfs.visit(node)
        states = expanded_states
        graph_bfs.new_depth()
        [graph_bfs.add_node(x, depth + 1) for x in states]
    return None, None


def dfs(state: Node, max_depth: int = 1000):
    graph_dfs = Graph()
    stack = [state]

    graph_dfs.new_depth()
    graph_dfs.add_node(state, 1)

    depth = 0
    while depth != max_depth and len(stack) != 0:
        graph_dfs.new_depth()
        node = stack.pop(0)
        graph_dfs.visit(node)
        if node.gamestate.finished():
            print("Found Goal. Depth:", node.dist)
            return graph_dfs, node
        else:
            expanded = new_states(node)
            [graph_dfs.add_node(x, x.dist + 1) for x in expanded]
            [stack.insert(0, x) for x in expanded if x not in graph_dfs.visited]
        depth += 1

    return None, None


def ids(state: Node, max_depth: int = 1000):
    for depth in range(1, max_depth):
        graph_ids, node = dfs(state, depth)
        if (graph_ids, node) != (None, None):
            return graph_ids, node
        print(depth)

    return state, None


# TODO
def greedy(state: Node, a_star: bool = False, max_depth: int = 5000):
    graph = Graph()
    state.setDist(0)
    stack = [state]
    graph.new_depth()
    graph.add_node(state, 1)

    depth = 1
    while depth != max_depth and len(stack) != 0:
        if a_star:
            stack.sort()
        else:
            stack.sort(key = lambda x: x.cost)
        graph.new_depth()
        node = stack.pop(0)
        if node.gamestate.finished():
            print("Found Goal. Depth:", node.dist)
            return graph, node
        else:
            graph.visit(node)
            expanded = new_states(node, a_star)
            [graph.add_node(x, depth + 1) for x in expanded]
            for children in expanded:
                if children in graph.visited:
                    continue
                if children in stack:
                    if (children.cost + node.dist + 1 < children.cost + children.dist) and a_star:
                        children.setParent(node)
                        children.setDist(node.dist + 1)
                else:
                    stack.append(children)

        print(depth)
        depth += 1


# TODO Function to check if a problem is possible to be solved
def checkSolvability(matrix: list):
    flat_list = [item for sublist in matrix for item in sublist]
    inversions = 0

    for x in range(0, len(flat_list)):
        for y in range(x + 1, len(flat_list)):
            inversions += 1 if (flat_list[x] > flat_list[y] and flat_list[y] != 0) else 0

    return inversions % 2 == 0


def print_solution(path: list):
    [x.print() for x in path]


if __name__ == "__main__":
    #puzzle = Game([Tube([1]), Tube([1, 1, 1])])
    #puzzle = Game([Tube([1, 2, 1, 2]), Tube([2, 1, 2, 1]), Tube()])
    puzzle = Game([Tube([1,2,3,1]),Tube([4,5,6,7]),Tube([6,1,7,2]),Tube([4,1,2,4]),Tube([6,5,3,4]),Tube([7,6,3,5]),Tube([5,3,7,2]), Tube(), Tube([])])
    init_state = Node(puzzle)

    # print("--- BFS ---")
    # graph, goal = bfs(init_state)

    # print("--- BFS-OPT ---")
    # graph, goal = bfs_optimized(init_state)

    # print("--- DFS ---")
    # graph, goal = dfs(init_state)

    # print("--- IDS ---")
    # graph, goal = ids(init_state)

    # print("--- Greedy ---")
    # graph, goal = greedy(init_state, False)

    print("--- A-Star ---")
    graph, goal = greedy(init_state, True)

    try:
        path = graph.path(goal)
        print_solution(path)
    except:
        print("No solution found!")
