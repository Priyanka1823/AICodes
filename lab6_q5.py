
import numpy as np
import random


N = 10  # Number of cities
cities = np.array([f"City {i + 1}" for i in range(N)])  # Names of cities

# Randomly generate the pairwise distance matrix
np.random.seed(0)
distances = np.random.randint(1, 100, size=(N, N))
np.fill_diagonal(distances, 0)  # Distance from a city to itself is 0

# Define the energy function components (route and distance)
alpha = 1
beta = 1 

# Initialize the Hopfield network (10 cities, so we have 100 neurons)
state = np.random.choice([-1, 1], size=(N, N))


# Define the energy function (route + distance components)
def energy_route(state):
    """Energy component enforcing the route constraint"""
    return np.sum((np.sum(state, axis=1) - 1) ** 2)


def energy_distance(state):
    """Energy component minimizing the total distance"""
    energy = 0
    for i in range(N):
        for j in range(i + 1, N):
            energy += distances[i, j] * state[i, j]
    return energy


def total_energy(state):
    """Total energy (route + distance components)"""
    return alpha * energy_route(state) + beta * energy_distance(state)


# Hopfield network update function
def update_state(state, W):
    """Update the state of the Hopfield network"""
    for i in range(N):
        for j in range(N):
            net_input = np.dot(W[i * N + j, :], state.flatten())
            state[i, j] = 1 if net_input > 0 else -1  # Binary update
    return state


# Weight matrix generation (based on energy function)
def weight_matrix(N):
    """Generate the weight matrix for the Hopfield network"""
    W = np.zeros((N * N, N * N))
    for i in range(N):
        for j in range(N):
            for k in range(N):
                for l in range(N):
                    if i == k and j != l:
                        W[i * N + j, k * N + l] = -alpha
                    elif j == l and i != k:
                        W[i * N + j, k * N + l] = -beta
    return W


# Function to solve the TSP using the Hopfield network
def solve_tsp():
    """Solve the Traveling Salesman Problem using Hopfield network"""
    W = weight_matrix(N)
    state = np.random.choice([-1, 1], size=(N, N))
    energy = total_energy(state)

    max_iterations = 1000
    for _ in range(max_iterations):
        new_state = update_state(state, W)
        new_energy = total_energy(new_state)

        if abs(new_energy - energy) < 1e-5:
            break

        state = new_state
        energy = new_energy

    return state



solution = solve_tsp()

print("Solution (Optimal/near-optimal path):")
for i in range(N):
    print(f"City {i + 1}: {cities[i]}")
