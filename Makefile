# =========================
# Init
# =====
.DEFAULT_GOAL := help
.SILENT:

# =========================
# Requirements
# =====
requirements.compile:
	uv lock

# =========================
# PreCommit
# =====
pre_commit.init:
	uv run pre-commit install
	uv run pre-commit install --hook-type pre-push
	uv run pre-commit install --hook-type commit-msg
	oco hook set

pre_commit.run_for_all:
	uv run pre-commit run --all-files

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
# Help
# =====
help:
	echo "available targets:"
	grep -E '^[a-zA-Z0-9][a-zA-Z0-9._-]*:' Makefile | sort | awk -F: '{print "  "$$1}'
