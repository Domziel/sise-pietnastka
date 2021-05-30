import collections
import time
import itertools
import queue
from Result import Result
from Node import Node


def solve_bfs(search_order, rows, columns, initial_state, target_state):
    validate_directions(search_order)
    nodes_states = collections.OrderedDict()
    explored_states = dict()
    node_state = initial_state
    node = Node(None, None, 0)
    nodes_states[node_state] = node
    max_depth = 0

    start_time = time.perf_counter()
    if node_state == target_state:
        end_time = time.perf_counter()
        return Result(node, len(nodes_states) + len(explored_states), len(explored_states), 0, end_time - start_time,
                      node_state)
    while 1:
        zero_position = node_state.index("0")
        neighbours = get_neighbours(node_state, rows, columns, zero_position, search_order)
        for key in neighbours:
            neighbour = neighbours[key]
            if not (neighbour in nodes_states or neighbour in explored_states):
                new_node = Node(node, key, node.cost + 1)
                nodes_states[neighbour] = new_node
                if neighbour == target_state:
                    end_time = time.perf_counter()
                    return Result(new_node, len(nodes_states) + len(explored_states), len(explored_states),
                                  max_depth + 1, end_time - start_time, neighbour)
        explored_states[node_state] = nodes_states.pop(node_state)
        node_state = next(iter(nodes_states))
        node = nodes_states[node_state]
        max_depth = max(node.cost, max_depth)


def solve_dfs(search_order, rows, columns, initial_state, target_state, depth_limit):
    validate_directions(search_order)
    nodes_states = collections.OrderedDict()
    explored_states = dict()
    node_state = initial_state
    node = Node(None, None, 0)
    nodes_states[node_state] = node
    max_depth = 0
    visited_states_count = 1
    explored_states_count = 0

    start_time = time.perf_counter()
    if node_state == target_state:
        end_time = time.perf_counter()
        return Result(node, visited_states_count, explored_states_count, 0, end_time - start_time, node_state)
    while 1:
        zero_position = node_state.index("0")
        neighbours = get_neighbours(node_state, rows, columns, zero_position, search_order)
        for key, neighbour in reversed(neighbours.items()):
            is_visited = neighbour in nodes_states
            is_explored = neighbour in explored_states
            new_node = Node(node, key, node.cost + 1)
            if not (is_visited or is_explored):
                visited_states_count += 1
                if neighbour == target_state:
                    end_time = time.perf_counter()
                    return Result(new_node, visited_states_count, explored_states_count, max_depth + 1,
                                  end_time - start_time, neighbour)
                if new_node.cost < depth_limit:
                    nodes_states[neighbour] = new_node
                    nodes_states.move_to_end(neighbour, last=False)
            else:
                if is_visited and nodes_states[neighbour].cost > new_node.cost:
                    nodes_states[neighbour] = new_node
                    nodes_states.move_to_end(neighbour, last=False)
                elif is_explored and explored_states[neighbour].cost > new_node.cost:
                    nodes_states[neighbour] = new_node
                    nodes_states.move_to_end(neighbour, last=False)
                    explored_states[neighbour] = new_node
        if not (node_state in explored_states):
            explored_states_count += 1
        explored_states[node_state] = nodes_states.pop(node_state)
        if len(nodes_states) == 0:
            end_time = time.clock()
            return Result(node, visited_states_count, explored_states_count, max_depth, end_time - start_time,
                          node_state)
        node_state = next(iter(nodes_states))
        node = nodes_states[node_state]
        if node.cost < depth_limit:
            max_depth = max(node.cost, max_depth)


def solve_a_star(heuristic_choice, rows, columns, initial_state, target_state):
    heuristic = validate_heuristic(heuristic_choice)
    search_order = "LRUD"

    states_queue = queue.PriorityQueue()
    visited_states = dict()
    explored_states = dict()
    nodes_states = dict()
    node_state = initial_state
    node = Node(None, None, 0)
    nodes_states[node_state] = node
    max_depth = 0

    start_time = time.perf_counter()
    if node_state == target_state:
        end_time = time.perf_counter()
        return Result(node, len(visited_states) + len(explored_states), len(explored_states), 0,
                      end_time - start_time, node_state)
    while 1:
        zero_position = node_state.index("0")
        neighbours = get_neighbours(node_state, rows, columns, zero_position, search_order)
        for key in neighbours:
            neighbour = neighbours[key]
            if not (neighbour in visited_states or neighbour in explored_states):
                priority = node.cost + 1 + heuristic(neighbour, target_state, columns)
                visited_states[neighbour] = 1
                states_queue.put((priority, neighbour))
                nodes_states[neighbour] = Node(node, key, node.cost + 1)
                if neighbour == target_state:
                    end_time = time.perf_counter()
                    return Result(nodes_states[neighbour], len(visited_states) + len(explored_states),
                                  len(explored_states), max_depth + 1, end_time - start_time, neighbour)
        explored_states[node_state] = 1
        node_state = states_queue.get()[1]
        visited_states.pop(node_state)
        node = nodes_states[node_state]
        max_depth = max(node.cost, max_depth)


def get_neighbours(node_state, rows, columns, zero_position, search_order):
    neighbours = collections.OrderedDict()
    row = int(zero_position / columns)
    column = (zero_position % columns)

    for direction in search_order:
        if direction == "L":
            if column != 0:
                new_state = list(node_state)
                new_position = zero_position - 1
                new_state[zero_position] = new_state[new_position]
                new_state[new_position] = "0"
                neighbours["L"] = tuple(new_state)
        elif direction == "R":
            if column != columns - 1:
                new_state = list(node_state)
                new_position = zero_position + 1
                new_state[zero_position] = new_state[new_position]
                new_state[new_position] = "0"
                neighbours["R"] = tuple(new_state)
        elif direction == "U":
            if row != 0:
                new_state = list(node_state)
                new_position = zero_position - columns
                new_state[zero_position] = new_state[new_position]
                new_state[new_position] = "0"
                neighbours["U"] = tuple(new_state)
        elif direction == "D":
            if row != rows - 1:
                new_state = list(node_state)
                new_position = zero_position + columns
                new_state[zero_position] = new_state[new_position]
                new_state[new_position] = "0"
                neighbours["D"] = tuple(new_state)
    return neighbours


def hamming(node_state, target_state):
    wrong_position_count = 0
    for i in range(len(node_state)):
        if node_state[i] != target_state[i]:
            wrong_position_count += 1
    return wrong_position_count


def manhattan(node_state, target_state, columns):
    sum_of_distances = 0
    for i in range(len(node_state)):
        target_position = target_state.index(node_state[i])
        sum_of_distances += abs(i % columns - target_position % columns) + abs(
            int(i / columns) - int(target_position / columns))
    return sum_of_distances


def validate_directions(search_order):
    coma_separated_permutations = list(itertools.permutations(["L", "U", "D", "R"]))
    permutations = []
    for permutation in coma_separated_permutations:
        permutations.append(''.join(permutation))
    if search_order not in permutations:
        raise Exception("Incorrect search order: ", search_order)


def validate_heuristic(heuristic_choice):
    if heuristic_choice == "hamm":
        return hamming
    elif heuristic_choice == "manh":
        return manhattan
    else:
        raise Exception("Incorrect heuristic: ", heuristic_choice)
