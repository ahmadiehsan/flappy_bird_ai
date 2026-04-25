import "_share.just"
import "_working_dir.just"

play:
    PYTHONPATH=. uv run --no-dev src/game/game.py

train:
    PYTHONPATH=. uv run --no-dev src/ai/ai.py
