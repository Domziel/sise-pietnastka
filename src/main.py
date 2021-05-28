import sys
import algorithms


def main(argv):
    if len(argv) != 6:
        raise Exception("Incorrect number of arguments")
    print("Provided arguments: ", argv[1:])

    strategy = argv[1]
    strategy_param = argv[2]
    initial_state_file = argv[3]
    solution_file = argv[4]
    additional_info_file = argv[5]

    initial_state, target_state, rows, columns = load_state(initial_state_file)
    result = solve_puzzle(strategy, strategy_param, rows, columns, initial_state, target_state)
    save_results(result, solution_file, additional_info_file, target_state)


def load_state(initial_state_file):
    file = open(initial_state_file)
    lines = file.readlines()
    file.close()

    rows = int(lines[0].split(" ")[0])
    columns = int(lines[0].split(" ")[1])
    initial_state = ()
    target_state = tuple([str(i) for i in range(1, rows * columns)] + ["0"])
    for line in lines[1:]:
        initial_state += tuple(line.replace("\n", "").split(" "))
    return initial_state, target_state, rows, columns


def save_results(result, solution_file, additional_info_file, target_state):
    time = '{0:.3f}'.format(result.time * 1000.0)
    print("Algorithm finished with time: ", time)
    solution = str()
    if result.state == target_state:
        node = result.node
        while node.operator is not None:
            solution = node.operator + solution
            node = node.parent_node
    else:
        solution = -1
        result.node.cost = -1

    file = open(solution_file, 'w+')
    if solution == -1:
        file.write("-1")
    else:
        file.write(str(result.node.cost) + "\n" + solution + "\n")
    file.close()

    file = open(additional_info_file, 'w+')
    file.write(
        str(result.node.cost) + "\n"
        + str(result.visited_states_count) + "\n"
        + str(result.explored_states_count) + "\n"
        + str(result.max_depth) + "\n"
        + str(time) + "\n"
    )
    file.close()


def solve_puzzle(strategy, strategy_param, rows, columns, initial_state, target_state):
    if strategy == "bfs":
        result = algorithms.solve_bfs(strategy_param, rows, columns, tuple(initial_state), target_state)
    elif strategy == "dfs":
        result = algorithms.solve_dfs(strategy_param, rows, columns, tuple(initial_state), target_state, 21)
    elif strategy == "astr":
        result = algorithms.solve_a_star(strategy_param, rows, columns, tuple(initial_state), target_state)
    else:
        raise Exception("Incorrect strategy: ", strategy)
    return result


main(sys.argv)
