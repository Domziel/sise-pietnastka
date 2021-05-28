import collections
import time
from Result import Result
from Node import Node


def solve_bfs(search_order, rows, columns, initial_state, target_state):
    nodes_states = collections.OrderedDict()
    explored_states = dict()
    node_state = initial_state
    node = Node(None, None, 0)
    nodes_states[node_state] = node
    max_depth = 0

    start_time = time.process_time()
    if node_state == target_state:
        end_time = time.process_time()
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
                    end_time = time.process_time()
                    return Result(new_node, len(nodes_states) + len(explored_states), len(explored_states),
                                  max_depth + 1, end_time - end_time, neighbour)
        explored_states[node_state] = nodes_states.pop(node_state)
        node_state = next(iter(nodes_states))
        node = nodes_states[node_state]
        max_depth = max(node.cost, max_depth)


def get_neighbours(node_state, rows, columns, zero_position, search_order):
    neighbours = collections.OrderedDict()
    row = int(zero_position / columns)
    column = (zero_position % columns)

    for direction in search_order:
        if direction == "L":
            if column != 0:
                new_state = node_state
                new_position = zero_position - 1
                new_state[zero_position] = new_state[new_position]
                new_state[new_position] = "0"
                neighbours["L"] = new_state
        elif direction == "R":
            if column != columns - 1:
                new_state = node_state
                new_position = zero_position + 1
                new_state[zero_position] = new_state[new_position]
                new_state[new_position] = "0"
                neighbours["R"] = new_state
        elif direction == "U":
            if row != 0:
                new_state = node_state
                new_position = zero_position - columns
                new_state[zero_position] = new_state[new_position]
                new_state[new_position] = "0"
                neighbours["U"] = new_state
        elif direction == "D":
            if row != rows - 1:
                new_state = list(node_state)
                new_position = zero_position + columns
                new_state[zero_position] = new_state[new_position]
                new_state[new_position] = "0"
                neighbours["D"] = new_state
    return neighbours
