def parse_apx(path: str) -> tuple[set[str], set[tuple[str, str]]]:
    A = set()
    R = set()
    with open(path, 'r', encoding= 'utf-8') as fichier:
        for ligne in fichier:
            ligne = ligne.strip()
            if ligne.startswith("arg("):
                A.add(ligne[4:-2])
            elif ligne.startswith("att("):
                args = ligne[4:-2]
                args = args.split(',')
                x = args[0]
                y = args[1]
                if x not in A or y not in A:
                    raise ValueError(f"Error: Argument utilisé dans une attaque avant d’être déclaré.")
                else :
                    R.add((x, y))
    return A, R

