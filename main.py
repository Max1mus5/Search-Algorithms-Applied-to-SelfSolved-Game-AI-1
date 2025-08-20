
import importlib.util
import os
import sys

def main():
    n8_path = os.path.join(os.path.dirname(__file__), 'Problems', 'N-8-Problem.py')
    spec = importlib.util.spec_from_file_location("n8_mod", n8_path)
    n8_mod = importlib.util.module_from_spec(spec)
    sys.modules["n8_mod"] = n8_mod
    spec.loader.exec_module(n8_mod)

if __name__ == "__main__":
    main()