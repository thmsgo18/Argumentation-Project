import sys
from src.cli import parse_args
from src.apx_parser import parse_apx
from src.af import AF
from src.queries import solve_query

def main():
    try :
        args= parse_args(sys.argv[1:])
        problem = args["probleme"]
        raw_a = args["arguments"].strip().lower()

        if not problem.startswith("VE-") and "," in raw_a:
            raise ValueError("Error: -a doit contenir un seul argument.")
        if not problem.startswith("VE-") and raw_a == "":
            raise ValueError("Error: -a ne peut pas être vide.")

        if problem.startswith("VE-"):
            tokens = []
            for t in raw_a.split(","):
                t = t.strip().lower()
                if t != "":
                    tokens.append(t)
            if len(tokens) == 0:
                raise ValueError("Error: -a doit contenir au moins un argument.")

        A, R = parse_apx(args["file"])
        af = AF(A, R)
        if args["probleme"].startswith("VE-") :
            query = set(tokens)
        else:
            query = raw_a
        
        res = solve_query(args["probleme"], af, query)
        if res :
            print("YES")
        else:
            print("NO")

    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
