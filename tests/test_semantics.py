import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from src.systeme_argumentation import AS
from src.semantics import (
    is_conflict_free,
    defends,
    is_admissible,
    is_stable,
    all_subsets,
    admissible_extensions,
    preferred_extensions,
    stable_extensions
)


class TestSemantics(unittest.TestCase):
    """Tests pour les fonctions de sémantique"""

    def setUp(self):
        """Initialise des AS pour les tests"""
        # AS simple: a -> b
        self.simple_as = AS({'a', 'b'}, {('a', 'b')})
        
        # AS de l'exemple: a -> b -> c, b -> d
        self.example_as = AS(
            {'a', 'b', 'c', 'd'},
            {('a', 'b'), ('b', 'c'), ('b', 'd')}
        )
        
        # AS avec cycle: a -> b -> c -> a
        self.cycle_as = AS(
            {'a', 'b', 'c'},
            {('a', 'b'), ('b', 'c'), ('c', 'a')}
        )
        
        # AS vide
        self.empty_as = AS(set(), set())
        
        # AS avec un seul argument
        self.single_as = AS({'a'}, set())

    # --- Tests pour is_conflict_free ---

    def test_conflict_free_empty_set(self):
        """Test que l'ensemble vide est sans conflit"""
        self.assertTrue(is_conflict_free(self.simple_as, set()))

    def test_conflict_free_single_argument(self):
        """Test qu'un seul argument est sans conflit"""
        self.assertTrue(is_conflict_free(self.simple_as, {'a'}))

    def test_conflict_free_no_attack(self):
        """Test ensemble sans conflit (pas d'attaque interne)"""
        self.assertTrue(is_conflict_free(self.example_as, {'a', 'c'}))

    def test_not_conflict_free(self):
        """Test ensemble avec conflit"""
        self.assertFalse(is_conflict_free(self.simple_as, {'a', 'b'}))

    def test_conflict_free_self_attack(self):
        """Test qu'une auto-attaque crée un conflit"""
        af = AS({'a'}, {('a', 'a')})
        self.assertFalse(is_conflict_free(af, {'a'}))

    def test_conflict_free_cycle(self):
        """Test conflit dans un cycle"""
        self.assertFalse(is_conflict_free(self.cycle_as, {'a', 'b'}))
        self.assertTrue(is_conflict_free(self.cycle_as, {'a'}))

    def test_conflict_free_unknown_argument_error(self):
        """Test erreur avec argument inconnu"""
        with self.assertRaises(ValueError):
            is_conflict_free(self.simple_as, {'z'})

    # --- Tests pour defends ---

    def test_defends_simple(self):
        """Test défense simple"""
        # {a} défend a car a n'a pas d'attaquant
        self.assertTrue(defends(self.simple_as, {'a'}, 'a'))

    def test_defends_counterattack(self):
        """Test qu'un ensemble défend en contre-attaquant"""
        # {a} défend c car a attaque b qui attaque c
        self.assertTrue(defends(self.example_as, {'a'}, 'c'))

    def test_not_defends(self):
        """Test qu'un ensemble ne défend pas"""
        # {d} ne défend pas b car a attaque b et d n'attaque pas a
        self.assertFalse(defends(self.example_as, {'d'}, 'b'))

    def test_defends_no_attackers(self):
        """Test défense d'un argument sans attaquant"""
        # Tout ensemble défend un argument qui n'a pas d'attaquant
        self.assertTrue(defends(self.example_as, set(), 'a'))

    def test_defends_empty_set(self):
        """Test que l'ensemble vide défend seulement les arguments sans attaquants"""
        self.assertTrue(defends(self.example_as, set(), 'a'))
        self.assertFalse(defends(self.example_as, set(), 'b'))

    def test_defends_unknown_argument_error(self):
        """Test erreur avec argument inconnu"""
        with self.assertRaises(ValueError):
            defends(self.simple_as, {'a'}, 'z')

    # --- Tests pour is_admissible ---

    def test_admissible_empty_set(self):
        """Test que l'ensemble vide est admissible"""
        self.assertTrue(is_admissible(self.simple_as, set()))

    def test_admissible_simple(self):
        """Test ensemble admissible simple"""
        self.assertTrue(is_admissible(self.simple_as, {'a'}))

    def test_not_admissible_conflict(self):
        """Test qu'un ensemble avec conflit n'est pas admissible"""
        self.assertFalse(is_admissible(self.simple_as, {'a', 'b'}))

    def test_not_admissible_not_defended(self):
        """Test qu'un ensemble non défendu n'est pas admissible"""
        # {b} n'est pas admissible car b est attaqué par a et {b} ne défend pas b
        self.assertFalse(is_admissible(self.simple_as, {'b'}))

    def test_admissible_example(self):
        """Test admissibilité sur l'exemple du sujet"""
        self.assertTrue(is_admissible(self.example_as, {'a'}))
        self.assertTrue(is_admissible(self.example_as, {'a', 'c', 'd'}))

    # --- Tests pour is_stable ---

    def test_stable_simple(self):
        """Test extension stable simple"""
        self.assertTrue(is_stable(self.simple_as, {'a'}))

    def test_not_stable_not_all_attacked(self):
        """Test qu'une extension stable doit attaquer tous les arguments extérieurs"""
        self.assertFalse(is_stable(self.example_as, {'a', 'c'}))

    def test_stable_example(self):
        """Test extension stable sur l'exemple"""
        self.assertTrue(is_stable(self.example_as, {'a', 'c', 'd'}))

    def test_not_stable_with_conflict(self):
        """Test qu'un ensemble avec conflit n'est pas stable"""
        self.assertFalse(is_stable(self.simple_as, {'a', 'b'}))

    def test_no_stable_extension_cycle(self):
        """Test qu'un cycle n'a pas d'extension stable"""
        extensions = stable_extensions(self.cycle_as)
        self.assertEqual(extensions, [])

    # --- Tests pour all_subsets ---

    def test_all_subsets_empty(self):
        """Test sous-ensembles de l'ensemble vide"""
        subsets = all_subsets(set())
        self.assertEqual(subsets, [set()])

    def test_all_subsets_single(self):
        """Test sous-ensembles d'un singleton"""
        subsets = all_subsets({'a'})
        self.assertEqual(len(subsets), 2)
        self.assertIn(set(), subsets)
        self.assertIn({'a'}, subsets)

    def test_all_subsets_count(self):
        """Test nombre de sous-ensembles (2^n)"""
        subsets = all_subsets({'a', 'b', 'c'})
        self.assertEqual(len(subsets), 8)  # 2^3

    # --- Tests pour admissible_extensions ---

    def test_admissible_extensions_simple(self):
        """Test extensions admissibles simples"""
        exts = admissible_extensions(self.simple_as)
        self.assertIn(set(), exts)
        self.assertIn({'a'}, exts)
        self.assertNotIn({'b'}, exts)

    def test_admissible_extensions_single(self):
        """Test extensions admissibles avec un seul argument"""
        exts = admissible_extensions(self.single_as)
        self.assertIn(set(), exts)
        self.assertIn({'a'}, exts)

    # --- Tests pour preferred_extensions ---

    def test_preferred_extensions_simple(self):
        """Test extensions préférées simples"""
        exts = preferred_extensions(self.simple_as)
        self.assertEqual(exts, [{'a'}])

    def test_preferred_extensions_example(self):
        """Test extensions préférées sur l'exemple du sujet"""
        exts = preferred_extensions(self.example_as)
        self.assertIn({'a', 'c', 'd'}, exts)

    def test_preferred_extensions_single(self):
        """Test extensions préférées avec un seul argument"""
        exts = preferred_extensions(self.single_as)
        self.assertEqual(exts, [{'a'}])

    def test_preferred_extensions_empty(self):
        """Test extensions préférées sur AS vide"""
        exts = preferred_extensions(self.empty_as)
        self.assertEqual(exts, [set()])

    def test_preferred_extensions_cycle(self):
        """Test extensions préférées sur un cycle"""
        exts = preferred_extensions(self.cycle_as)
        # Un cycle impair (3 arguments) n'a que l'ensemble vide comme extension préférée
        # car aucun argument ne peut se défendre contre son attaquant
        self.assertEqual(len(exts), 1)
        self.assertIn(set(), exts)

    # --- Tests pour stable_extensions ---

    def test_stable_extensions_simple(self):
        """Test extensions stables simples"""
        exts = stable_extensions(self.simple_as)
        self.assertEqual(exts, [{'a'}])

    def test_stable_extensions_example(self):
        """Test extensions stables sur l'exemple"""
        exts = stable_extensions(self.example_as)
        self.assertIn({'a', 'c', 'd'}, exts)

    def test_stable_extensions_single(self):
        """Test extensions stables avec un seul argument"""
        exts = stable_extensions(self.single_as)
        self.assertEqual(exts, [{'a'}])

    def test_stable_extensions_cycle_none(self):
        """Test qu'un cycle n'a pas d'extension stable"""
        exts = stable_extensions(self.cycle_as)
        self.assertEqual(exts, [])

    def test_stable_extensions_empty(self):
        """Test extensions stables sur AS vide"""
        exts = stable_extensions(self.empty_as)
        self.assertEqual(exts, [set()])


if __name__ == '__main__':
    unittest.main()
