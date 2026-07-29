import chess
import numpy as np
import pandas as pd
import random
from keras.layers import Dense, Flatten
from keras.models import Sequential, load_model

from chessplayer.encoder import BoardEncoder


class ChessModel:
    def __init__(self, model=None):
        self.encoder = BoardEncoder()
        self.model = model

    def train(self, data_path='data/train.csv'):
        train_data = pd.read_csv(data_path, index_col='id')
        val_data = train_data[-1000:]
        train_data = train_data[:20000]

        X_train = np.stack(train_data['board'].apply(self.encoder.encode_fen_string))
        y_train = train_data['black_score']

        X_val = np.stack(val_data['board'].apply(self.encoder.encode_fen_string))
        y_val = val_data['black_score']

        # Make the neural nets
        self.model = Sequential([
            Flatten(),  # input
            Dense(4096, activation='relu'),  # hidden layers, can add more layers/epochs
            Dense(1),  # output
        ])

        self.model.compile(
            optimizer='rmsprop',
            loss='mean_squared_error'
        )

        self.model.fit(X_train, y_train, epochs=50, validation_data=(X_val, y_val))
        return self.model

    def save(self, path='./models/chess_model.keras'):
        self.model.save(path)

    @classmethod
    def load(cls, path='./models/chess_model.keras'):
        return cls(model=load_model(path))

    def play_random(self, fen):
        chess_board = chess.Board(fen=fen)
        move = random.choice(list(chess_board.legal_moves))
        return str(move)

    # value fcn above used to create a policy
    def play_nn(self, fen, show_move_evaluations=False):
        board = chess.Board(fen=fen)

        moves = []
        input_vectors = []

        for move in board.legal_moves:
            possible_board = board.copy()
            possible_board.push(move)
            moves.append(move)
            input_vectors.append(self.encoder.one_hot_encode_board(possible_board).astype(np.int32))

        input_vectors = np.stack(input_vectors)

        scores = self.model.predict(input_vectors, verbose=0)

        if board.turn == chess.BLACK:
            index_of_best_move = np.argmax(scores)
        else:
            index_of_best_move = np.argmax(-scores)

        if show_move_evaluations:
            print(zip(moves, scores))

        best_move = moves[index_of_best_move]

        return str(best_move)
