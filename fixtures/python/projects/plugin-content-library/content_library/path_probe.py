"""Helper to print sys.path[0] for launcher demo (PY-CAN-MOD-016)."""

import sys, json
print(json.dumps(sys.path[0]))
