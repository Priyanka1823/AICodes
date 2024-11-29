
import numpy as np

# Define the size of the board
N = 8  # 8x8 chessboard

# Define parameters for the energy function
alpha = 1  # Penalty for multiple rooks in a row
beta = 1  # Penalty for multiple rooks in a column

# Initialize the state of the network (random initial state)
# A board of size 8x8 with values +1 or -1 (binary representation)
state = np.random.choice([-1, 1], size=(N, N))


# Energy function definitions
def energy_row(state):
    """Energy function for the row constraint (one rook per row)"""
    return np.sum((np.sum(state, axis=1) - 1) ** 2)


def energy_col(state):
    """Energy function for the column constraint (one rook per column)"""
    return np.sum((np.sum(state, axis=0) - 1) ** 2)


def total_energy(state):
    """Total energy combining row and column penalties"""
    return alpha * energy_row(state) + beta * energy_col(state)


# Weight matrix calculation
def weight_matrix(N):
    """Generate the weight matrix based on the row and column constraints"""
    W = np.zeros((N * N, N * N))  # Weight matrix for the network
    for i in range(N):
        for j in range(N):
            for k in range(N):
                for l in range(N):
                    if i == k and j != l:
                        W[i * N + j, k * N + l] = -alpha  # Same row
                    elif j == l and i != k:
                        W[i * N + j, k * N + l] = -beta  # Same column
    return W


# Update function for the network
def update_state(state, W):
    """Update the state of the network (asynchronous update rule)"""
    N = state.shape[0]
    for i in range(N):
        for j in range(N):
            # Compute the net input to the neuron
            net_input = np.dot(W[i * N + j, :], state.flatten())
            # Update neuron state
            state[i, j] = 1 if net_input > 0 else -1
    return state


# Hopfield network for the eight-rook problem
def solve_eight_rook():
    """Solve the Eight-Rook problem using Hopfield network"""
    W = weight_matrix(N)  # Generate weight matrix
    state = np.random.choice([-1, 1], size=(N, N))  # Initialize state
    energy = total_energy(state)
    print(f"Initial energy: {energy}")

    # Iteratively update the state until convergence
    max_iterations = 1000
    tolerance = 1e-5  # Convergence tolerance
    for _ in range(max_iterations):
        # Update state
        new_state = update_state(state, W)
        new_energy = total_energy(new_state)

        # Check for convergence (if the energy doesn't change significantly)
        if abs(new_energy - energy) < tolerance:
            break

        state = new_state
        energy = new_energy

    return state


# Solve the problem
solution = solve_eight_rook()

# Output the solution
print("Final configuration of rooks (1 means rook is placed, -1 means empty):")
print(solution)