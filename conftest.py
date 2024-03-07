import sys
from pathlib import Path

cli_path = Path(__file__).parent / "cli"

sys.path.insert(0, str(cli_path))
