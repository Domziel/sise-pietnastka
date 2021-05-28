class Result:
    def __init__(self, node, visited_states_count, explored_states_count, max_depth, time, state):
        self.node = node
        self.visited_states_count = visited_states_count
        self.explored_states_count = explored_states_count
        self.max_depth = max_depth
        self.time = time
        self.state = state
