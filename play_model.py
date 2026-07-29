from chessplayer.model import ChessModel
from chessplayer.game import ChessGame

model = ChessModel.load('./models/chess_model.keras')
game = ChessGame()
game.play(model.play_nn)
