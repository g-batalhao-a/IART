from xlwt import Workbook
from graph import *
import json
import time
import random


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


def bfs(state: Node, max_depth: int = 15):
    states = [state]

    graph_bfs = Graph()
    graph_bfs.new_depth()
    graph_bfs.add_node(state, 1)
    for depth in range(1, max_depth + 1):
        expanded_states = []
        for node in states:
            if node.gamestate.finished():
                print("BFS OPT - Found Goal. Depth:", node.dist)
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
    return graph_bfs, None


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
            print("DFS - Found Goal. Depth:", node.dist)
            return graph_dfs, node
        else:
            expanded = new_states(node)
            [graph_dfs.add_node(x, x.dist + 1) for x in expanded]
            [stack.insert(0, x) for x in expanded if x not in graph_dfs.visited]

        depth += 1

    return graph_dfs, None


def ids(state: Node, max_depth: int = 1000):
    graph_ids = None
    for depth in range(1, max_depth):
        graph_ids, node = dfs(state, depth)
        if node is not None:
            return graph_ids, node

    return graph_ids, None


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
            stack.sort(key=lambda x: x.cost)
        graph.new_depth()
        node = stack.pop(0)

        if node.gamestate.finished():
            print("GREEDY - Found Goal. Depth:", node.dist)
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
    sheet_bfs_opt = wb.add_sheet('BFS OPT sheet', True)
    sheet_bfs = wb.add_sheet('BFS sheet', True)
    return wb, sheet_A, sheet_greedy, sheet_ids, sheet_dfs, sheet_bfs_opt, sheet_bfs


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

    wb, sheet_A, sheet_greedy, sheet_ids, sheet_dfs, sheet_bfs_opt, sheet_bfs = create_sheet()

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
        try:
            start = time.perf_counter()
            graph, goal = greedy(init_state, True)
            end = (time.perf_counter() - start)
            write_to_sheet(sheet_A, result, pos, end, game.num_of_colors, graph, graph.path(goal))
        except:
            print("No solution found! - A*")

        try:
            start = time.perf_counter()
            graph, goal = greedy(init_state, False)
            end = (time.perf_counter() - start)
            write_to_sheet(sheet_greedy, result, pos, end, game.num_of_colors, graph, graph.path(goal))
        except:
            print("No solution found! - Greedy")

        try:
            start = time.perf_counter()
            graph, goal = ids(init_state)
            end = (time.perf_counter() - start)
            write_to_sheet(sheet_ids, result, pos, end, game.num_of_colors, graph, graph.path(goal))
        except:
            print("No solution found! - IDS")

        try:
            start = time.perf_counter()
            graph, goal = dfs(init_state)
            end = (time.perf_counter() - start)
            write_to_sheet(sheet_dfs, result, pos, end, game.num_of_colors, graph, graph.path(goal))
        except:
            print("No solution found! - DFS")

        try:
            start = time.perf_counter()
            graph, goal = bfs(init_state)
            end = (time.perf_counter() - start)
            write_to_sheet(sheet_bfs, result, pos, end, game.num_of_colors, graph, graph.path(goal))
        except:
            print("No solution found! - BFS")

        result += 1
        wb.save('Results.xls')
