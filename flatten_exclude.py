import os
from pathlib import Path
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern

# --- SETTINGS ---
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = BASE_DIR / 'repo_combined_output.txt'

# Common unwanted file extensions
EXCLUDE_EXTENSIONS = {
    '.png', '.jpg', '.jpeg', '.pdf', '.zip', '.mp4', '.mp3',
    '.pyc', '.exe', '.db', '.sqlite3', '.log'
}

#------------Default use case start--------------------

# Common unwanted paths (folders/files)
DEFAULT_EXCLUDES = [
    '.git/',
    '.github/',
    '.venv/',
    'venv/',
    '__pycache__/',
    'node_modules/',
    '.idea/',
    '.vscode/',
]

# Manual exclusions for each run (relative to BASE_DIR)
MANUAL_EXCLUDE = [
    'Code of Conduct.md',
    'CONTRIBUTING.md',
    'LICENSE',
    'pyproject.toml',
    'README.md',
    'repo_combined_output.txt',
    'SECURITY.md',
    'flatten_exclude.py',
    'flatten_include.py',
    '.gitignore',
]

#------------Default use case end--------------------

def load_gitignore(base_dir):
    gitignore_path = base_dir / '.gitignore'
    if not gitignore_path.exists():
        return PathSpec.from_lines(GitWildMatchPattern, [])
    with open(gitignore_path, 'r') as f:
        lines = f.readlines()
    return PathSpec.from_lines(GitWildMatchPattern, lines)

def is_excluded(rel_path_str):
    for pattern in DEFAULT_EXCLUDES + MANUAL_EXCLUDE:
        pattern = pattern.rstrip('/')
        # Match exact or as subfolder anywhere in tree
        if (
            rel_path_str == pattern
            or rel_path_str.startswith(pattern + '/')
            or f"/{pattern}/" in "/" + rel_path_str  # match anywhere in path
        ):
            return True
    return False

def collect_files(base_dir, output_file):
    spec = load_gitignore(base_dir)
    with open(output_file, 'w', encoding='utf-8') as out:
        for path in base_dir.rglob('*'):
            if path.is_dir():
                continue

            rel_path_str = str(path.relative_to(base_dir)).replace('\\', '/')
            ext = path.suffix.lower()

            if (
                spec.match_file(rel_path_str)
                or ext in EXCLUDE_EXTENSIONS
                or is_excluded(rel_path_str)
            ):
                continue

            try:
                with open(path, 'r', encoding='utf-8') as f:
                    out.write(f"\n\n===== {rel_path_str} =====\n")
                    out.write(f.read())
            except Exception as e:
                print(f"Skipped: {rel_path_str} ({e})")

    print(f"\n✅ Done. Combined content written to: {output_file}")

if __name__ == '__main__':
    collect_files(BASE_DIR, OUTPUT_FILE)
