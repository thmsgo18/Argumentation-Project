# 🎯 Projet Argumentation

> Projet de Master IAD - Représentation des Connaissances et Raisonnement  
> Année universitaire 2025-2026

## 📋 Description

Ce projet implémente un solveur pour systèmes d'argumentation (AS). Il permet de calculer et vérifier différents types d'extensions selon les sémantiques préférées (PR) et stables (ST).

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
python3 program.py -p <PROBLEME> -f <FICHIER> -a <ARGUMENTS>
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
python3 program.py -p VE-PR -f af.txt -a a,c,d
# Sortie: YES

# Vérifier l'acceptabilité crédule de 'b' (préférée)
python3 program.py -p DC-PR -f af.txt -a b
# Sortie: NO

# Vérifier l'acceptabilité sceptique de 'a' (préférée)
python3 program.py -p DS-PR -f af.txt -a a
# Sortie: YES

# Vérifier si {a,c,d} est une extension stable
python3 program.py -p VE-ST -f af.txt -a a,c,d
# Sortie: YES
```

## 📁 Structure du projet

```
Projet-RCR/
├── README.md                
├── program.py                   # Point d'entrée principal
├── src/
│   ├── __init__.py
│   ├── cli.py                   # Gestion des arguments en ligne de commande
│   ├── apx_parser.py            # Parser pour fichiers .apx
│   ├── systeme_argumentation.py # Classe pour le système d'argumentation
│   ├── semantics.py             # Algorithmes pour les sémantiques
│   └── queries.py               # Résolution des requêtes
└── Fichiers-tests/              # Fichiers de test fournis
    ├── test_af1.apx
    ├── test_af1_pr.txt
    ├── test_af1_st.txt
    ├── test_af2.apx
    ├── test_af2_pr.txt
    ├── test_af2_st.txt
    └── ...
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

## 🔍 Exemples de tests

Le dossier `Fichiers-tests/` contient plusieurs cas de test :

```bash
# Tester avec les fichiers fournis
python3 program.py -p VE-PR -f Fichiers-tests/test_af1.apx -a a,c,d
python3 program.py -p DC-ST -f Fichiers-tests/test_af2.apx -a b
```

## 👥 Auteurs

[@thmsgo18](https://github.com/thmsgo18)

[@RayaneParis](https://github.com/RayaneParis)
