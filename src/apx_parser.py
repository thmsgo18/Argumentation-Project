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
    A = set()
    R = set()
    with open(path, 'r', encoding= 'utf-8') as fichier:
        for ligne in fichier:
            ligne = ligne.strip()
            if ligne.startswith("arg("):
                A.add(ligne[4:-2].lower())
            elif ligne.startswith("att("):
                args = ligne[4:-2]
                args = args.split(',')
                x = args[0].lower()
                y = args[1].lower()
                if x not in A or y not in A:
                    raise ValueError(f"Error: Argument utilisé dans une attaque avant d’être déclaré.")
                else :
                    R.add((x, y))
    return A, R
