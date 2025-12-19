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
    raw_a = raw_a.strip().lower()   # Suppression des espaces inutile et mise en minuscule.
    tokens = []                     # Initatialisation de la liste les arguments pour les problèmes VE-.
    if not problem.startswith("VE-"):   # Cas DC / DS où on attend un seul argument.
        if "," in raw_a:                # On teste la présence d'une virgule (c'ets a dire est ce qu'il y'a plusieurs arguments).
            raise ValueError("Error: -a doit contenir un seul argument.")
        if raw_a == "":                 # On teste si la chaine est vide (c'est a dire il n'y a pas d'arguments).
            raise ValueError("Error: -a ne peut pas être vide.")
        return raw_a        # On retourne l'argument.
    for t in raw_a.split(","):  # On itère sur la liste d'arguments qui a été créé en séparant à partir de la virgule.
        t = t.strip()           # Suppression des espaces inutile.
        if t != "":             # On teste si la chaine est vide.
            tokens.append(t)    # Si la chaine n'est pas vide on l'ajoute à la liste des arguments.
    if not tokens:              # Si la liste des arguments est vide on lève une erreur.
        raise ValueError("Error: -a doit contenir au moins un argument.")
    return set(tokens) # On retourne le(s) argument(s) sous forme d'ensemble.

def main():
    """
    Fonction principale du programme.
    """
    try: # Bloc permettant de géré les erreurs pouvant etre provoquée par les fonctions à l'intérieur.
        args = parse_args(sys.argv[1:]) # Récupération des paramètres passés en ligne de commande.
        problem = args["probleme"]      # Récupération du problème voulant etre traité.

        query = parse_and_validate_query(problem, args["arguments"]) # Récupération des arguments à 

        A, R = parse_apx(args["file"])      # Récupération des attributs et des relations à partir du fichier.
        systeme_argumentation = AS(A, R)    # Création du système d'argumentation à partir du fichier renseigné.

        res = solve_query(problem, systeme_argumentation, query) # Résolution du problème voulu avec les arguments voulu pour le système d'argumentation voulu.
        print("YES" if res else "NO")   # Affiche YES ou NO en fonction du résultat de la résolution du problème.

    except Exception as e:              # En cas d'erreur, le programme affiche l'erreur sur la sortir d'erreur et pas sur la sortie standard.
        print(str(e), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    """
    Lancement du programme depuis la ligne de commande.
    """
    main()
