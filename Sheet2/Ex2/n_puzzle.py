import copy

class Node:
    parent = None

    def __init__(self, matrix, empty_pos, cost: int=0, dist: int=0):
        self.matrix = matrix
        self.empty_pos = empty_pos
        self.dist=dist
        self.cost=cost

    def __eq__(self, o):
        return o.matrix == self.matrix and o.empty_pos == self.empty_pos

    def __hash__(self):
        return self.matrix[0][0] + self.matrix[1][2] - self.matrix[0][2] - self.matrix[2][1]

    def print(self):
        for x in self.matrix:
            print(x)
        print("---------")
    def __lt__(self,o):
        return (self.dist+self.cost)<(o.dist+o.cost)
    def setDist(self,newDist):
        self.dist=newDist
    def setCost(self,newCost):
        self.cost=newCost
    def setParent(self,node):
        self.parent = node



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

    def expanded_states(self):
        count=0
        for level in self.depth:
            count+=len(level)
        return count
    



def expand(state: Node, a_star: bool=False):
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
        expansion.append(Node(copy_matrix,(row-1)*size+col,manhattan(copy_matrix),state.dist+1)) if a_star else expansion.append(Node(copy_matrix,(row-1)*size+col,manhattan(copy_matrix),0))
    # Move Down
    if(row!=(size-1)):
        copy_matrix = copy.deepcopy(matrix)
        zero,numb=matrix[row][col],matrix[row+1][col]
        copy_matrix[row][col],copy_matrix[row+1][col]=numb,zero
        expansion.append(Node(copy_matrix,(row+1)*size+col,manhattan(copy_matrix),state.dist+1)) if a_star else expansion.append(Node(copy_matrix,(row+1)*size+col,manhattan(copy_matrix),0))
    # Move Left
    if(col!=0):
        copy_matrix = copy.deepcopy(matrix)
        zero,numb=matrix[row][col],matrix[row][col-1]
        copy_matrix[row][col],copy_matrix[row][col-1]=numb,zero
        expansion.append(Node(copy_matrix,row*size+(col-1),manhattan(copy_matrix),state.dist+1)) if a_star else expansion.append(Node(copy_matrix,row*size+(col-1),manhattan(copy_matrix),0))
    # Move Right
    if(col!=(col_size-1)):
        copy_matrix = copy.deepcopy(matrix)
        zero,numb=matrix[row][col],matrix[row][col+1]
        copy_matrix[row][col],copy_matrix[row][col+1]=numb,zero
        expansion.append(Node(copy_matrix,row*size+(col+1),manhattan(copy_matrix),state.dist+1)) if a_star else expansion.append(Node(copy_matrix,row*size+(col+1),manhattan(copy_matrix),0))

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
            expanded = expand(node,a_star)
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


if __name__ == "__main__":
    #start = [[5,2,8],[4,1,7],[0,3,6]]
    #start = [[1,2,3],[4,5,6],[7,0,8]]
    #start = [[0,2,3],[1,5,6],[4,7,8]]
    start = [[5,1,3,4],[2,0,7,8],[10,6,11,12],[9,13,14,15]]
    pos = calculate_z_pos(start)
    if(checkSolvability(start)):
        print(start," is solvable")
    else:
        print(start," isn't solvable")
    #print("--- BFS ---")
    #graph, depth = bfs(Node(start, pos))
    print("--- GREEDY ---")
    graph, depth = heuristic(Node(start, pos),False,1000000,[[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]])
    print(graph.expanded_states())

    #print("--- A* ---")
    #graph, depth = heuristic(Node(start, pos),True,1000000,[[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]])
    #print(graph.expanded_states())

