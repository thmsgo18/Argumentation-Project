from src.af import AF
from itertools import combinations

def is_conflict_free(af: AF, S: set[str]) -> bool:
    if not S.issubset(af.A):
        raise ValueError("S contient un argument inconnu.")
    
    for arg in S:
        attacks = af.attacks(arg)
        for att in attacks:
            if att in S:
                return False
    return True

def defends(af: AF, S: set[str], a: str) -> bool:
    if not S.issubset(af.A):
        raise ValueError("S contient un argument inconnu.")
    if a not in af.A:
        raise ValueError(f"L'argument {a} n'est pas dans les arguments.")
    
    for x in af.attackers_of(a):
        find = False
        for y in S:
            if x in af.attacks(y):
                find = True
                break
        if not find:
            return False
    return True

def is_admissible(af: AF, S: set[str]) -> bool:
    if not is_conflict_free(af, S):
        return False
    for a in S:
        if not defends(af, S, a):
            return False
    return True

def is_stable(af: AF, S: set[str]) -> bool:
    if not is_conflict_free(af, S):
        return False
    outside = af.A - S
    attacked_by_S = set()
    for b in S:
        attacked_by_S |= af.attacks(b)
    return outside.issubset(attacked_by_S)

def all_subsets(A: set[str]) -> list[set[str]]:
    res = []
    elements = list(A)
    for k in range(len(elements)+1):
        for combo in combinations(elements, k):
            S = set(combo)
            res.append(S)
    return res


def admissible_extensions(af: AF) -> list[set[str]]:
    res = []
    sous_ensembles = all_subsets(af.A)
    for se in sous_ensembles:
        if is_admissible(af, se):
            res.append(se)
    return res

def preferred_extensions(af: AF) -> list[set[str]]:
    res = []
    admissibles = admissible_extensions(af)
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

def stable_extensions(af: AF) -> list[set[str]]:
    res = []
    sous_ensembles = all_subsets(af.A)
    for se in sous_ensembles:
        if is_stable(af, se):
            res.append(se)
    return res



