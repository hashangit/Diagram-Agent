import sys

print("This is a test output.")
print("Error message", file=sys.stderr)

# Attempt to flush the output
sys.stdout.flush()
sys.stderr.flush()