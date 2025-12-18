from src.systeme_argumentation import AS
import src.semantics as semantics

def solve_query(problem: str, systeme_argumentation: AS, query) -> bool:
    match problem:
        case 'VE-PR':
            return ve_pr(systeme_argumentation, query)
        
        case 'DC-PR':
            return dc_pr(systeme_argumentation, query)
        
        case 'DS-PR':
            return ds_pr(systeme_argumentation, query)
        
        case 'VE-ST':
            return ve_st(systeme_argumentation, query)
        
        case 'DC-ST':
            return dc_st(systeme_argumentation, query)
        
        case 'DS-ST':
            return ds_st(systeme_argumentation, query)
        
        case _:
            raise ValueError(f"Problème inconnu: {problem}")


# --- Preferred semantics (PR) ---

def ve_pr(systeme_argumentation: AS, S: set[str]) -> bool:
    return S in semantics.preferred_extensions(systeme_argumentation)

def dc_pr(systeme_argumentation: AS, a: str) -> bool:
    return any(a in S for S in semantics.preferred_extensions(systeme_argumentation))

def ds_pr(systeme_argumentation: AS, a: str) -> bool:
    exts = semantics.preferred_extensions(systeme_argumentation)
    return (not exts) or all(a in S for S in exts)

# --- Stable semantics (ST) ---

def ve_st(systeme_argumentation: AS, S: set[str]) -> bool:
    return S in semantics.stable_extensions(systeme_argumentation)

def dc_st(systeme_argumentation: AS, a: str) -> bool:
    return any(a in S for S in semantics.stable_extensions(systeme_argumentation))

def ds_st(systeme_argumentation: AS, a: str) -> bool:
    exts = semantics.stable_extensions(systeme_argumentation)
    return (not exts) or all(a in S for S in exts)
