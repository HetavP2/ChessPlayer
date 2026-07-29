import os

from chessplayer.model import ChessModel

os.makedirs('models', exist_ok=True)

model = ChessModel()
model.train('data/train.csv')
model.save('./models/chess_model.keras')
