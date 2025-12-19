"""
src/systeme_argumentation.py

Représentation d'un système d’argumentation (AS) avec : <A, R>
    - A : ensemble d'arguments (set[str]).
    - R : relation d'attaque (set[tuple[str, str]]) avec (attaquant, attaqué).
    Avec Les fonctions:
        - attackers_of(a): qui attaque a.
        - attacks(a): qui est attaqué par a.
"""
class AS:
    def __init__(self, A: set[str], R:set[tuple[str, str]]):
        """
        Initialise un AF.
        Args:
            - A: ensemble des arguments.
            - R: ensemble des attaques (x, y) avec x attaque y.
        Returns: None
        """
        self.A = A      # Initialisation de l'ensemble des arguments.
        self.R = R      # Initialisation de l'ensemble des attaques.
    
    def attackers_of(self, a: str) -> set[str]:
        """
        Donne les attaquants de a.
        Args:
            - a: argument cible.
        Returns: L'ensemble contenant tous les attaquant de a.
        Raises: ValueError: si a n'est pas dans A.
        """
        if a not in self.A:         # Verification de si l'argument a appartient à l'ensemble des arguments du système.
            raise ValueError(f"L'argument {a} n'est pas dans les arguments.")
        attackers = set()       # Initialisation de l'ensemble des attaquant de 'a'.
        for r in self.R:        # On itére sur chaque relation dans l'ensemble des relations du système.
            if(r[1] == a):      # On regarde si la relation porte sur 'a' qui se fait attaquer.
                attackers.add(r[0])     # Si c'est le cas on ajoute l'attaquant à la liste des attaquant de 'a'.
        return attackers # On retourne la liste des attaquant.
    
    def attacks(self, a: str) -> set[str]:
        """
        Donne les arguments attaqués par a.
        Args:
            - a: argument attaquant.
        Returns: l'ensemble contenant tous les arguments attaqués par a.
        Raises: ValueError: si a n'est pas dans A.
        """
        if a not in self.A:         # Verification de si l'argument a appartient à l'ensemble des arguments du système.
            raise ValueError(f"L'argument {a} n'est pas dans les arguments.")
        attacks = set()         # Initialisation de l'ensemble des attaqué par 'a'.
        for r in self.R:        # On itére sur chaque relation dans l'ensemble des relations du système.
            if(r[0] == a):      # On regarde si la relation porte sur 'a' qui attaque.
                attacks.add(r[1])       # Si c'est le cas on ajoute l'attaqué à la liste des attaqué par 'a'.
        return attacks # On retourne la liste des attaqué.
