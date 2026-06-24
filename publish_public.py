import re
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

EXCLUDE_SUFFIXES = {
    ".xlsx",
    ".csv",
    ".db",
    ".sqlite",
}

SECRET_PATTERNS = [
    r"github_pat_[A-Za-z0-9_]+",
    r"ghp_[A-Za-z0-9_]+",
    r"Bearer\s+(github_pat_|ghp_)[A-Za-z0-9_]+",
    r"AKIA[0-9A-Z]{16}",
    r"aws_secret_access_key\s*=\s*[A-Za-z0-9/+=]{20,}",
]


def run_command(command, cwd=None):
    print(f"Running: {' '.join(command)}")
    subprocess.run(command, cwd=cwd, check=True)


def should_skip(path):
    if any(part in EXCLUDE_NAMES for part in path.parts):
        return True

    if path.suffix in EXCLUDE_SUFFIXES:
        return True

    return False


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
        relative_path = item.relative_to(PRIVATE_REPO_DIR)

        if should_skip(relative_path):
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
                    "*.db",
                    "*.sqlite",
                ),
            )
        else:
            shutil.copy2(item, target)


def replace_private_files():
    private_watchlist = PUBLIC_REPO_DIR / "app" / "watchlist.json"
    sample_watchlist = PUBLIC_REPO_DIR / "app" / "watchlist_sample.json"

    if private_watchlist.exists():
        private_watchlist.unlink()

    if sample_watchlist.exists():
        shutil.copy2(sample_watchlist, private_watchlist)


def scan_for_secrets():
    risky_files = []

    for path in PUBLIC_REPO_DIR.rglob("*"):
        if path.is_dir():
            continue

        if ".git" in path.parts:
            continue

        if path.suffix.lower() not in {".py", ".yml", ".yaml", ".md", ".json", ".txt", ".example"}:
            continue

        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        for pattern in SECRET_PATTERNS:
            if re.search(pattern, content):
                risky_files.append(str(path.relative_to(PUBLIC_REPO_DIR)))
                break

    if risky_files:
        print("Potential secrets found in public repo:")
        for file_name in risky_files:
            print(f"- {file_name}")

        raise RuntimeError("Public publish stopped because potential secrets were found.")

    print("Secret scan passed.")


def validate_public_repo():
    env_file = PUBLIC_REPO_DIR / ".env"

    if env_file.exists():
        raise RuntimeError(".env should not exist in public repo.")

    watchlist_file = PUBLIC_REPO_DIR / "app" / "watchlist.json"
    sample_watchlist_file = PUBLIC_REPO_DIR / "app" / "watchlist_sample.json"

    if sample_watchlist_file.exists() and not watchlist_file.exists():
        raise RuntimeError("watchlist.json was not generated from watchlist_sample.json.")

    scan_for_secrets()


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
    validate_public_repo()
    commit_and_push()
    print("Public repository updated successfully.")


if __name__ == "__main__":
    main()