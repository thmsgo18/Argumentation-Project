import sys
from src.cli import parse_args
from src.apx_parser import parse_apx
from src.af import AF
from src.queries import solve_query

def parse_and_validate_query(problem: str, raw_a: str):
    raw_a = raw_a.strip().lower()
    tokens = []
    if not problem.startswith("VE-"):
        if "," in raw_a:
            raise ValueError("Error: -a doit contenir un seul argument.")
        if raw_a == "":
            raise ValueError("Error: -a ne peut pas être vide.")
        return raw_a
    for t in raw_a.split(","):
        t = t.strip()
        if t != "":
            tokens.append(t)
    if not tokens:
        raise ValueError("Error: -a doit contenir au moins un argument.")
    return set(tokens)

def main():
    try:
        args = parse_args(sys.argv[1:])
        problem = args["probleme"]

        query = parse_and_validate_query(problem, args["arguments"])

        A, R = parse_apx(args["file"])
        af = AF(A, R)

        res = solve_query(problem, af, query)
        print("YES" if res else "NO")

    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
