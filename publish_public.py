import os
import shutil
import subprocess
from pathlib import Path


PRIVATE_REPO_DIR = Path.home() / "Git" / "stock-alert-system"
PUBLIC_REPO_DIR = Path.home() / "Git" / "investment-assistant-public"
PUBLIC_REPO_URL = "https://github.com/sharonwei2160/investment-assistant-public.git"

EXCLUDE_NAMES = {
    ".git",
    ".env",
    ".venv",
    "__pycache__",
    "data",
    "logs",
    "lambda_package",
    "lambda_deploy.zip",
}


def run_command(command, cwd=None):
    print(f"Running: {' '.join(command)}")
    subprocess.run(command, cwd=cwd, check=True)


def should_skip(path):
    return any(part in EXCLUDE_NAMES for part in path.parts)


def copy_project():
    if not PUBLIC_REPO_DIR.exists():
        run_command(["git", "clone", PUBLIC_REPO_URL, str(PUBLIC_REPO_DIR)])

    for item in PUBLIC_REPO_DIR.iterdir():
        if item.name == ".git":
            continue

        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()

    for item in PRIVATE_REPO_DIR.iterdir():
        if should_skip(item.relative_to(PRIVATE_REPO_DIR)):
            continue

        target = PUBLIC_REPO_DIR / item.name

        if item.is_dir():
            shutil.copytree(
                item,
                target,
                ignore=shutil.ignore_patterns(
                    ".git",
                    ".env",
                    ".venv",
                    "__pycache__",
                    "*.pyc",
                    "*.xlsx",
                    "*.csv",
                ),
            )
        else:
            if item.suffix in [".xlsx", ".csv"]:
                continue
            shutil.copy2(item, target)


def replace_private_files():
    private_watchlist = PUBLIC_REPO_DIR / "app" / "watchlist.json"
    sample_watchlist = PUBLIC_REPO_DIR / "app" / "watchlist_sample.json"

    if private_watchlist.exists():
        private_watchlist.unlink()

    if sample_watchlist.exists():
        shutil.copy2(sample_watchlist, private_watchlist)


def commit_and_push():
    run_command(["git", "add", "."], cwd=PUBLIC_REPO_DIR)

    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=PUBLIC_REPO_DIR,
        capture_output=True,
        text=True,
        check=True,
    )

    if not result.stdout.strip():
        print("No changes to publish.")
        return

    run_command(
        ["git", "commit", "-m", "Update public portfolio version"],
        cwd=PUBLIC_REPO_DIR,
    )
    run_command(["git", "push", "origin", "main"], cwd=PUBLIC_REPO_DIR)


def main():
    print("Start publishing public version...")
    copy_project()
    replace_private_files()
    commit_and_push()
    print("Public repository updated successfully.")


if __name__ == "__main__":
    main()