# 🎯 Projet Argumentation Abstraite

> Projet de Master IAD - Représentation des Connaissances et Raisonnement  
> Année universitaire 2025-2026

## 📋 Description

Ce projet implémente un solveur pour systèmes d'argumentation abstraite (Abstract Argumentation Framework). Il permet de calculer et vérifier différents types d'extensions selon les sémantiques préférées (PR) et stables (ST).

Un système d'argumentation est défini par **F = ⟨A, R⟩** où :
- **A** est un ensemble d'arguments abstraits
- **R ⊆ A × A** est la relation d'attaque entre arguments

### Problèmes résolus

Le programme résout les 6 problèmes suivants :

| Type | Sémantique | Description |
|------|-----------|-------------|
| **VE-PR** | Préférée | Vérifier si S est une extension préférée |
| **DC-PR** | Préférée | Acceptabilité crédule d'un argument |
| **DS-PR** | Préférée | Acceptabilité sceptique d'un argument |
| **VE-ST** | Stable | Vérifier si S est une extension stable |
| **DC-ST** | Stable | Acceptabilité crédule d'un argument |
| **DS-ST** | Stable | Acceptabilité sceptique d'un argument |

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- Aucune dépendance externe nécessaire (bibliothèque standard uniquement)

### Vérification de l'installation

```bash
python3 --version
```

## 💻 Utilisation

### Syntaxe générale

```bash
python3 programme.py -p <PROBLEME> -f <FICHIER> -a <ARGUMENTS>
```

### Paramètres

- **-p** : Type de problème (`VE-PR`, `DC-PR`, `DS-PR`, `VE-ST`, `DC-ST`, `DS-ST`)
- **-f** : Chemin vers le fichier `.apx` contenant l'AF
- **-a** : Arguments de la requête
  - Pour VE-* : liste séparée par des virgules (ex: `a,c,d`)
  - Pour DC-* et DS-* : un seul argument (ex: `b`)

### Exemples d'utilisation

En supposant que `af.txt` contient l'AF avec A = {a,b,c,d} et R = {(a,b), (b,c), (b,d)} :

```bash
# Vérifier si {a,c,d} est une extension préférée
python3 programme.py -p VE-PR -f af.txt -a a,c,d
# Sortie: YES

# Vérifier l'acceptabilité crédule de 'b' (préférée)
python3 programme.py -p DC-PR -f af.txt -a b
# Sortie: NO

# Vérifier l'acceptabilité sceptique de 'a' (préférée)
python3 programme.py -p DS-PR -f af.txt -a a
# Sortie: YES

# Vérifier si {a,c,d} est une extension stable
python3 programme.py -p VE-ST -f af.txt -a a,c,d
# Sortie: YES
```

## 📁 Structure du projet

```
Projet-RCR/
├── README.md                    # Ce fichier
├── programme.py                 # Point d'entrée principal
├── af.txt                       # Exemple de fichier AF
├── src/
│   ├── __init__.py
│   ├── cli.py                   # Gestion des arguments en ligne de commande
│   ├── apx_parser.py            # Parser pour fichiers .apx
│   ├── af.py                    # Classe AF (Argumentation Framework)
│   ├── semantics.py             # Algorithmes pour les sémantiques
│   └── queries.py               # Résolution des requêtes
├── Fichiers-tests/              # Fichiers de test fournis
│   ├── test_af1.apx
│   ├── test_af1_pr.txt
│   ├── test_af1_st.txt
│   └── ...
└── tests/                       # Tests unitaires (à compléter)
    └── __init__.py
```

## 📝 Format du fichier .apx

Les fichiers `.apx` suivent le format suivant :

```
arg(nom_argument).
att(argument_source,argument_cible).
```

### Règles

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

Cet exemple représente le graphe :
```
a → b → c
    ↓
    d
```

## 🧮 Algorithmes implémentés

### Sémantique préférée

1. Génération de tous les sous-ensembles de A
2. Filtrage des ensembles sans conflit
3. Filtrage des ensembles admissibles (qui se défendent)
4. Sélection des ensembles maximaux par inclusion

### Sémantique stable

1. Génération de tous les sous-ensembles de A
2. Filtrage des ensembles sans conflit
3. Vérification que tous les arguments extérieurs sont attaqués

**Note** : L'approche actuelle est exhaustive (complexité exponentielle). Pour des AF de plus de 20 arguments, des optimisations seraient nécessaires.

## 🔍 Tests

Le dossier `Fichiers-tests/` contient plusieurs cas de test :

```bash
# Tester avec les fichiers fournis
python3 programme.py -p VE-PR -f Fichiers-tests/test_af1.apx -a a,c,d
python3 programme.py -p DC-ST -f Fichiers-tests/test_af2.apx -a b
```

## ⚠️ Limitations connues

- Complexité exponentielle : impraticable au-delà de ~20 arguments
- Pas de cache pour les extensions calculées
- Pas d'optimisation par élagage (pruning)

## 👥 Auteurs

Thomas GOMES  
Master IAD - Université [Nom]

## 📚 Références

Projet basé sur les travaux de Dung (1995) sur l'argumentation abstraite :
- Dung, P. M. (1995). "On the acceptability of arguments and its fundamental role in nonmonotonic reasoning, logic programming and n-person games". *Artificial Intelligence*, 77(2), 321-357.
