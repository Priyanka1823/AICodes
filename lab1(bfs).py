from collections import deque


def bfs_solve(initial_state):
    queue = deque([(initial_state, [])])  
    visited = set([initial_state]) 
    node_visited = 0


    while queue:
        state, path = queue.popleft()
        node_visited += 1


        # Goal 
        if state == "WWW.EEE":
            # print(f"Total Nodes Visited : {node_visited}")
            print(f"Number of Nodes in Solution Path: {len(path) + 1}")
            return path + [state]

        
        index = state.index('.')

        # Explore all possible moves: -1, -2 (left), +1, +2 (right)
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

                    # If this new state hasn't been visited, add it to the queue
                    if new_state not in visited:
                        visited.add(new_state)
                        queue.append((new_state, path + [state]))

    return None 


initial_state = "EEE.WWW"
solution = bfs_solve(initial_state)

if solution:
    print("BFS Solution found:")
    for step in solution:
        print(step)
else:
    print("No BFS solution found.")