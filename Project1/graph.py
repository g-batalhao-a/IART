from tube import *


class Node:
    parent = None

    def __init__(self, gamestate: Game, cost: int = 0, dist: int = 0):
        self.gamestate = gamestate
        self.dist = dist
        self.cost = cost

    def __eq__(self, o):
        return self.gamestate.__eq__(o.gamestate)

    def __hash__(self):
        return ".".join([str(tube) for tube in self.gamestate.get_tubes()])

    def print(self):
        self.gamestate.print()
        print("-----" * len(self.gamestate.tubes))

    def __lt__(self, o):
        return (self.dist + self.cost) < (o.dist + o.cost)

    def setDist(self, newDist):
        self.dist = newDist

    def setCost(self, newCost):
        self.cost = newCost

    def setParent(self, node):
        self.parent = node

    def clone(self):
        return copy.deepcopy(self)

    def better_nWrong_heuristics(self):
        cost = 0

        for tube in self.gamestate.tubes:
            balls = tube.balls.copy()
            idx = next((i for i, v in enumerate(balls) if v != balls[0]), -1)
            if idx == -1:
                continue

            balls = balls[idx:]
            balls.reverse()
            
            for i, ball in enumerate(balls):
                cost += i + 1

        return cost
                


class Graph:

    def __init__(self, depth=None, visited=None):
        self.depth = [] if depth is None else depth
        self.visited = [] if visited is None else visited

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
        count = 0
        for level in self.depth:
            count += len(level)
        return count
