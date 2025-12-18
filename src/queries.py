"""
src/queries.py

Gestion des commandes VE / DC / DS avec les sémantiques :
    - préférée (PR)
    - stable (ST)
"""

from src.systeme_argumentation import AS
import src.semantics as semantics

def solve_query(problem: str, systeme_argumentation: AS, query) -> bool:
    """
    Résout une requête VE / DC / DS selon la sémantique demandée.
    Args:
        - problem: type de problème.
        - systeme_argumentation: système d'argumentation <A, R>.
        - query: ensemble S (pour les VE) ou argument a (pour DC / DS).
    Returns:
        - True si la requête est satisfaite.
        - False sinon.
    Raises: ValueError: si le problème est inconnu.
    """
    match problem:      # Appel de la bonne fonction en fonction du problème renseigné en paramètre.
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
        
        case _:         # Cas d'érreur si jamais.
            raise ValueError(f"Problème inconnu: {problem}")


# --- Preferred semantics (PR) ---

def ve_pr(systeme_argumentation: AS, S: set[str]) -> bool:
    """
    Vérifie que 'S' est une extension préférée.
    Args:
        - systeme_argumentation: système d'argumentation <A, R>.
        - S: ensemble d'arguments.
    Returns:
        - True si S est une extension préférée.
        - False sinon.
    """
    return S in semantics.preferred_extensions(systeme_argumentation) # Teste si S est dans l'ensemble des extensions préférées du système.

def dc_pr(systeme_argumentation: AS, a: str) -> bool:
    """
    Vérifie 'a' appartient à au moins une extension préférée.
    Args:
        - systeme_argumentation: système d'argumentation <A, R>.
        - a: argument à tester.
    Returns:
        - True si a est crédullement accepté.
        - False sinon.
    """
    return any(a in S for S in semantics.preferred_extensions(systeme_argumentation)) # Teste si l'argument 'a' est au moins dans une des extentions préférées.

def ds_pr(systeme_argumentation: AS, a: str) -> bool:
    """
    Vérifie que 'a' appartient à toutes les extensions préférées.
    Args:
        - systeme_argumentation: système d'argumentation <A, R>.
        - a: argument à tester.
    Returns:
        - True si a est sceptiquement accepté.
        - False sinon.
    """
    exts = semantics.preferred_extensions(systeme_argumentation) # Toutes les extensions préférées du système.
    return (not exts) or all(a in S for S in exts) # Teste s'il n'y a pas d'extensions préférées ou si 'a' appartient a toutes les extentions préférées.

# --- Stable semantics (ST) ---

def ve_st(systeme_argumentation: AS, S: set[str]) -> bool:
    """
    Vérifie que 'S' est une extension stable.
    Args:
        - systeme_argumentation: système d'argumentation <A, R>.
        - S: ensemble d'arguments.
    Returns:
        - True si S est une extension stable.
        - False sinon.
    """
    return S in semantics.stable_extensions(systeme_argumentation) #Teste si 'S' est dans l'ensemble des extensions stables.

def dc_st(systeme_argumentation: AS, a: str) -> bool:
    """
    Vérifie que 'a' appartient à au moins une extension stable.
    Args:
        - systeme_argumentation: système d'argumentation <A, R>.
        - a: argument à tester.
    Returns:
        - True si a est crédullement accepté.
        - False sinon.
    """
    return any(a in S for S in semantics.stable_extensions(systeme_argumentation)) # On teste si 'a' appartient à au moins une des extension stable.

def ds_st(systeme_argumentation: AS, a: str) -> bool:
    """
    Vérifie que 'a' appartient à toutes les extensions stables.
    Args:
        - systeme_argumentation: système d'argumentation <A, R>.
        - a: argument à tester.
    Returns:
        - True si a est sceptiquement accepté.
        - False sinon.
    """
    exts = semantics.stable_extensions(systeme_argumentation) # Toutes les extensions stables du système.
    return (not exts) or all(a in S for S in exts) # Teste s'il n'y a pas d'extensions stable ou si 'a' appartient a toutes les extentions stables.
