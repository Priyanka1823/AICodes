import random

matchboxes = {}


def initialize_matchbox(state):
    matchboxes[state] = [1 for _ in range(9)]  # 9 possible moves (0-8)


# Function to choose a move based on the beads in the matchbox
def choose_move(state):
    if state not in matchboxes:
        initialize_matchbox(state)
    beads = matchboxes[state]
    total_beads = sum(beads)
    weighted_choices = [i for i, count in enumerate(beads) for _ in range(count)]
    return random.choice(weighted_choices)


# Reward Function
def update_matchbox(state, move, outcome):
    if state not in matchboxes:
        return
    if outcome == 'win':
        matchboxes[state][move] += 3
    elif outcome == 'draw':
        matchboxes[state][move] += 1
    elif outcome == 'lose':
        matchboxes[state][move] = max(1, matchboxes[state][move] - 1)


def play_game():
    states = []  # Store states and moves to update after the game
    board = [' '] * 9
    player = 'X'

    while ' ' in board:
        state = ''.join(board)
        if player == 'X':  # MENACE's turn
            move = choose_move(state)
        else:  # Random player move
            move = random.choice([i for i, x in enumerate(board) if x == ' '])

        board[move] = player
        states.append((state, move))

        # Check for a win or draw
        if check_win(board, player):
            return 'X' if player == 'X' else 'O', states
        if ' ' not in board:
            return 'draw', states

        player = 'O' if player == 'X' else 'X'

    return 'draw', states


# Function to check if a player has won
def check_win(board, player):
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),
                      (0, 4, 8), (2, 4, 6)]
    return any(all(board[i] == player for i in condition) for condition in win_conditions)


# Train MENACE over multiple games
for _ in range(1000):
    outcome, states = play_game()
    for state, move in states:
        update_matchbox(state, move, outcome)

# Output the matchbox configuration after training
print(matchboxes)


# Function to play interactively against MENACE
def play_against_menace():
    board = [' '] * 9
    player = 'X'
    while ' ' in board:
        state = ''.join(board)
        if player == 'X':  # MENACE's turn
            move = choose_move(state)
            print(f"MENACE plays at position {move}")
        else:
            print(f"Current board: {state}")
            move = int(input("Your move (0-8): "))
            while board[move] != ' ':
                move = int(input("Spot already taken. Choose another move (0-8): "))

        board[move] = player
        print(''.join(board))

        if check_win(board, player):
            print(f"{player} wins!")
            return

        player = 'O' if player == 'X' else 'X'

    print("It's a draw!")


# Let the user play against MENACE after training
play_against_menace()
