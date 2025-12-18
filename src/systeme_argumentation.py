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
        self.A = A
        self.R = R
    
    def attackers_of(self, a: str) -> set[str]:
        """
        Donne les attaquants de a.
        Args:
            - a: argument cible.
        Returns: L'ensemble contenant tous les attaquant de a.
        Raises: ValueError: si a n'est pas dans A.
        """
        if a not in self.A:
            raise ValueError(f"L'argument {a} n'est pas dans les arguments.")
        attackers = set()
        for r in self.R:
            if(r[1] == a):
                attackers.add(r[0])
        return attackers
    
    def attacks(self, a: str) -> set[str]:
        """
        Donne les arguments attaqués par a.
        Args:
            - a: argument attaquant.
        Returns: l'ensemble contenant tous les arguments attaqués par a.
        Raises: ValueError: si a n'est pas dans A.
        """
        if a not in self.A:
            raise ValueError(f"L'argument {a} n'est pas dans les arguments.")
        attacks = set()
        for r in self.R:
            if(r[0] == a):
                attacks.add(r[1])
        return attacks
