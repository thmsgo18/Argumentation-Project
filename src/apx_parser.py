"""
src/parse_apx.py

Parsing des fichiers .apx décrivant une AS.
Lecture des arguments et des attaques.
"""
def parse_apx(path: str) -> tuple[set[str], set[tuple[str, str]]]:
    """
    Parse un fichier .apx et construit la AS.
    Args:
        - path: chemin du fichier .apx.
    Returns:
        - A: ensemble des arguments (set[str]).
        - R: ensemble des attaques (set[(str, str)]).
    Raises: ValueError: si une attaque utilise un argument non déclaré.
    """
    A = set()   # Initialisation de l'ensemble des arguments.
    R = set()   # Initialisation de l'ensemble des relations entre les arguments.
    
    # Ouverture du fichier .apx :
    with open(path, 'r', encoding= 'utf-8') as fichier:
        for ligne in fichier:       # Lecture ligne par lignes.
            ligne = ligne.strip()   # Enlève les espaces et les retours à la ligne s'il y'en a. (Ca n'est pas obligatoire mais si jamais.)
            if ligne.startswith("arg("):        # Si la ligne définie un argument.
                A.add(ligne[4:-2].lower())  # On ajout le nom de l'argument (en minuscule) à l'ensemble des arguments.
            elif ligne.startswith("att("):      # Si la ligne définie une relation entre deux arguments.
                args = ligne[4:-2]
                args = args.split(',')      # Séparation des deux arguments en relation.
                x = args[0].lower()     # x = attaquant.
                y = args[1].lower()     # y = attaqué.
                if x not in A or y not in A:    # Vérification que les arguments x et y sont bien dans l'ensemble des arguments.
                    raise ValueError(f"Error: Argument utilisé dans une attaque avant d’être déclaré.")
                else :      # Si pas les arguments sont bien dans l'ensemble.
                    R.add((x, y))   # Ajout de la relation dans l'ensemble des relations.
    return A, R
