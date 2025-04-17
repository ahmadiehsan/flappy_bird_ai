# =========================
# Init
# =====
.DEFAULT_GOAL := help
.SILENT:

# =========================
# Game
# =====
game.start:
	PYTHONPATH=. uv run src/game/game.py

# =========================
# AI
# =====
ai.train:
	PYTHONPATH=. uv run src/ai/ai.py

# =========================
# Scripts
# =====
script.dir_checker:
	PYTHONPATH=. uv run --no-sync scripts/dir_checker/main.py

script.python_checker:
	PYTHONPATH=. uv run --no-sync scripts/python_checker/main.py

# =========================
# Dependencies
# =====
dependencies.lock:
	uv lock

dependencies.upgrade:
	uv lock --upgrade

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
# Help
# =====
help:
	echo "available targets:"
	grep -E '^[a-zA-Z0-9][a-zA-Z0-9._-]*:' Makefile | sort | awk -F: '{print "  "$$1}'
