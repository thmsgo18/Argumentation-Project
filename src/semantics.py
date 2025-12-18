from src.systeme_argumentation import AS
from itertools import combinations

def is_conflict_free(systeme_argumentation: AS, S: set[str]) -> bool:
    if not S.issubset(systeme_argumentation.A):
        raise ValueError("S contient un argument inconnu.")
    
    for arg in S:
        attacks = systeme_argumentation.attacks(arg)
        for att in attacks:
            if att in S:
                return False
    return True

def defends(systeme_argumentation: AS, S: set[str], a: str) -> bool:
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
    if not is_conflict_free(systeme_argumentation, S):
        return False
    for a in S:
        if not defends(systeme_argumentation, S, a):
            return False
    return True

def is_stable(systeme_argumentation: AS, S: set[str]) -> bool:
    if not is_conflict_free(systeme_argumentation, S):
        return False
    outside = systeme_argumentation.A - S
    attacked_by_S = set()
    for b in S:
        attacked_by_S |= systeme_argumentation.attacks(b)
    return outside.issubset(attacked_by_S)

def all_subsets(A: set[str]) -> list[set[str]]:
    res = []
    elements = list(A)
    for k in range(len(elements)+1):
        for combo in combinations(elements, k):
            S = set(combo)
            res.append(S)
    return res


def admissible_extensions(systeme_argumentation: AS) -> list[set[str]]:
    res = []
    sous_ensembles = all_subsets(systeme_argumentation.A)
    for se in sous_ensembles:
        if is_admissible(systeme_argumentation, se):
            res.append(se)
    return res

def preferred_extensions(systeme_argumentation: AS) -> list[set[str]]:
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
    res = []
    sous_ensembles = all_subsets(systeme_argumentation.A)
    for se in sous_ensembles:
        if is_stable(systeme_argumentation, se):
            res.append(se)
    return res
