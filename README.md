# ChessPlayer

A small neural-network chess opponent. A network learns a value function over
board positions (from `data/train.csv`), and the play policy picks the legal
move leading to the best-scored resulting position. You play White; the model
plays Black.

## Project layout

```
chessplayer/
  encoder.py   BoardEncoder  – one-hot encodes a board / FEN string
  model.py     ChessModel    – build, train, save, load, and pick moves
  game.py      ChessGame     – interactive human-vs-model play loop
train_model.py                – build a model from data and save it
play_model.py                 – load a saved model and play against it
data/                         – train.csv / test.csv
models/                       – saved .keras models
```

## Setup

```
.venv\Scripts\activate        # Windows (PowerShell)
pip install -r requirements.txt
```

## Run a saved model

A trained model ships in `models/chess_model.keras`. To play against it:

```
python play_model.py
```

Enter moves in UCI form (e.g. `d2d4`), or type `quit` to stop.

## Generate your own model and save it

Trains a new network on `data/train.csv` and writes it to
`models/chess_model.keras`:

```
python train_model.py
```
