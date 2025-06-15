# Chain Reaction Game with Minimax AI

This repository contains a simple implementation of the Chain Reaction board game.
It includes:

- `board.py` – game logic and board representation.
- `heuristics.py` – a set of evaluation heuristics for the AI.
- `ai.py` – minimax search with alpha–beta pruning.
- `human_vs_ai.py` – text UI using the file protocol described in the assignment.
- `ai_vs_ai.py` – run matches between two AI agents.

## Running

To play against the AI using the file protocol:

```bash
python3 human_vs_ai.py
```

This will create a `gamestate.txt` file. Edit the file after each AI move to
enter your move, then save it and the AI will respond.

For quick AI vs AI matches:

```bash
python3 ai_vs_ai.py
```
