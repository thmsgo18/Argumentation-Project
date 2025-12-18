"""
src/systeme_argumentation.py

- Représentation d'un système d’argumentation (AS) avec : <A, R>
- A : ensemble d'arguments (set[str])
- R : relation d'attaque (set[tuple[str, str]]) avec (attaquant, attaqué)
- Fournit des fonctions utilitaires :
  - attackers_of(a) : qui attaque a
  - attacks(a)      : qui est attaqué par a
"""
class AS:
    def __init__(self, A: set[str], R:set[tuple[str, str]]):
        self.A = A
        self.R = R
    
    def attackers_of(self, a: str) -> set[str]:
        if a not in self.A:
            raise ValueError(f"L'argument {a} n'est pas dans les arguments.")
        attackers = set()
        for r in self.R:
            if(r[1] == a):
                attackers.add(r[0])
        return attackers
    
    def attacks(self, a: str) -> set[str]:
        if a not in self.A:
            raise ValueError(f"L'argument {a} n'est pas dans les arguments.")
        attacks = set()
        for r in self.R:
            if(r[0] == a):
                attacks.add(r[1])
        return attacks
