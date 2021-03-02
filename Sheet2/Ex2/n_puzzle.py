import copy

class Node:
    parent = None

    def __init__(self, matrix, empty_pos, cost: int=0):
        self.matrix = matrix
        self.empty_pos = empty_pos
        self.cost=cost

    def __eq__(self, o):
        return o.matrix == self.matrix and o.empty_pos == self.empty_pos

    def __hash__(self):
        return self.matrix[0][0] + self.matrix[1][2] - self.matrix[0][2] - self.matrix[2][1]

    def print(self):
        for x in self.matrix:
            print(x)



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
            print(state.matrix)
            if state.matrix == goal:
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
    



def expand(state: Node, cost: int=0):
    expansion = []

    matrix, pos = state.matrix,state.empty_pos
    size= len(matrix)
    col_size = len(matrix[0])
    row = pos//size
    col = pos%size
    # Move Up
    if(row!=0):
        copy_matrix = copy.deepcopy(matrix)
        zero,numb=matrix[row][col],matrix[row-1][col]
        copy_matrix[row][col],copy_matrix[row-1][col]=numb,zero
        expansion.append(Node(copy_matrix,(row-1)*size+col,manhattan(copy_matrix)+cost))
    # Move Down
    if(row!=(size-1)):
        copy_matrix = copy.deepcopy(matrix)
        zero,numb=matrix[row][col],matrix[row+1][col]
        copy_matrix[row][col],copy_matrix[row+1][col]=numb,zero
        expansion.append(Node(copy_matrix,(row+1)*size+col,manhattan(copy_matrix)+cost))
    # Move Left
    if(col!=0):
        copy_matrix = copy.deepcopy(matrix)
        zero,numb=matrix[row][col],matrix[row][col-1]
        copy_matrix[row][col],copy_matrix[row][col-1]=numb,zero
        expansion.append(Node(copy_matrix,row*size+(col-1),manhattan(copy_matrix)+cost))
    # Move Right
    if(col!=(col_size-1)):
        copy_matrix = copy.deepcopy(matrix)
        zero,numb=matrix[row][col],matrix[row][col+1]
        copy_matrix[row][col],copy_matrix[row][col+1]=numb,zero
        expansion.append(Node(copy_matrix,row*size+(col+1),manhattan(copy_matrix)+cost))

    for children in expansion:
        children.parent = state

    return expansion


def found_goal(states, goal: list):
    for state in states:
        if state.matrix == goal:
            return True
    return False

def calculate_z_pos(matrix: list):
    pos=0
    found=False
    for row in matrix:
        for col in row:
            if col==0:
                found=True
                break
            pos+=1
        if found:
            break
    
    return pos

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

def bfs(state: Node, max_depth: int = 100, goal: list=[[1,2,3],[4,5,6],[7,8,0]]):
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

def heuristic(state: Node, a_star: bool = False,max_depth: int = 20, goal: list=[[1,2,3],[4,5,6],[7,8,0]]):
    graph = Graph()
    stack = [state]
    graph.new_depth()
    graph.add_node(state, 1)

    depth = 1
    while depth != max_depth and len(stack) != 0:
        graph.new_depth()
        node = stack.pop(0)
        if node.matrix == goal:
            print("For goal:", node.matrix, "Depth: ",depth)
            _path = graph.path(node)
            print_solution(_path)
            return graph,depth
        else:
            if a_star:
                expanded = expand(node,depth)
            else :
                expanded = expand(node)
            [graph.add_node(x, depth + 1) for x in expanded]
            graph.visit(node)
            [stack.append(x) for x in expanded if x not in graph.visited]
            stack.sort(key=lambda node: node.cost)
        depth += 1



if __name__ == "__main__":
    start = [[4,3,8],[7,1,2],[0,5,6]]
    #start = [[1,2,3],[4,5,6],[7,0,8]]
    #start = [[0,2,3],[1,5,6],[4,7,8]]
    pos = calculate_z_pos(start)
    #print("--- BFS ---")
    #graph, depth = bfs(Node(start, pos))
    #print("--- GREEDY ---")
    #graph, depth = heuristic(Node(start, pos))
    print("--- GREEDY ---")
    graph, depth = heuristic(Node(start, pos),True)

