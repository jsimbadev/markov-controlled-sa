"""Keep Quarto's document preview current when included manuscript inputs change."""

import argparse
import hashlib
from pathlib import Path
import subprocess
import threading


INPUTS = (
    "sections", "figures", "filters", "styles", "tex",
    "_quarto.yml", "macros.tex", "references.bib", "styles.css",
)


def snapshot(root):
    result = {}
    for name in INPUTS:
        path = root / name
        files = path.rglob("*") if path.is_dir() else (path,)
        for file in files:
            try:
                if file.is_file():
                    result[file] = hashlib.sha256(file.read_bytes()).digest()
            except FileNotFoundError:
                # An editor may replace a file between listing and reading it.
                pass
    return result


def watch(root, stopped):
    previous = snapshot(root)
    while not stopped.wait(0.5):
        current = snapshot(root)
        if current != previous:
            # Quarto watches index.qmd but doesn't track its include dependencies.
            # Updating its timestamp triggers a fresh render without changing text.
            (root / "index.qmd").touch()
            previous = current


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quarto", default="quarto")
    arguments, preview_arguments = parser.parse_known_args()
    root = Path(__file__).resolve().parent.parent
    stopped = threading.Event()
    watcher = threading.Thread(target=watch, args=(root, stopped), daemon=True)
    watcher.start()
    try:
        return subprocess.call(
            [arguments.quarto, "preview", "index.qmd", "--to", "html", *preview_arguments],
            cwd=root,
        )
    except KeyboardInterrupt:
        return 130
    finally:
        stopped.set()
        watcher.join()


if __name__ == "__main__":
    raise SystemExit(main())
