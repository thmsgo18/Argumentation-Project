"""
src/semantics.py

Implémente les sémantiques pour un système d'argumentation.
Fonctions de base :
    - conflit
    - défense
    - admissibilité
    - stabilité
Recherche des extensions :
    - admissibles
    - préférées
    - stables
"""
from src.systeme_argumentation import AS
from itertools import combinations

# ******** Fonctions de base: ********

def is_conflict_free(systeme_argumentation: AS, S: set[str]) -> bool:
    """
    Vérifie si un ensemble est sans conflit.
    Args:
        - systeme_argumentation: système d'argumentation <A, R>.
        - S: ensemble d'arguments.
    Returns:
        - True si S est sans conflit.
        - False sinon.
    Raises: ValueError: si S contient un argument inconnu.
    """
    if not S.issubset(systeme_argumentation.A):
        raise ValueError("S contient un argument inconnu.")
    
    for arg in S:
        attacks = systeme_argumentation.attacks(arg)
        for att in attacks:
            if att in S:
                return False
    return True

def defends(systeme_argumentation: AS, S: set[str], a: str) -> bool:
    """
    Vérifie si S défend l'argument a.
    Args:
        - systeme_argumentation: système d'argumentation <A, R>.
        - S: ensemble d'arguments défenseurs.
        - a: argument à défendre.
    Returns:
        - True si tous les attaquants de a sont contrattaqués par S.
        - False sinon.
    Raises: ValueError: si S ou a contient un argument inconnu.
    """
    if not S.issubset(systeme_argumentation.A):
        raise ValueError("S contient un argument inconnu.")
    if a not in systeme_argumentation.A:
        raise ValueError(f"L'argument {a} n'est pas dans les arguments.")
    
    for x in systeme_argumentation.attackers_of(a):
        find = False
        for y in S:
            if x in systeme_argumentation.attacks(y):
                find = True
                break
        if not find:
            return False
    return True

def is_admissible(systeme_argumentation: AS, S: set[str]) -> bool:
    """
    Vérifie si un ensemble est admissible.
    Args:
        - systeme_argumentation: système d'argumentation <A, R>.
        - S: ensemble d'arguments.
    Returns:
        - True si S est sans conflit et défend tous ses éléments.
        - False sinon.
    """
    if not is_conflict_free(systeme_argumentation, S):
        return False
    for a in S:
        if not defends(systeme_argumentation, S, a):
            return False
    return True

def is_stable(systeme_argumentation: AS, S: set[str]) -> bool:
    """
    Vérifie si un ensemble est stable.
    Args:
        - systeme_argumentation: système d'argumentation <A, R>.
        - S: ensemble d'arguments.
    Returns:
        - True si S est sans conflit et attaque tous les arguments hors de S.
        - False sinon.
    """
    if not is_conflict_free(systeme_argumentation, S):
        return False
    outside = systeme_argumentation.A - S
    attacked_by_S = set()
    for b in S:
        attacked_by_S |= systeme_argumentation.attacks(b)
    return outside.issubset(attacked_by_S)

def all_subsets(A: set[str]) -> list[set[str]]:
    """
    Génère tous les sous-ensembles d'un ensemble d'arguments.
    Args:
        - A: ensemble d'arguments.
    Returns:
        - Liste de tous les sous-ensembles de A.
    """
    res = []
    elements = list(A)
    for k in range(len(elements)+1):
        for combo in combinations(elements, k):
            S = set(combo)
            res.append(S)
    return res

# ******** Recherche des extensions: ********

def admissible_extensions(systeme_argumentation: AS) -> list[set[str]]:
    """
    Donne toutes les extensions admissibles.
    Args:
        - systeme_argumentation: système d'argumentation <A, R>.
    Returns:
        - Liste des ensembles admissibles.
    """
    res = []
    sous_ensembles = all_subsets(systeme_argumentation.A)
    for se in sous_ensembles:
        if is_admissible(systeme_argumentation, se):
            res.append(se)
    return res

def preferred_extensions(systeme_argumentation: AS) -> list[set[str]]:
    """
    Donne les extensions préférées.
    Args:
        - systeme_argumentation: système d'argumentation <A, R>.
    Returns:
        - Liste des extensions admissibles maximales par inclusion.
    """
    res = []
    admissibles = admissible_extensions(systeme_argumentation)
    for i in range(len(admissibles)):
        S = admissibles[i]
        pref = True
        for admi in admissibles:
            if S < admi:
                pref = False
                break
        if pref:
            res.append(S)
    return res

def stable_extensions(systeme_argumentation: AS) -> list[set[str]]:
    """
    Donne les extensions stables.
    Args:
        - systeme_argumentation: système d'argumentation <A, R>.
    Returns:
        - Liste des extensions stables.
    """
    res = []
    sous_ensembles = all_subsets(systeme_argumentation.A)
    for se in sous_ensembles:
        if is_stable(systeme_argumentation, se):
            res.append(se)
    return res
