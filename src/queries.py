from src.af import AF
import src.semantics as semantics

def solve_query(problem: str, af: AF, query) -> bool:
    match problem:
        case 'VE-PR':
            return ve_pr(af, query)
        
        case 'DC-PR':
            return dc_pr(af, query)
        
        case 'DS-PR':
            return ds_pr(af, query)
        
        case 'VE-ST':
            return ve_st(af, query)
        
        case 'DC-ST':
            return dc_st(af, query)
        
        case 'DS-ST':
            return ds_st(af, query)
        
        case _:
            raise ValueError(f"Problème inconnu: {problem}")


# --- Preferred semantics (PR) ---

def ve_pr(af: AF, S: set[str]) -> bool:
    return S in semantics.preferred_extensions(af)

def dc_pr(af: AF, a: str) -> bool:
    find = False
    for S in semantics.preferred_extensions(af):
        if a in S:
            find = True
            break
    return find

def ds_pr(af: AF, a: str) -> bool:
    exts = semantics.preferred_extensions(af)
    if not exts:
        return True
    for S in exts:
        if a not in S:
            return False
    return True

# # --- Stable semantics (ST) ---

def ve_st(af: AF, S: set[str]) -> bool:
    return S in semantics.stable_extensions(af)

def dc_st(af: AF, a: str) -> bool:
    find = False
    for S in semantics.stable_extensions(af):
        if a in S:
            find = True
            break
    return find

def ds_st(af: AF, a: str) -> bool:
    exts = semantics.stable_extensions(af)
    if not exts:
        return True
    for S in exts:
        if a not in S:
            return False
    return True