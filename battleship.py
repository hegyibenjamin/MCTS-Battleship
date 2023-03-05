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
    return all(guess in ship_positions for guess in guesses)

def check_sunk_ships(ship_positions, guesses):
    sunk_ships = []
    for ship, length in ships.items():
        ship_cells = [cell for cell in ship_positions if cell in guesses]
        if len(ship_cells) == length:
            sunk_ships.append(ship)
    return sunk_ships

def play_again():
    choice = input('Do you want to play again? (y/n): ')
    return choice.lower() == 'y'


# Game loop
while True:
    os.system('cls' if os.name == 'nt' else 'clear')

    # Game setup
    player_board = create_board(board_size)
    ai_board = create_board(board_size)
    ai_ship_positions = []
    player_ship_positions = []

    for ship, length in ships.items():
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Player\'s Turn')
        print(f'Placing the {ship} ({length} cells).')
        print('Player\'s Board:')
        print_board(player_board)
        placement, ship_positions = get_ship_placement(player_board, ship, length)
        player_ship_positions.extend(ship_positions)
        player_board = placement

    for ship, length in ships.items():
        ai_placement, ship_positions = random_ship_placement(ai_board, ship, length)
        ai_ship_positions.extend(ship_positions)
    os.system('cls')
    print('AI\'s Board:')
    print_board(ai_board)

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        print('Player\'s Turn')
        print('Player\'s Board:')
        print_board(player_board)
        print('AI\'s Board:')
        print_board(ai_board)

        # Player's turn
        guess = get_player_guess()

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

        sunk_ships = check_sunk_ships(ai_ship_positions, player_ship_positions)
        if sunk_ships:
            print(f'You sunk the following ship(s): {", ".join(sunk_ships)}!')

        if check_victory(ai_ship_positions, player_ship_positions):
            print('Congratulations! You sank all the AI\'s ships!')
            break

        # AI's turn
        ai_guess = random.choice([(x, y) for x in range(board_size) for y in range(board_size)])
        if ai_guess in player_ship_positions:
            result = 'hit'
            player_ship_positions.remove(ai_guess)
        else:
            result = 'miss'

        update_board(player_board, ai_guess, result)

        print('\nAI\'s Guess:')
        print('Player\'s Board:')
        print_board(player_board)
        print(f'AI guessed: {chr(ai_guess[1] + ord("A"))}{ai_guess[0]} - {result}')

        if check_victory(player_ship_positions, ai_ship_positions):
            print('AI sank all your ships! You lost.')
            break

    if not play_again():
        break
