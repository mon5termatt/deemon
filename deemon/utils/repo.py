import logging
import re
import subprocess
from functools import lru_cache
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

DEFAULT_GITHUB_REPO = "mon5termatt/deemon"


def _parse_github_remote(url: str) -> Optional[str]:
    url = url.strip().rstrip("/")
    if url.endswith(".git"):
        url = url[:-4]

    ssh_match = re.match(r"^git@github\.com:(?P<repo>[^/]+/[^/]+)$", url)
    if ssh_match:
        return ssh_match.group("repo")

    parsed = urlparse(url)
    if parsed.netloc.lower() in {"github.com", "www.github.com"}:
        parts = [part for part in parsed.path.strip("/").split("/") if part]
        if len(parts) >= 2:
            return f"{parts[0]}/{parts[1]}"

    return None


def _git_repo_root() -> Optional[Path]:
    candidates = [
        Path(__file__).resolve().parents[2],
        Path.cwd(),
    ]

    for candidate in candidates:
        if (candidate / ".git").exists():
            return candidate

    return None


@lru_cache(maxsize=1)
def get_github_repo() -> str:
    repo_root = _git_repo_root()
    if not repo_root:
        return DEFAULT_GITHUB_REPO

    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as e:
        logger.debug(f"Unable to read git remote origin: {e}")
        return DEFAULT_GITHUB_REPO

    if result.returncode != 0:
        logger.debug(f"git remote get-url origin failed: {result.stderr.strip()}")
        return DEFAULT_GITHUB_REPO

    slug = _parse_github_remote(result.stdout)
    return slug or DEFAULT_GITHUB_REPO


def get_github_repo_url() -> str:
    return f"https://github.com/{get_github_repo()}"


def get_github_releases_url() -> str:
    return f"{get_github_repo_url()}/releases"


def get_github_api_repo_url() -> str:
    return f"https://api.github.com/repos/{get_github_repo()}"
