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
    if not S.issubset(systeme_argumentation.A): # Vérification que l'ensemble S est un sous ensemble de l'ensemble des arguments de l'AS.
        raise ValueError("S contient un argument inconnu.")
    
    for arg in S:   # On boucle sur tout les arguments de l'ensemble S.
        attacks = systeme_argumentation.attacks(arg)    # Ensemble des arguments attaqué par l'argument sur lequel on boucle.
        for att in attacks:     # On itére sur les arguments attaqués.
            if att in S:        # On teste leur présence dans l'ensemble S.
                return False        # Si un argument de S est attaqué par un autre argument de S on retourne False.
    return True     # Si aucuns des arguments de S ne s'attaque.

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
    if not S.issubset(systeme_argumentation.A):     # Vérification que l'ensemble S est un sous ensemble de l'ensemble des arguments de l'AS.
        raise ValueError("S contient un argument inconnu.")
    if a not in systeme_argumentation.A:            # Vérification que l'argument a est présent dans l'ensemble des arguments de l'AS.
        raise ValueError(f"L'argument {a} n'est pas dans les arguments.")
    
    for x in systeme_argumentation.attackers_of(a): # On boucle sur les attaquant de l'argument a. x représente donc un attaquant de a.
        find = False
        for y in S: # On boucle sur les arguments de l'ensemble S.
            if x in systeme_argumentation.attacks(y): # Si y attaque x.
                find = True # On indique que un élément de Y défend bien a. (a <-- x <-- y)
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
    if not is_conflict_free(systeme_argumentation, S):      # Vérification que l'ensemble S est sans conflit.
        return False        # S'il n'est pas sans conflit on retourne False.
    for a in S:             # On itére sur tous les arguments de a.
        if not defends(systeme_argumentation, S, a): # Si a n'est pas défendu par l'ensemble S. 
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
    if not is_conflict_free(systeme_argumentation, S):      # Vérification que l'ensemble S est sans conflit.
        return False
    outside = systeme_argumentation.A - S       # On cherche tous les arguments non compris dans l'ensemble S.
    attacked_by_S = set()       # Initialisation de l'ensemble des arguments qui sont attaqués par un argument de l'ensemble S.
    for b in S:                 # b est un argument de S.
        attacked_by_S |= systeme_argumentation.attacks(b)   # Union de attacked_by_S et des arguments attaqué par b.
    return outside.issubset(attacked_by_S)      # On teste si outside est un sous ensemble de l'ensembles des attacked_by_S.

def all_subsets(A: set[str]) -> list[set[str]]:
    """
    Génère tous les sous-ensembles d'un ensemble d'arguments.
    Args:
        - A: ensemble d'arguments.
    Returns:
        - Liste de tous les sous-ensembles de A.
    """
    res = []                # Initialisation de la liste des sous ensembles.
    elements = list(A)      # Transformation de l'ensemble A en liste.
    for k in range(len(elements)+1):
        for combo in combinations(elements, k): # Itération sur les combinaisons compossible de l'ensemble A de taille k.
            S = set(combo)      # Transformation de la combinaison en ensemble.
            res.append(S)       # Ajout de la combinaison à la liste des sous ensemble.
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
    res = []                # Initialisation de la liste des extensions admissibles.
    sous_ensembles = all_subsets(systeme_argumentation.A) # Liste des sous ensembles de l'AS.
    for se in sous_ensembles:                           # On boucle sur chaque sous ensembles.
        if is_admissible(systeme_argumentation, se):    # On teste si le sous ensemble est admissible.
            res.append(se)                              # Si tel est le cas on le rajoute à la liste des extensions admissibles.
    return res

def preferred_extensions(systeme_argumentation: AS) -> list[set[str]]:
    """
    Donne les extensions préférées.
    Args:
        - systeme_argumentation: système d'argumentation <A, R>.
    Returns:
        - Liste des extensions admissibles maximales par inclusion.
    """
    res = []                # Initialisation de la liste des extensions préférées.
    admissibles = admissible_extensions(systeme_argumentation) # Liste des extentions admissibles de l'AS.
    for i in range(len(admissibles)): # Parcourt chaque extension admissible.
        S = admissibles[i]  # S = extension admissible courante sur laquelle on itère.
        pref = True                 # On pose S est préferré.
        for admi in admissibles:    # On boucle sur les admissibles.
            if S < admi:            # Si S est inclu dans l'admissible sur lequel on itére on sort de la boucle.
                pref = False
                break
        if pref:    # Si pref est encore a True (cest a dire qu'on a pas trouvé d'expression plus inclue S)
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
    res = []                # Initialisation de la liste des extensions stables.
    sous_ensembles = all_subsets(systeme_argumentation.A) # Liste des sous ensembles de l'AS.
    for se in sous_ensembles:                           # On boucle sur chaque sous ensembles.
        if is_stable(systeme_argumentation, se):        # On teste si le sous ensemble est stable.
            res.append(se)                              # Si tel est le cas on le rajoute à la liste des extensions admissibles.
    return res
