# =========================
# Init
# =====
.DEFAULT_GOAL := help
.SILENT:

# =========================
# Dependencies
# =====
dependencies.install:
	uv sync

dependencies.upgrade:
	uv sync --upgrade

dependencies.lock:
	uv lock

# =========================
# Git
# =====
git.init_hooks:
	uv run --only-dev pre-commit install
	uv run --only-dev pre-commit install --hook-type pre-push
	uv run --only-dev pre-commit install --hook-type commit-msg
	oco hook set

git.run_hooks_for_all:
	uv run --only-dev pre-commit run --all-files

# =========================
# Game
# =====
game.start:
	PYTHONPATH=. uv run --no-dev src/game/game.py

# =========================
# AI
# =====
ai.train:
	PYTHONPATH=. uv run --no-dev src/ai/ai.py

# =========================
# Scripts
# =====
script.dir_checker:
	PYTHONPATH=. uv run --no-sync scripts/dir_checker/main.py

script.python_checker:
	PYTHONPATH=. uv run --no-sync scripts/python_checker/main.py

# =========================
# Help
# =====
help:
	echo "available targets:"
	grep -E '^[a-zA-Z0-9][a-zA-Z0-9._-]*:' Makefile | sort | awk -F: '{print "  "$$1}'
