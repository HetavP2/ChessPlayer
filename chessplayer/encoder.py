import chess
import numpy as np


class BoardEncoder:
    def one_hot_encode_piece(self, piece):
        pieces = list('rnbqkpRNBQKP.')
        arr = np.zeros(len(pieces))
        piece_to_index = {p: i for i, p in enumerate(pieces)}
        index = piece_to_index[piece]
        arr[index] = 1
        return arr

    def one_hot_encode_board(self, chess_board):
        chess_board_str = str(chess_board)
        chess_board_str = chess_board_str.replace(' ', '')
        chess_board_list = []

        for row in chess_board_str.split('\n'):
            row_list = []
            for piece in row:
                row_list.append(self.one_hot_encode_piece(piece))
            chess_board_list.append(row_list)
        return np.array(chess_board_list)

    def encode_fen_string(self, fen):
        chess_board = chess.Board(fen=fen)
        return self.one_hot_encode_board(chess_board)
