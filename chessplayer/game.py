import chess


class ChessGame:
    def __init__(self, board=None):
        self.chess_board = board if board is not None else chess.Board()

    def play(self, model_fcn):
        chess_board = self.chess_board
        print('Welcome to Chess \n')
        while chess_board.outcome() is None:
            print(chess_board)

            if chess_board.turn == chess.WHITE:
                user_move = input('Enter your move (e.g. d2d4, quit): ')
                if user_move == 'quit':
                    break
                while user_move not in [str(move) for move in chess_board.legal_moves]:
                    print('Invalid move, enter again in Standard Algebraic Notation')
                    user_move = input('Enter your move (e.g. d2d4, quit): ')

                chess_board.push_san(user_move)

            elif chess_board.turn == chess.BLACK:
                model_move = model_fcn(chess_board.fen())
                print(f'Model chose move: {model_move}')
                chess_board.push_san(model_move)

        print(chess_board.outcome())
