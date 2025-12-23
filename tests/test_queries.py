import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from src.systeme_argumentation import AS
from src.queries import (
    solve_query,
    ve_pr, dc_pr, ds_pr,
    ve_st, dc_st, ds_st
)


class TestQueries(unittest.TestCase):
    """Tests pour les fonctions de requêtes"""

    def setUp(self):
        """Initialise des AS pour les tests"""
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
        
        # AS simple: a -> b
        self.simple_as = AS({'a', 'b'}, {('a', 'b')})
        
        # AS avec un seul argument
        self.single_as = AS({'a'}, set())

    # --- Tests VE-PR (Verify Extension - Preferred) ---

    def test_ve_pr_valid_extension(self):
        """Test VE-PR avec une extension valide"""
        result = ve_pr(self.example_as, {'a', 'c', 'd'})
        self.assertTrue(result)

    def test_ve_pr_invalid_extension(self):
        """Test VE-PR avec une extension invalide"""
        result = ve_pr(self.example_as, {'a'})
        self.assertFalse(result)

    def test_ve_pr_empty_set(self):
        """Test VE-PR avec l'ensemble vide"""
        result = ve_pr(self.simple_as, set())
        self.assertFalse(result)

    def test_ve_pr_example_from_subject(self):
        """Test VE-PR selon l'exemple du sujet"""
        # L'exemple dit: ./my_solver -p VE-PR -f af.txt -a a,c,d => YES
        result = ve_pr(self.example_as, {'a', 'c', 'd'})
        self.assertTrue(result)
        
        # L'exemple dit: ./my_solver -p VE-PR -f af.txt -a a => NO
        result = ve_pr(self.example_as, {'a'})
        self.assertFalse(result)

    # --- Tests DC-PR (Decide Credulous - Preferred) ---

    def test_dc_pr_argument_in_extension(self):
        """Test DC-PR pour un argument dans une extension"""
        result = dc_pr(self.example_as, 'a')
        self.assertTrue(result)

    def test_dc_pr_argument_not_in_any_extension(self):
        """Test DC-PR pour un argument absent de toutes les extensions"""
        result = dc_pr(self.example_as, 'b')
        self.assertFalse(result)

    def test_dc_pr_example_from_subject(self):
        """Test DC-PR selon l'exemple du sujet"""
        # L'exemple dit: ./my_solver -p DC-PR -f af.txt -a b => NO
        result = dc_pr(self.example_as, 'b')
        self.assertFalse(result)

    def test_dc_pr_cycle(self):
        """Test DC-PR sur un cycle (aucun argument n'est crédule car seul vide est admissible)"""
        # Dans un cycle, seul l'ensemble vide est préféré
        self.assertFalse(dc_pr(self.cycle_as, 'a'))
        self.assertFalse(dc_pr(self.cycle_as, 'b'))
        self.assertFalse(dc_pr(self.cycle_as, 'c'))

    # --- Tests DS-PR (Decide Skeptical - Preferred) ---

    def test_ds_pr_argument_in_all_extensions(self):
        """Test DS-PR pour un argument dans toutes les extensions"""
        result = ds_pr(self.example_as, 'a')
        self.assertTrue(result)

    def test_ds_pr_argument_not_in_all_extensions(self):
        """Test DS-PR pour un argument absent d'au moins une extension"""
        result = ds_pr(self.simple_as, 'b')
        self.assertFalse(result)

    def test_ds_pr_example_from_subject(self):
        """Test DS-PR selon l'exemple du sujet"""
        # L'exemple dit: ./my_solver -p DS-PR -f af.txt -a a => YES
        result = ds_pr(self.example_as, 'a')
        self.assertTrue(result)

    def test_ds_pr_single_argument(self):
        """Test DS-PR avec un seul argument"""
        result = ds_pr(self.single_as, 'a')
        self.assertTrue(result)

    def test_ds_pr_cycle(self):
        """Test DS-PR sur un cycle (aucun argument n'est sceptique)"""
        self.assertFalse(ds_pr(self.cycle_as, 'a'))
        self.assertFalse(ds_pr(self.cycle_as, 'b'))
        self.assertFalse(ds_pr(self.cycle_as, 'c'))

    # --- Tests VE-ST (Verify Extension - Stable) ---

    def test_ve_st_valid_extension(self):
        """Test VE-ST avec une extension stable valide"""
        result = ve_st(self.example_as, {'a', 'c', 'd'})
        self.assertTrue(result)

    def test_ve_st_invalid_extension(self):
        """Test VE-ST avec une extension non stable"""
        result = ve_st(self.example_as, {'a'})
        self.assertFalse(result)

    def test_ve_st_cycle_no_stable(self):
        """Test VE-ST sur un cycle (pas d'extension stable)"""
        result = ve_st(self.cycle_as, {'a'})
        self.assertFalse(result)

    # --- Tests DC-ST (Decide Credulous - Stable) ---

    def test_dc_st_argument_in_stable(self):
        """Test DC-ST pour un argument dans une extension stable"""
        result = dc_st(self.example_as, 'a')
        self.assertTrue(result)

    def test_dc_st_argument_not_in_stable(self):
        """Test DC-ST pour un argument absent des extensions stables"""
        result = dc_st(self.example_as, 'b')
        self.assertFalse(result)

    def test_dc_st_cycle_no_stable(self):
        """Test DC-ST sur un cycle (pas d'extension stable)"""
        result = dc_st(self.cycle_as, 'a')
        self.assertFalse(result)

    # --- Tests DS-ST (Decide Skeptical - Stable) ---

    def test_ds_st_argument_in_all_stable(self):
        """Test DS-ST pour un argument dans toutes les extensions stables"""
        result = ds_st(self.example_as, 'a')
        self.assertTrue(result)

    def test_ds_st_argument_not_in_all_stable(self):
        """Test DS-ST pour un argument absent d'au moins une extension stable"""
        af = AS({'a', 'b', 'c'}, {('a', 'b'), ('b', 'a')})
        result = ds_st(af, 'c')
        self.assertTrue(result)

    def test_ds_st_cycle_no_stable(self):
        """Test DS-ST sur un cycle (pas d'extension stable, retourne True par convention)"""
        result = ds_st(self.cycle_as, 'a')
        self.assertTrue(result)

    def test_ds_st_single_argument(self):
        """Test DS-ST avec un seul argument"""
        result = ds_st(self.single_as, 'a')
        self.assertTrue(result)

    # --- Tests solve_query (fonction principale) ---

    def test_solve_query_ve_pr(self):
        """Test solve_query pour VE-PR"""
        result = solve_query('VE-PR', self.example_as, {'a', 'c', 'd'})
        self.assertTrue(result)

    def test_solve_query_dc_pr(self):
        """Test solve_query pour DC-PR"""
        result = solve_query('DC-PR', self.example_as, 'a')
        self.assertTrue(result)

    def test_solve_query_ds_pr(self):
        """Test solve_query pour DS-PR"""
        result = solve_query('DS-PR', self.example_as, 'a')
        self.assertTrue(result)

    def test_solve_query_ve_st(self):
        """Test solve_query pour VE-ST"""
        result = solve_query('VE-ST', self.example_as, {'a', 'c', 'd'})
        self.assertTrue(result)

    def test_solve_query_dc_st(self):
        """Test solve_query pour DC-ST"""
        result = solve_query('DC-ST', self.example_as, 'a')
        self.assertTrue(result)

    def test_solve_query_ds_st(self):
        """Test solve_query pour DS-ST"""
        result = solve_query('DS-ST', self.example_as, 'a')
        self.assertTrue(result)

    def test_solve_query_invalid_problem(self):
        """Test solve_query avec un problème invalide"""
        with self.assertRaises(ValueError) as context:
            solve_query('INVALID', self.example_as, 'a')
        
        self.assertIn("Problème inconnu", str(context.exception))


if __name__ == '__main__':
    unittest.main()
