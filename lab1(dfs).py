def dfs_solve(initial_state):
    stack = [(initial_state, [])]  # Stack stores (current state, path to current state)
    visited = set([initial_state])  

    while stack:
        state, path = stack.pop()

        # Goal check
        if state == "WWW.EEE":
            print(f"Number of Nodes in Solution Path: {len(path) + 1}")
            return path + [state]

        index = state.index('.')

        # Explore all possible moves
        for move in [-1, -2, 1, 2]:
            new_index = index + move
            if 0 <= new_index < len(state):  # Ensure we don't move out of bounds

                # Valid moves:
                if (move == 1 and state[new_index] == 'W') or \
                        (move == 2 and state[new_index] == 'W' and state[index + 1] == 'E') or \
                        (move == -1 and state[new_index] == 'E') or \
                        (move == -2 and state[new_index] == 'E' and state[index - 1] == 'W'):

                    # Swap the rabbits
                    new_state = list(state)
                    new_state[index], new_state[new_index] = new_state[new_index], new_state[index]
                    new_state = ''.join(new_state)

                    # If this new state hasn't been visited, add it to the stack
                    if new_state not in visited:
                        visited.add(new_state)
                        stack.append((new_state, path + [state]))

    return None 

initial_state = "EEE.WWW"
solution = dfs_solve(initial_state)

if solution:
    print("DFS Solution found:")
    for step in solution:
        print(step)
else:
    print("No DFS solution found.")