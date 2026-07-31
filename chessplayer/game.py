import chess


def count_material(fen):
    total_material = 0
    material_dict = {
        'p': 1,
        'b': 3,
        'n': 3,
        'r': 5,
        'q': 9
    }
    for char in fen.split(' ')[0].lower():
        if char in material_dict:
            total_material += material_dict[char]

    return total_material


def material_balance(fen):
    # Material from Black's perspective: positive = Black is up material.
    balance = 0
    material_dict = {
        'p': 1,
        'b': 3,
        'n': 3,
        'r': 5,
        'q': 9
    }
    for char in fen.split(' ')[0]:
        value = material_dict.get(char.lower())
        if value is not None:
            balance += value if char.islower() else -value

    return balance


def material_minimax(board, depth):
    # Best-case material balance (Black's perspective)
    if board.is_checkmate():
        return 1000 if board.turn == chess.WHITE else -1000
    if depth == 0 or board.is_game_over():
        return material_balance(board.fen())

    values = []
    for move in board.legal_moves:
        child = board.copy()
        child.push(move)
        values.append(material_minimax(child, depth - 1))

    return min(values) if board.turn == chess.WHITE else max(values)


class ChessGame:
    def __init__(self, board=None):
        self.chess_board = board if board is not None else chess.Board()

    def play(self, model_fcn):
        chess_board = self.chess_board
        positions = [chess_board.fen()]
        quit_game = False
        print('Welcome to Chess \n')
        while chess_board.outcome() is None:
            print(chess_board)

            if chess_board.turn == chess.WHITE:
                user_move = input('Enter your move (e.g. d2d4, quit): ')
                if user_move == 'quit':
                    quit_game = True
                    break
                while user_move not in [str(move) for move in chess_board.legal_moves]:
                    print('Invalid move, enter again in Standard Algebraic Notation')
                    user_move = input('Enter your move (e.g. d2d4, quit): ')

                chess_board.push_uci(user_move)

            elif chess_board.turn == chess.BLACK:
                model_move = model_fcn(chess_board.fen())
                print(f'Model chose move: {model_move}')
                chess_board.push_uci(model_move)

            positions.append(chess_board.fen())

        print(chess_board.outcome())
        return positions, self.result_value(quit_game)

    def result_value(self, quit_game, win_value=1000):
        # Training signal from Black's perspective: win = + win_value, loss = -win_value, draw = 0. quit = look at material
        outcome = self.chess_board.outcome()
        if outcome is not None and outcome.winner is not None:
            return win_value if outcome.winner == chess.BLACK else -win_value
        if outcome is not None:
            return 0
        return 100 * material_balance(self.chess_board.fen())
