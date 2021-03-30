from xlwt import Workbook
from graph import *
import json
import time
import random
from enum import Enum


class Algorithm(Enum):
    BFS = 1
    DFS = 2
    IDS = 3
    GREEDY = 4
    A_STAR = 5


def expand_node(node: Node, visited, algorithm: Algorithm):
    expansion = []
    moves = node.gamestate.expand()

    for move in moves:
        new_gamestate = node.gamestate.clone()
        from_i, to_i = move
        new_gamestate.move_ball(from_i, to_i)
        new_node = Node(new_gamestate, 0, node.dist + 1)

        if algorithm == Algorithm.GREEDY or algorithm == Algorithm.A_STAR:
            new_node.setCost(new_node.number_of_wrong_heuristics())

        expansion.append(new_node)

    for children in expansion:
        children.parent = node

    return expansion


def get_stack_item(stack, item):
    try:
        idx = stack.index(item)
        return stack[idx]
    except:
        return None


def add_states_to_stack(stack, new_states, algorithm: Algorithm, node: Node):
    if algorithm == Algorithm.BFS:
        stack = stack + new_states
    elif algorithm == Algorithm.DFS or algorithm == Algorithm.IDS:
        stack = new_states + stack
    elif algorithm == Algorithm.GREEDY:
        stack = stack + new_states
        stack.sort(key=lambda x: x.cost)
    elif algorithm == Algorithm.A_STAR:
        for children in new_states:
            stack_node = get_stack_item(stack, children)
            if stack_node is not None:
                if children.getTotalCost() < stack_node.getTotalCost():
                    stack_node.setParent(node)
                    stack_node.setDist(node.dist + 1)
            else:
                stack.append(children)

        stack.sort(key=lambda x: x.getTotalCost())

    return stack


def check_final_depth_solution(expanded: list):
    for node in expanded:
        if node.gamestate.finished():
            print("Found goal!")
            return node

    return None


def solver(start_node: Node, algorithm: Algorithm, max_depth: int = 5000):
    graph = Graph()
    stack = [start_node]

    graph.new_depth()
    graph.add_node(start_node, 1)

    graph.new_depth()

    while len(stack) != 0:
        node = stack.pop(0)

        visited_node = get_stack_item(graph.visited, node)
        if visited_node is not None and node.dist >= visited_node.dist:
            continue

        graph.visit(node)
        graph.add_node(node, node.dist + 1)

        if algorithm != Algorithm.IDS and node.gamestate.finished():
            print("Found goal!")
            return graph, node

        expanded = expand_node(node, graph.visited, algorithm)

        if node.dist < max_depth - 1:
            stack = add_states_to_stack(stack, expanded, algorithm, node)
        else:
            solution = check_final_depth_solution(expanded)
            if solution is not None:
                return graph, solution

    return graph, None


def ids(start_node: Node, max_depth: int = 5000):
    graph = None
    for depth in range(1, max_depth):
        graph, node = solver(start_node, Algorithm.IDS, depth)
        if node is not None:
            return graph, node

    return graph, None


# doesnt print anything (used for interface)
def greedy_np(state: Node, a_star: bool = False, max_depth: int = 1000):
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
            stack.sort(key=lambda x: x.cost)
        graph.new_depth()
        node = stack.pop(0)
        if node.gamestate.finished():
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

        depth += 1


def print_solution(path: list):
    [x.print() for x in path]


def generate_puzzle(colors: int):
    balls_list = []
    for i in range(1, colors + 1):
        color = [i] * 4
        balls_list += color
    random.shuffle(balls_list)

    tubes_list = []
    pos = 0
    for i in range(colors):
        tubes_list.append(Tube(balls_list[pos:pos + 4]))
        pos += 4
    tubes_list.append(Tube([]))
    tubes_list.append(Tube([]))

    return Game(tubes_list)


def create_sheet():
    wb = Workbook()
    sheet_A = wb.add_sheet('A_star sheet', True)
    sheet_greedy = wb.add_sheet('Greedy sheet', True)
    sheet_ids = wb.add_sheet('IDS sheet', True)
    sheet_dfs = wb.add_sheet('DFS sheet', True)
    sheet_bfs = wb.add_sheet('BFS sheet', True)
    return wb, sheet_A, sheet_greedy, sheet_ids, sheet_dfs, sheet_bfs


def write_to_sheet(sheet, row, col, exec_time, size, graph, path):
    sheet.write(0, 0, "Expanded States")
    sheet.write(0, 1, "Solution Size")
    sheet.write(0, 2, "Time")
    sheet.write(0, 3, "Puzzle Size")
    sheet.write(row, col, graph.expanded_states())
    if path is not None:
        sheet.write(row, col + 1, len(path))
    else:
        sheet.write(row, col + 1, "Failed")
    sheet.write(row, col + 2, exec_time)
    sheet.write(row, col + 3, size)


if __name__ == "__main__":

    wb, sheet_A, sheet_greedy, sheet_ids, sheet_dfs, sheet_bfs = create_sheet()

    with open('levels.json') as f:
        levels = json.load(f)

    for level in levels:
        tubes = levels[level]['tubes']
        new_tubes = []
        for tube in tubes:
            new_tubes.append(Tube(tube))
        levels[level] = new_tubes

    pos = 0
    result = 1
    for level in levels:
        game = Game(levels[level])
        init_state = Node(game)
        """
        try:
            start = time.perf_counter()
            graph, goal = solver(init_state, Algorithm.A_STAR, 30)
            end = (time.perf_counter() - start)
            write_to_sheet(sheet_A, result, pos, end, game.num_of_colors, graph, graph.path(goal))
        except:
            print("No solution found! - A*")

        try:
            start = time.perf_counter()
            graph, goal = solver(init_state, Algorithm.GREEDY, 30)
            end = (time.perf_counter() - start)
            write_to_sheet(sheet_greedy, result, pos, end, game.num_of_colors, graph, graph.path(goal))
        except:
            print("No solution found! - Greedy")

        """
        try:
            start = time.perf_counter()
            graph, goal = ids(init_state, 60)
            end = (time.perf_counter() - start)
            write_to_sheet(sheet_ids, result, pos, end, game.num_of_colors, graph, graph.path(goal))
        except:
            print("No solution found! - IDS")
        """
        try:
            start = time.perf_counter()
            graph, goal = solver(init_state, Algorithm.DFS, 60)
            end = (time.perf_counter() - start)
            write_to_sheet(sheet_dfs, result, pos, end, game.num_of_colors, graph, graph.path(goal))
        except:
            print("No solution found! - DFS")

        try:
            start = time.perf_counter()
            graph, goal = solver(init_state, Algorithm.BFS, 15)
            end = (time.perf_counter() - start)
            write_to_sheet(sheet_bfs, result, pos, end, game.num_of_colors, graph, graph.path(goal))
        except:
            print("No solution found! - BFS")
        """

        result += 1
        wb.save('Results.xls')
