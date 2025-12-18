"""
program.py

Point d'entrée principal du programme.
Orchestration complète :
  - parsing de la ligne de commande.
  - validation de la requête utilisateur.
  - parsing du fichier .apx.
  - construction du système d'argumentation.
  - résolution de la requête.

Affiche uniquement YES ou NO sur la sortie standard.
Les erreurs sont affichées sur stderr et pas sur la sortie standard.
"""
import sys
from src.cli import parse_args
from src.apx_parser import parse_apx
from src.systeme_argumentation import AS
from src.queries import solve_query

def parse_and_validate_query(problem: str, raw_a: str):
    """
    Parse et valide l'argument -a en fonction du problème.
    Args:
        - problem: type de problème.
        - raw_a: valeur brute de l'option -a (chaine de caractères).
    Returns:
        - Un ensemble d'arguments (set[str]) pour VE.
        - Un argument unique (str) pour DC / DS.
    Raises: ValueError: si le format de -a est invalide.
    """
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
    """
    Fonction principale du programme.
    """
    try:
        args = parse_args(sys.argv[1:])
        problem = args["probleme"]

        query = parse_and_validate_query(problem, args["arguments"])

        A, R = parse_apx(args["file"])
        systeme_argumentation = AS(A, R)

        res = solve_query(problem, systeme_argumentation, query)
        print("YES" if res else "NO")

    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    """
    Lancement du programme depuis la ligne de commande.
    """
    main()
