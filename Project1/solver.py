from graph import *

def new_states(state: Node, a_star: bool=False):
    expansion = []
    moves = state.gamestate.expand()

    for move in moves:
        new_gamestate=state.gamestate.clone()
        from_i,to_i = move
        new_gamestate.move_ball(from_i,to_i)
        expansion.append(Node(new_gamestate))

    for children in expansion:
        children.parent = state

    return expansion


# Num of wrong, but wrong is defined by level of depth
def manhattan(matrix: list):
    size= len(matrix)
    col_size = len(matrix[0])
    row_i=0
    col_i=0
    distance=0
    for row in matrix:
        for number in row:
            if number==0:
                col_i+=1
                continue
            real_pos = number - 1
            real_row_i = real_pos//size
            real_col_i = real_pos%col_size
            distance += abs(real_row_i-row_i)+abs(real_col_i-col_i)
            col_i+=1
        row_i+=1

    return distance

def bfs(state: Node, max_depth: int = 10000):
    states = [state]

    graph = Graph()
    graph.new_depth()
    graph.add_node(state, 1)
    for depth in range(1, max_depth + 1):
        expanded_states = []
        for s in states:
            if s.gamestate.finished():
                print("Found Goal. Depth:", depth)
                return graph, depth
            if s in graph.visited:
                continue
            aux = new_states(s)
            for e in aux:
                expanded_states.append(e)
            graph.visit(s)
        states = expanded_states
        graph.new_depth()
        [graph.add_node(x, depth + 1) for x in states]

def heuristic(state: Node, a_star: bool = False,max_depth: int = 5000, goal: list=[[1,2,3],[4,5,6],[7,8,0]]):
    graph = Graph()
    state.setDist(0)
    stack = [state]
    graph.new_depth()
    graph.add_node(state, 1)

    depth = 1
    while depth != max_depth and len(stack) != 0:
        stack.sort()
        graph.new_depth()
        node = stack.pop(0)
        if node.matrix == goal:
            _path = graph.path(node)
            print("For goal:", node.matrix, "Depth: ",len(_path)-1)
            print_solution(_path)
            return graph,depth
        else:
            graph.visit(node)
            expanded = new_states(node,a_star)
            [graph.add_node(x, depth + 1) for x in expanded]
            for children in expanded:
                if children in graph.visited:
                    continue
                if children in stack:
                    if (children.cost+node.dist+1<children.cost+children.dist) and a_star:
                        children.setParent(node)
                        children.setDist(node.dist+1)
                else:
                    stack.append(children)
            
        depth += 1

def checkSolvability(matrix: list):
    flat_list = [item for sublist in matrix for item in sublist]
    inversions = 0

    for x in range(0,len(flat_list)):
        for y in range(x+1,len(flat_list)):
            inversions+=1 if (flat_list[x]>flat_list[y] and flat_list[y]!=0) else 0
                
    return inversions%2==0

def print_solution(path: list):
    [x.print() for x in path]

if __name__ == "__main__":
    puzzle = Game([Tube([1]),Tube([1,1,1])])
    puzzle = Game([Tube([1,2,1,2]),Tube([2,1,2,1]),Tube()])
    init_state= Node(puzzle)
    print("--- BFS ---")
    graph, depth = bfs(init_state)
    goals = []
    [goals.append(x) for x in graph.find_goals(depth)]
    for goal in goals:
        path = graph.path(goal)
        print_solution(path)

