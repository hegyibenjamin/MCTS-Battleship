import random
import os

# Game setup
board_size = 10
ships = {'Carrier': 5, 'Battleship': 4, 'Cruiser': 3, 'Submarine': 3, 'Destroyer': 2}

def create_board(size):
    board = [['O' for _ in range(size)] for _ in range(size)]
    return board

def print_board(board):
    print('     A B C D E F G H I J')
    for i in range(len(board)):
        row = ' '.join(board[i])
        if i+1<10:
            print(f'{i+1}    {row}')
        else:
            print(f'{i+1}   {row}')

def place_ship(board, ship, length, orientation, x, y):
    ship_positions = []
    if orientation == 'h':
        positions = [(x, y + i) for i in range(length)]
    else:
        positions = [(x + i, y) for i in range(length)]
    for x, y in positions:
        board[x][y] = 'S'
        ship_positions.append((x, y))
    return board, ship_positions

def random_ship_placement(board, ship, length):
    while True:
        orientation = random.choice(['h', 'v'])
        x = random.randint(0, board_size - 1)
        y = random.randint(0, board_size - 1)

        if orientation == 'h':
            if y + length > board_size:
                continue
        else:
            if x + length > board_size:
                continue

        board_copy = [row[:] for row in board]
        new_board, ship_positions = place_ship(board_copy, ship, length, orientation.lower(), x, y)
        if new_board is None:
            continue
        
        return new_board, ship_positions

def get_ship_placement(board, ship, length):
    while True:
        print(f'Placing the {ship} ({length} cells).')
        orientation = input('Enter the orientation (h for horizontal, v for vertical): ')
        if orientation.lower() not in ['h', 'v']:
            print('Invalid orientation. Please try again.')
            continue

        coordinate = input('Enter the starting coordinate (e.g., A3): ')
        if not is_valid_coordinate(coordinate):
            print('Invalid coordinate. Please try again.')
            continue

        x, y = convert_coordinate(coordinate)
        
        if orientation.lower() == 'h':
            if y + length > board_size:
                print('Invalid placement. The ship goes out of bounds. Please try again.')
                continue
        else:
            if x + length > board_size:
                print('Invalid placement. The ship goes out of bounds. Please try again.')
                continue

        board_copy = [row[:] for row in board]
        new_board, ship_positions = place_ship(board_copy, ship, length, orientation.lower(), x, y)
        if new_board is None:
            print('Invalid placement. Ships overlap or go out of bounds. Please try again.')
            continue

        return new_board, ship_positions

def convert_coordinate(coordinate):
    column = ord(coordinate[0].upper()) - ord('A')
    row = int(coordinate[1:])-1 
    return row, column

def is_valid_coordinate(coordinate):
    if len(coordinate) < 2:
        return False
    row, column = convert_coordinate(coordinate)
    return 0 <= column < board_size and 0 <= row < board_size

def get_player_guess():
    while True:
        guess = input('Enter your guess (e.g., A3): ')
        if is_valid_coordinate(guess):
            return convert_coordinate(guess)
        else:
            print('Invalid guess. Please try again.')

def evaluate_guess(guess, ship_positions):
    if guess in ship_positions:
        return 'hit'
    else:
        return 'miss'

def update_board(board, guess, result):
    row, col = guess
    if result == 'hit':
        board[row][col] = 'X'
    else:
        board[row][col] = 'M'

def check_victory(ship_positions, guesses):
    return all(position in guesses for position in ship_positions)

def play_again():
    choice = input('Do you want to play again? (y/n): ')
    return choice.lower() == 'y'

def monte_carlo_tree_search(board, ship_positions, ai_guesses):
    available_positions = [(x, y) for x in range(board_size) for y in range(board_size) if (x, y) not in ai_guesses]
    best_score = float('-inf')
    best_guess = None
    depth = 40
    for _ in range(10):
        guess = random.choice(available_positions)
        score = simulate_guess(board, ship_positions, guess, depth)
        if score > best_score:
            best_score = score
            best_guess = guess
    return best_guess

def simulate_guess(board, ship_positions, guess,depth):
    board_copy = [row[:] for row in board]
    ship_positions_copy=[position[:] for position in ship_positions]
    score=0
    if guess in ship_positions:
        result = 'hit'
        ship_positions_copy.remove(guess)
        score = score + 1/17
    else:
        result = 'miss'
    score = score + simulate_random_guesses(board_copy, ship_positions_copy,depth)
    print(score)
    return score

def simulate_random_guesses(board, ship_positions,depth):
    guesses = []
    hits=0
    i=0
    while (ship_positions and i!=depth):
        i = i + 1
        guess = random.choice([(x, y) for x in range(board_size) for y in range(board_size) if (x, y) not in guesses])
        guesses.append(guess)
        if guess in ship_positions:
            ship_positions.remove(guess)
            hits+=1
    return hits/depth
# Game loop
while True:
    os.system('cls' if os.name == 'nt' else 'clear')

    # Game setup
    player_board = create_board(board_size)
    ai_board = create_board(board_size)
    ai_ship_positions = []
    player_ship_positions = []
    player_guesses = []
    ai_guesses = []
    test=True
    if test:
        player_ship_positions=[(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 2), (1, 3), (2, 0), (2, 1), (2, 2), (3, 0), (3, 1), (3, 2), (4, 0), (4, 1)]
        player_board=[['S', 'S', 'S', 'S', 'S', 'O', 'O', 'O', 'O', 'O'], ['S', 'S', 'S', 'S', 'O', 'O', 'O', 'O', 'O', 'O'], ['S', 'S', 'S', 'O', 'O', 'O', 'O', 'O', 'O', 'O'], ['S', 'S', 'S', 'O', 'O', 'O', 'O', 'O', 'O', 'O'], ['S', 'S', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'], ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'], ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'], ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'], ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'], ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']]
    else:
        # Player setup
        for ship, length in ships.items():
            os.system('cls' if os.name == 'nt' else 'clear')
            print('Player\'s Turn')
            print(f'Placing the {ship} ({length} cells).')
            print('Player\'s Board:')
            print_board(player_board)
            placement, ship_positions = get_ship_placement(player_board, ship, length)
            player_ship_positions.extend(ship_positions)
            player_board = placement
    # AI setup
    for ship, length in ships.items():
        ai_placement, ship_positions = random_ship_placement(ai_board, ship, length)
        ai_ship_positions.extend(ship_positions)

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        print('Player\'s Turn')
        print('Player\'s Board:')
        print_board(player_board)
        print('AI\'s Board:')
        print_board(ai_board)

        # Player's turn
        guess = get_player_guess()
        player_guesses.extend(guess)

        if guess in ai_ship_positions:
            result = 'hit'
            ai_ship_positions.remove(guess)
        else:
            result = 'miss'

        update_board(ai_board, guess, result)

        if result == 'hit':
            print('You hit a ship!')
        else:
            print('You missed.')

        if check_victory(ai_ship_positions, player_guesses):
            print('Congratulations! You sank all the AI\'s ships!')
            break

        # AI's turn
        ai_guess = monte_carlo_tree_search(player_board, player_ship_positions, ai_guesses)
        ai_guesses.extend(ai_guess)
        if ai_guess in player_ship_positions:
            result = 'hit'
            player_ship_positions.remove(ai_guess)
        else:
            result = 'miss'

        update_board(player_board, ai_guess, result)
        
        print('\nAI\'s Guess:')
        print(f'AI guessed: {chr(ai_guess[1] + ord("A"))}{ai_guess[0]+1} - {result}')

        if check_victory(player_ship_positions, ai_guesses):
            print('AI sank all your ships! You lost.')
            break
    if not play_again():
        break
