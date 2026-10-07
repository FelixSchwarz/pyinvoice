#!/bin/sh
# Build the PyInstaller executable "dist/pyinvoice-<version>-linux-<arch>" from
# the wheel in "dist/" (see "just build") and the dependencies pinned in
# "uv.lock".
#
# usage: tools/build-executable.sh [PYTHON]
#
# PYTHON (default: "python3") must be a Python with a shared libpython which
# PyInstaller bundles together with all dependencies. The executable runs only on
# Linux systems with the same or a newer glibc than the build system.
set -eu

python="${1:-python3}"
version=$(tr -d '\n' < VERSION.txt)
arch=$(uname -m)
build_dir="build/executable"

wheel="dist/pyinvoice-$version-py3-none-any.whl"
if [ ! -f "$wheel" ]; then
    echo "$wheel not found, run \"just build\" first" >&2
    exit 1
fi

# A separate virtualenv so the project's ".venv" stays as it is.
export UV_PROJECT_ENVIRONMENT="$build_dir/venv"
uv sync --locked --no-install-project --no-default-groups --group executable --python "$python"
uv pip install --python "$UV_PROJECT_ENVIRONMENT" --no-deps --reinstall "$wheel"
uv run --no-sync pyinstaller --noconfirm --clean \
    --distpath "$build_dir/dist" --workpath "$build_dir/work" pyinvoice.spec

mkdir -p dist
executable="dist/pyinvoice-$version-linux-$arch"
cp "$build_dir/dist/pyinvoice" "$executable"

# The executable must be able to run our code, not just the bootloader.
reported_version=$("$executable" --version)
if [ "$reported_version" != "$version" ]; then
    echo "$executable reports version \"$reported_version\", expected \"$version\"" >&2
    exit 1
fi
echo "built $executable"
