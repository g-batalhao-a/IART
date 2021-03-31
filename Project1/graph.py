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

    def getTotalCost(self):
        return self.cost - self.dist

    def clone(self):
        return copy.deepcopy(self)

    def number_of_wrong_heuristics(self):
        cost = 0
        
        for tube in self.gamestate.tubes:
            balls = tube.balls.copy()

            if(len(balls)==0): continue
            
            idx = next((i for i, v in enumerate(balls) if v != balls[0]), -1)
            if idx == -1: continue

            balls = balls[idx:]
            cost += len(balls)

        return cost

    def number_of_consecutive_heuristics(self):
        cost = 0
        dic = dict()

        for tube in self.gamestate.tubes:
            balls = tube.balls
            if (len(balls) == 0): continue

            for i in range(0, len(balls)):
                idx = next((x for x, v in enumerate(balls, start = i) if v != balls[i]), -1)
                if idx == -1:
                    dic.setdefault(balls[0],[]).append(len(balls) - i)
                    break
                else:
                    dic.setdefault(balls[0],[]).append(idx - i)

        for key in dic:
            cost += 4 - max(dic[key])

        return cost

    def node_score_heuristic(self):
        score = 0

        for tube in self.gamestate.tubes:
            balls = tube.balls.copy()

            if len(balls) == 0: 
                score += 10
            else:
                c1 = balls.pop(0)
                cnt = 1
                while len(balls) != 0:
                    c2 = balls.pop(0)
                    if c1 == c2:
                        cnt += 1
                    else:
                        c1 = c2
                        cnt = 1
                score += (5 * cnt)

        return score


class Graph:

    def __init__(self, depth=None, visited=None):
        self.depth = [] if depth is None else depth
        self.visited = [] if visited is None else visited

    def new_depth(self):
        self.depth.append([])

    def add_node(self, node: Node, level):
        while len(self.depth) < level:
            self.new_depth()

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
