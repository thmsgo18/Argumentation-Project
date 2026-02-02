# Solveur de Systèmes d'Argumentation

> Projet de Master IAD - Représentation des Connaissances et Raisonnement  
> Année universitaire 2025-2026

**Français** | **[English](README.md)**

## Présentation

Ce projet implémente un solveur pour systèmes d'argumentation (AS). Il permet de calculer et vérifier différents types d'extensions selon les sémantiques préférées (PR) et stables (ST).

Un système d'argumentation est défini par **F = ⟨A, R⟩** où :
- **A** est un ensemble d'arguments abstraits
- **R ⊆ A × A** est la relation d'attaque entre arguments

## Problèmes Supportés

Le programme résout les 6 problèmes suivants :

| Problème | Sémantique | Description |
|----------|------------|-------------|
| **VE-PR** | Préférée | Vérifier si S est une extension préférée |
| **DC-PR** | Préférée | Acceptabilité crédule d'un argument |
| **DS-PR** | Préférée | Acceptabilité sceptique d'un argument |
| **VE-ST** | Stable | Vérifier si S est une extension stable |
| **DC-ST** | Stable | Acceptabilité crédule d'un argument |
| **DS-ST** | Stable | Acceptabilité sceptique d'un argument |

## Installation

### Prérequis

- Python 3.8 ou supérieur
- Aucune dépendance externe nécessaire (bibliothèque standard uniquement)

### Vérification de l'Installation

```bash
python3 --version
```

## Utilisation

### Syntaxe Générale

```bash
python3 program.py -p <PROBLEME> -f <FICHIER> -a <ARGUMENTS>
```

### Paramètres

- **-p** : Type de problème (`VE-PR`, `DC-PR`, `DS-PR`, `VE-ST`, `DC-ST`, `DS-ST`)
- **-f** : Chemin vers le fichier `.apx` contenant le système d'argumentation
- **-a** : Arguments de la requête
  - Pour les problèmes VE-* : liste séparée par des virgules (ex: `a,c,d`)
  - Pour les problèmes DC-* et DS-* : un seul argument (ex: `b`)

### Exemples d'Utilisation

En supposant que `af.txt` contient un AF avec A = {a,b,c,d} et R = {(a,b), (b,c), (b,d)} :

```bash
# Vérifier si {a,c,d} est une extension préférée
python3 program.py -p VE-PR -f af.txt -a a,c,d
# Sortie: YES

# Vérifier l'acceptabilité crédule de 'b' (sémantique préférée)
python3 program.py -p DC-PR -f af.txt -a b
# Sortie: NO

# Vérifier l'acceptabilité sceptique de 'a' (sémantique préférée)
python3 program.py -p DS-PR -f af.txt -a a
# Sortie: YES

# Vérifier si {a,c,d} est une extension stable
python3 program.py -p VE-ST -f af.txt -a a,c,d
# Sortie: YES
```

## Structure du Projet

```
Argumentation-Project/
├── README.md                # Documentation anglaise
├── README.fr.md             # Documentation française
├── program.py               # Point d'entrée principal
├── src/
│   ├── __init__.py
│   ├── cli.py              # Gestion des arguments en ligne de commande
│   ├── apx_parser.py       # Parser pour fichiers .apx
│   ├── systeme_argumentation.py  # Classe du système d'argumentation
│   ├── semantics.py        # Algorithmes pour les sémantiques
│   └── queries.py          # Résolution des requêtes
└── Fichiers-tests/         # Fichiers de test
    ├── test_af1.apx
    ├── test_af1_pr.txt
    ├── test_af1_st.txt
    └── ...
```

## Format du Fichier APX

Les fichiers `.apx` suivent le format suivant :

```
arg(nom_argument).
att(argument_source,argument_cible).
```

### Règles du Format

- Chaque argument doit être déclaré avec `arg()` avant d'être utilisé dans une attaque
- Pas d'espaces dans les lignes
- Les noms peuvent contenir lettres, chiffres et `_` (sauf `arg` et `att` qui sont réservés)

### Exemple

```
arg(a).
arg(b).
arg(c).
arg(d).
att(a,b).
att(b,c).
att(b,d).
```

Cet exemple représente le graphe suivant :
```
a → b → c
    ↓
    d
```

## Exécution des Tests

Le dossier `Fichiers-tests/` contient plusieurs cas de test :

```bash
# Tester avec les fichiers fournis
python3 program.py -p VE-PR -f Fichiers-tests/test_af1.apx -a a,c,d
python3 program.py -p DC-ST -f Fichiers-tests/test_af2.apx -a b
```

## Détails d'Implémentation

### Extensions Préférées

Le solveur utilise un algorithme de backtracking pour calculer tous les ensembles sans conflit et admissibles, puis identifie les ensembles admissibles maximaux (extensions préférées).

### Extensions Stables

Une extension stable est calculée en trouvant des ensembles sans conflit qui attaquent tous les arguments en dehors de l'ensemble.

### Résolution des Requêtes

- **VE (Vérification)** : Vérifie si l'ensemble donné est une extension sous la sémantique spécifiée
- **DC (Crédule)** : Retourne YES si l'argument apparaît dans au moins une extension
- **DS (Sceptique)** : Retourne YES si l'argument apparaît dans toutes les extensions

## Auteur

[@thmsgo18](https://github.com/thmsgo18) - Thomas Gourmelen

## Licence

Ce projet fait partie du cursus académique du Master IAD.
