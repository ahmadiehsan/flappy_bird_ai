# =========================
# Init
# =====
.DEFAULT_GOAL := help

# =========================
# PreCommit
# =====
pre_commit.init:
	pre-commit install
	pre-commit install --hook-type pre-push
	pre-commit install --hook-type commit-msg
	oco hook set

pre_commit.run_for_all:
	pre-commit run --all-files

# =========================
# Requirements
# =====
requirements.compile:
	pip install -q poetry==1.8.5
	poetry update

requirements.install:
	pip install -q poetry==1.8.5
	poetry install

# =========================
# Game
# =====
game.start:
	PYTHONPATH=. python src/game/game.py

# =========================
# AI
# =====
ai.train:
	echo "Not implemented yet!"

# =========================
# Help
# =====
help:
	@echo "Available targets:"
	@grep -E '^[a-zA-Z0-9][a-zA-Z0-9._-]*:' Makefile | sort | awk -F: '{print "  "$$1}'
