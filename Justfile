# query OSV for known malware before syncing
export UV_MALWARE_CHECK := "1"

# running plain "just" should not trigger a recipe, default to listing all recipes
[private]
default:
    @just --list --unsorted

# update the pinned prek hooks (with a 7 day cooldown)
[group("dependencies")]
update-prek-hooks:
    uv run --group quality prek update --freeze --cooldown-days=7
