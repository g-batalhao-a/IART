from tube import *

class Node:
    parent = None

    def __init__(self, gamestate: Game, cost: int=0, dist: int=0):
        self.gamestate = gamestate
        self.dist=dist
        self.cost=cost

    def __eq__(self, o):
        return o.gamestate == self.gamestate

    def __hash__(self):
        return self.matrix[0][0] + self.matrix[1][2] - self.matrix[0][2] - self.matrix[2][1]

    def print(self):
        self.gamestate.print()
        print("-----"*len(self.gamestate.tubes))
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

    def find_goals(self, level):
        sol = []
        for state in self.depth[level - 1]:
            if state.gamestate.finished():
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
    