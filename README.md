# Projet RCR

Projet de Master IAD - S1

## Description

Ajouter une description du projet ici.

## Installation

Instructions d'installation du projet.

## Utilisation

Instructions d'utilisation du projet.

## Arborescence

```
RCR/
├─ README.md
├─ program.py
├─ src/
│  ├─ __init__.py
│  ├─ cli.py
│  ├─ apx_parser.py
│  ├─ af.py
│  ├─ semantics.py
│  └─ queries.py
├─ Fichiers_tests/
│  ├─ af1.apx
│  ├─ af2.apx
│  └─ ...
├─ tests/
│  ├─ test_parser.py
│  ├─ test_semantics.py
│  └─ test_queries.py
└─ report/
   └─ Toto_Titi.pdf
```

# ✅ TODO List – Projet Argumentation

## 1. Gestion de la ligne de commande

- [ ] Parser l’option `-p`
  - Lire la valeur après `-p` et vérifier qu’elle est parmi : `VE-PR`, `DC-PR`, `DS-PR`, `VE-ST`, `DC-ST`, `DS-ST`.
- [ ] Parser l’option `-f`
  - Récupérer le chemin du fichier `.apx`, vérifier qu’il est présent et lisible.
- [ ] Parser l’option `-a`
  - Lire la liste d’arguments passée (ex. `a,b,c`) et la convertir en liste/ensemble Python.
- [ ] Vérifier la validité des arguments
  - Vérifier que toutes les options nécessaires sont présentes et qu’il n’y a pas d’option inconnue.
- [ ] Gérer les erreurs minimales
  - En cas de problème (option manquante, fichier introuvable, etc.), afficher un message clair et arrêter le programme.

---

## 2. Parser du fichier `.apx`

- [ ] Lire le fichier ligne par ligne
  - Ouvrir le fichier et parcourir chaque ligne en ignorant les lignes vides.
- [ ] Extraire les `arg(x).`
  - Pour chaque ligne qui commence par `arg(`, extraire `x` et l’ajouter à l’ensemble des arguments `A`.
- [ ] Extraire les `att(x,y).`
  - Pour chaque ligne qui commence par `att(`, extraire `x` et `y`, puis ajouter `(x,y)` à la relation d’attaque `R`.
- [ ] Vérifier que les arguments utilisés dans les attaques existent
  - S’assurer que `x` et `y` sont bien dans `A`; sinon, décider s’il faut lever une erreur ou les ignorer.
- [ ] Retourner les structures `A` et `R`
  - À la fin du parsing, retourner par exemple `A: set(str)` et `R: set(tuple(str,str))`.

---

## 3. Fonctions de base sur les attaques

- [ ] Fonction `attackers_of(a)`
  - Retourner l’ensemble de tous les arguments qui attaquent `a` (tous les `x` tels que `(x,a) ∈ R`).
- [ ] Fonction `attacks(a)`
  - Retourner l’ensemble de tous les arguments attaqués par `a` (tous les `x` tels que `(a,x) ∈ R`).
- [ ] Fonction `S_attacks(a)`
  - Retourner `True` si au moins un argument de `S` attaque `a`, sinon `False`.
- [ ] Fonction `S_undefended_argument(S)`
  - Parcourir les arguments de `S` et retourner un argument qui n’est pas défendu par `S` (ou `None` si tous le sont).

---

## 4. Vérifier qu’un ensemble est sans conflit

- [ ] Implémenter `is_conflict_free(S)`
  - Vérifier qu’il n’existe pas de paire `(a,b)` dans `S` telle que `(a,b) ∈ R` ou `(b,a) ∈ R`.
  - Retourner `True` si aucun conflit détecté, sinon `False`.

---

## 5. Vérifier la défense

- [ ] Implémenter `defends(S, a)`
  - Pour chaque attaquant `x` de `a` (i.e. `(x,a) ∈ R`), vérifier qu’il existe un `y ∈ S` tel que `(y,x) ∈ R`.
  - Retourner `True` si tous les attaquants de `a` sont contrattaqués par `S`, sinon `False`.

---

## 6. Vérifier l’admissibilité

- [ ] Implémenter `is_admissible(S)`
  - D’abord vérifier que `S` est sans conflit.
  - Puis vérifier que pour chaque `a ∈ S`, `S` défend `a` (en utilisant la fonction `defends`).
  - Retourner `True` si les deux conditions sont satisfaites, sinon `False`.

---

## 7. Générer les sous-ensembles d’arguments

- [ ] Générer tous les sous-ensembles de `A` (`all_subsets(A)`)
  - Utiliser une approche combinatoire (par exemple avec `itertools`) pour obtenir tous les `S ⊆ A`.
  - Retourner une liste (ou un générateur) de sous-ensembles, chaque sous-ensemble étant représenté comme `set`.

---

## 8. Calculer les extensions admissibles

- [ ] Calculer tous les ensembles admissibles
  - Parcourir tous les sous-ensembles `S ⊆ A`.
  - Garder ceux pour lesquels `is_admissible(S)` est vraie.
  - Retourner la liste de tous ces ensembles admissibles.

---

## 9. Calculer les extensions préférées

- [ ] Trouver les ensembles admissibles maximaux
  - À partir de la liste des ensembles admissibles, garder uniquement ceux qui sont **maximaux par inclusion** (aucun autre admissible ne les contient strictement).
- [ ] Implémenter `preferred_extensions(A,R)`
  - Combiner les étapes précédentes pour retourner la liste complète des extensions préférées.

---

## 10. Calculer les extensions stables

- [ ] Implémenter `is_stable(S)`
  - Vérifier que `S` est sans conflit.
  - Vérifier que pour tout argument `a ∉ S`, il existe un `b ∈ S` tel que `(b,a) ∈ R` (i.e. `S` attaque tous les arguments hors `S`).
- [ ] Implémenter `stable_extensions(A,R)`
  - Parcourir tous les sous-ensembles `S ⊆ A`.
  - Garder ceux pour lesquels `is_stable(S)` est vraie.
  - Retourner la liste de toutes les extensions stables.

---

## 11. Requêtes VE / DC / DS

### Pour les préférées (PR)

- [ ] `VE_PR(S)`
  - Calculer les extensions préférées.
  - Vérifier si l’ensemble `S` fourni dans la requête est exactement égal à l’une des extensions préférées.
- [ ] `DC_PR(a)`
  - Calculer les extensions préférées.
  - Retourner `YES` si `a` appartient à **au moins une** extension préférée, sinon `NO`.
- [ ] `DS_PR(a)`
  - Calculer les extensions préférées.
  - Retourner `YES` si `a` appartient à **toutes** les extensions préférées (et gérer le cas où il n’y en a pas, selon ta convention), sinon `NO`.

### Pour les stables (ST)

- [ ] `VE_ST(S)`
  - Calculer les extensions stables.
  - Vérifier si l’ensemble `S` de la requête est exactement égal à l’une des extensions stables.
- [ ] `DC_ST(a)`
  - Calculer les extensions stables.
  - Retourner `YES` si `a` appartient à **au moins une** extension stable, sinon `NO`.
- [ ] `DS_ST(a)`
  - Calculer les extensions stables.
  - Retourner `YES` si `a` appartient à **toutes** les extensions stables (et gérer le cas où il n’y en a pas), sinon `NO`.

---

## 12. Programme principal (`main`)

- [ ] Lire les options de la ligne de commande
  - Utiliser une bibliothèque (par ex. `argparse` en Python) ou parser manuellement `sys.argv`.
- [ ] Charger l’AF via le parser `.apx`
  - Appeler ta fonction de parsing pour obtenir `A` et `R`.
- [ ] Appeler la bonne fonction selon `-p`
  - En fonction de la valeur de `-p`, choisir entre PR/ST et VE/DC/DS.
- [ ] Afficher strictement `YES` ou `NO`
  - Ne rien afficher d’autre que `YES` ou `NO` sur la sortie standard, comme demandé dans le sujet.

---

## 13. Tests

- [ ] Tester avec l’exemple du sujet
  - Reprendre l’AF de l’énoncé et vérifier que tu obtiens bien les réponses données en exemple.
- [ ] Tester un AF sans extension stable
  - Construire un petit AF connu pour ne pas avoir d’extension stable et vérifier le comportement.
- [ ] Tester un AF avec cycle
  - Par exemple un cycle `a` attaque `b`, `b` attaque `c`, `c` attaque `a`, et vérifier les extensions.
- [ ] Tester un AF simple
  - Très petit AF (1 ou 2 arguments), pour vérifier les cas de base.
- [ ] Tester un cas limite (1 argument)
  - Un seul argument sans attaque, vérifier PR/ST, VE/DC/DS.
