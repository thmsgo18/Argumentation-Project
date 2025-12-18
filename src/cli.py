"""
src/cli.py

Gestion de la ligne de commande.
Lecture et validation syntaxique des options :
    - -p : type de problème.
    - -f : chemin du fichier .apx.
    - -a : arguments de la requête.
"""
import argparse

def parse_args(argv):
    """
    Parse les arguments de la ligne de commande.
    Args:
        - argv: liste des arguments de la ligne de commande (sans le nom du programme).
    Returns: Dictionnaire contenant :
        - "probleme": type de problème (ex: VE-PR, DC-ST).
        - "file": chemin du fichier .apx.
        - "arguments": arguments de la requête sous forme de chaîne.
    """
    parser = argparse.ArgumentParser()              # Séparation des arguments de ligne de commande.
    parser.add_argument("-p", required= True, choices=['VE-PR', 'DC-PR', 'DS-PR', 'VE-ST', 'DC-ST', 'DS-ST']) # Récupération du nom du problème. (On vérifie que l'on gère ce problème.)
    parser.add_argument("-f", required= True)       # Récupération du nom du fichier .apx.
    parser.add_argument("-a", required= True)       # Récupération de(s) argument(s).

    args = parser.parse_args(argv)

    return {
        "probleme" : args.p,
        "file" : args.f,
        "arguments" : args.a
    }   # On retourne un dictionnaire avec les infos dont on à besoin.
