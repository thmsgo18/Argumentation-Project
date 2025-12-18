import sys
from src.cli import parse_args

def main():
    args= parse_args(sys.argv[1:])
    print(args)
    print("Rien pour l'instant")

if __name__ == "__main__":
    main()
