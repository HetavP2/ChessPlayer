from chessplayer.model import ChessModel
from chessplayer.game import ChessGame

MODEL_PATH = './models/chess_model.keras'

model = ChessModel.load(MODEL_PATH)
game = ChessGame()

positions, result_value = game.play(model.play_nn)

print('\nUpdating the model from this game...')
model.learn_from_game(positions, result_value)
model.save(MODEL_PATH)
print('Model updated and saved.')
