"""Install packages exactly as the lab notebooks do, using their `! pip install ...` cells.

CI runs this in a clean environment (no requirements.txt) and then runs the smoke tests,
so what CI checks is what a student gets by running the notebook top to bottom.
"""
import re
import shlex
import subprocess
import sys
from pathlib import Path

import nbformat

ROOT = Path(__file__).resolve().parents[1]
PIP_LINE = re.compile(r"^\s*[!%]\s*pip install\s+(.+)$")


def notebook_installs():
    args = []
    for path in sorted(ROOT.rglob("*.ipynb")):
        if "env" in path.parts:
            continue
        for cell in nbformat.read(path, as_version=4).cells:
            if cell.cell_type != "code":
                continue
            for line in cell.source.splitlines():
                match = PIP_LINE.match(line)
                if match:
                    args += [a for a in shlex.split(match.group(1), comments=True) if not a.startswith("-")]
    return list(dict.fromkeys(args))  # de-duplicate, keep order


if __name__ == "__main__":
    packages = notebook_installs()
    print("Installing as the notebooks do:", " ".join(packages), flush=True)
    sys.exit(subprocess.call([sys.executable, "-m", "pip", "install", *packages]))
