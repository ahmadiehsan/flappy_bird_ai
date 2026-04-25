import "_share.just"
import "_working_dir.just"

dir_checker:
    uv run --only-dev dir_checker

python_checker:
    uv run --only-dev python_checker

just_indexer:
    uv run --only-dev just_indexer .just
