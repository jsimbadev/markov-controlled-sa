from pathlib import Path
import shutil


def main():
    root = Path(__file__).resolve().parent.parent
    for name in ("_output", ".quarto", "index_files"):
        target = root / name
        if target.is_symlink():
            target.unlink()
        elif target.is_dir():
            shutil.rmtree(target)
    for suffix in ("tex", "aux", "log", "out", "toc", "fls", "fdb_latexmk", "synctex.gz"):
        (root / f"index.{suffix}").unlink(missing_ok=True)
    print("Removed generated output and index intermediates.")


if __name__ == "__main__":
    main()
