import random
import time

# Generate k-SAT problem with m clauses and n variables
def generate_k_sat(k, m, n):
    clauses = []
    for _ in range(m):
        clause = []
        variables = random.sample(range(1, n+1), k)  # Select k distinct variables
        for var in variables:
            if random.choice([True, False]):
                clause.append(var)  # Include the variable
            else:
                clause.append(-var)  # Include the negation of the variable
        clauses.append(clause)
    return clauses

# Evaluate the current solution (heuristic 1)
def evaluate_solution_heuristic1(assignment, clauses):
    satisfied_clauses = 0
    for clause in clauses:
        if any((lit > 0 and assignment[abs(lit)-1]) or (lit < 0 and not assignment[abs(lit)-1]) for lit in clause):
            satisfied_clauses += 1
    return satisfied_clauses

# Evaluate the current solution (heuristic 2 - negative count heuristic)
def evaluate_solution_heuristic2(assignment, clauses):
    satisfied_clauses = 0
    for clause in clauses:
        clause_val = sum((lit > 0 and assignment[abs(lit)-1]) or (lit < 0 and not assignment[abs(lit)-1]) for lit in clause)
        satisfied_clauses += clause_val
    return satisfied_clauses

### Hill-Climbing Algorithm
def hill_climbing(clauses, n, heuristic):
    assignment = [random.choice([True, False]) for _ in range(n)]
    best_score = heuristic(assignment, clauses)
    
    while True:
        neighbors = []
        for i in range(n):
            neighbor = assignment[:]
            neighbor[i] = not neighbor[i]  # Flip variable i
            neighbors.append(neighbor)
        
        best_neighbor = max(neighbors, key=lambda x: heuristic(x, clauses))
        best_neighbor_score = heuristic(best_neighbor, clauses)
        
        if best_neighbor_score > best_score:
            assignment = best_neighbor
            best_score = best_neighbor_score
        else:
            break  # No better neighbors found

    return assignment if best_score == len(clauses) else None

# Beam Search Algorithm
def beam_search(clauses, n, beam_width, heuristic):
    beam = [[random.choice([True, False]) for _ in range(n)] for _ in range(beam_width)]
    
    while True:
        expanded_states = []
        for state in beam:
            for i in range(n):
                new_state = state[:]
                new_state[i] = not new_state[i]  # Flip variable i
                expanded_states.append(new_state)
        
        beam = sorted(expanded_states, key=lambda x: heuristic(x, clauses), reverse=True)[:beam_width]
        
        for state in beam:
            if heuristic(state, clauses) == len(clauses):
                return state  # Found a solution

        if not beam:
            break  # Beam is empty, failure

    return None

# Variable Neighborhood Descent Algorithm
def variable_neighborhood_descent(clauses, n, neighborhood_funcs, heuristic):
    assignment = [random.choice([True, False]) for _ in range(n)]
    
    while True:
        for neighborhood_func in neighborhood_funcs:
            neighbors = neighborhood_func(assignment)
            best_neighbor = max(neighbors, key=lambda x: heuristic(x, clauses))
            best_neighbor_score = heuristic(best_neighbor, clauses)
            
            if best_neighbor_score > heuristic(assignment, clauses):
                assignment = best_neighbor
                break  # Move to better solution
        else:
            break  # No improvement, exit

    return assignment if heuristic(assignment, clauses) == len(clauses) else None

# Define 3 neighborhood functions
def flip_single_var(assignment):
    return [[not assignment[i] if i == idx else assignment[i] for i in range(len(assignment))] for idx in range(len(assignment))]

def flip_two_vars(assignment):
    neighbors = []
    for i in range(len(assignment)):
        for j in range(i+1, len(assignment)):
            neighbor = assignment[:]
            neighbor[i] = not neighbor[i]
            neighbor[j] = not neighbor[j]
            neighbors.append(neighbor)
    return neighbors

def flip_three_vars(assignment):
    neighbors = []
    for i in range(len(assignment)):
        for j in range(i+1, len(assignment)):
            for k in range(j+1, len(assignment)):
                neighbor = assignment[:]
                neighbor[i] = not neighbor[i]
                neighbor[j] = not neighbor[j]
                neighbor[k] = not neighbor[k]
                neighbors.append(neighbor)
    return neighbors

# Performance Testing and Comparison
def compare_algorithms(m_values, n_values):
    results = []
    
    for m in m_values:
        for n in n_values:
            print(f"Testing for m = {m}, n = {n}")
            
            # Generate random 3-SAT problem
            clauses = generate_k_sat(3, m, n)
            print(f"Generated 3-SAT problem with {m} clauses and {n} variables.")
            
            algorithms = [
                ("Hill-Climbing", hill_climbing, [evaluate_solution_heuristic1, evaluate_solution_heuristic2]),
                ("Beam Search (width=3)", lambda c, n: beam_search(c, n, 3, evaluate_solution_heuristic1), [evaluate_solution_heuristic1]),
                ("Beam Search (width=4)", lambda c, n: beam_search(c, n, 4, evaluate_solution_heuristic1), [evaluate_solution_heuristic1]),
                ("Variable Neighborhood Descent", variable_neighborhood_descent, [evaluate_solution_heuristic1, evaluate_solution_heuristic2]),
            ]

            neighborhood_funcs = [flip_single_var, flip_two_vars, flip_three_vars]
            
            for algo_name, algo_func, heuristics in algorithms:
                for heuristic in heuristics:
                    start_time = time.time()
                    if algo_name == "Variable Neighborhood Descent":
                        solution = algo_func(clauses, n, neighborhood_funcs, heuristic)
                    else:
                        solution = algo_func(clauses, n) if algo_name.startswith("Beam") else algo_func(clauses, n, heuristic)
                    
                    elapsed_time = time.time() - start_time
                    
                    heuristic_name = "Heuristic 1" if heuristic == evaluate_solution_heuristic1 else "Heuristic 2"
                    result = {
                        "Algorithm": algo_name,
                        "m": m,
                        "n": n,
                        "Heuristic": heuristic_name,
                        "Time (s)": elapsed_time,
                        "Solution Found": solution is not None
                    }
                    results.append(result)
                    print(result)
    
    return results

def main():
    # Take m and n values from user input
    m_values_input = input("Enter the m values (comma-separated): ")
    n_values_input = input("Enter the n values (comma-separated): ")

    # Convert input strings to lists of integers
    m_values = list(map(int, m_values_input.split(',')))
    n_values = list(map(int, n_values_input.split(',')))
    
    # Run the comparison
    results = compare_algorithms(m_values, n_values)
    for res in results:
        print(res)

if __name__ == "__main__":

    main()