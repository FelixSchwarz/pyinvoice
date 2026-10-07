# query OSV for known malware before syncing
export UV_MALWARE_CHECK := "1"

# running plain "just" should not trigger a recipe, default to listing all recipes
[private]
default:
    @just --list --unsorted

# run the test suite
[group("development")]
run-tests:
    uv run --locked --extra testing pytest

# create/update the project virtualenv with all extras and the quality tools
[group("development")]
setup-venv:
    uv sync --locked --all-extras --group=quality

# install the build backend pinned by the current lockfile
[group("dependencies")]
install-locked-dependencies:
    uv sync --locked --only-group build

# update "uv.lock" to the latest versions
[group("dependencies")]
update-dependencies:
    uv lock --upgrade

# update the pinned prek hooks (with a 7 day cooldown)
[group("dependencies")]
update-prek-hooks:
    uv run --group quality prek update --freeze --cooldown-days=7
