import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from src.systeme_argumentation import AS


class TestAS(unittest.TestCase):
    """Tests pour la classe AS (Argumentation Framework)"""

    def setUp(self):
        """Initialise des AS pour les tests"""
        # AS simple: a -> b
        self.simple_as = AS({'a', 'b'}, {('a', 'b')})
        
        # AS de l'exemple du sujet: a -> b -> c, b -> d
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
        
        # AS avec un seul argument sans attaque
        self.single_as = AS({'a'}, set())

    def test_init_as(self):
        """Test de l'initialisation d'un AS"""
        systeme_arg = AS({'a', 'b'}, {('a', 'b')})
        self.assertEqual(systeme_arg.A, {'a', 'b'})
        self.assertEqual(systeme_arg.R, {('a', 'b')})

    def test_attackers_of_simple(self):
        """Test de la fonction attackers_of sur un cas simple"""
        attackers = self.simple_as.attackers_of('b')
        self.assertEqual(attackers, {'a'})

    def test_attackers_of_no_attacker(self):
        """Test attackers_of quand il n'y a pas d'attaquant"""
        attackers = self.simple_as.attackers_of('a')
        self.assertEqual(attackers, set())

    def test_attackers_of_multiple(self):
        """Test attackers_of avec plusieurs attaquants"""
        af = AS({'a', 'b', 'c'}, {('a', 'c'), ('b', 'c')})
        attackers = af.attackers_of('c')
        self.assertEqual(attackers, {'a', 'b'})

    def test_attackers_of_unknown_argument(self):
        """Test erreur quand l'argument n'existe pas"""
        with self.assertRaises(ValueError) as context:
            self.simple_as.attackers_of('z')
        
        self.assertIn("n'est pas dans les arguments", str(context.exception))

    def test_attacks_simple(self):
        """Test de la fonction attacks sur un cas simple"""
        attacked = self.simple_as.attacks('a')
        self.assertEqual(attacked, {'b'})

    def test_attacks_no_target(self):
        """Test attacks quand l'argument n'attaque personne"""
        attacked = self.simple_as.attacks('b')
        self.assertEqual(attacked, set())

    def test_attacks_multiple(self):
        """Test attacks avec plusieurs cibles"""
        attacked = self.example_as.attacks('b')
        self.assertEqual(attacked, {'c', 'd'})

    def test_attacks_unknown_argument(self):
        """Test erreur quand l'argument n'existe pas"""
        with self.assertRaises(ValueError) as context:
            self.simple_as.attacks('z')
        
        self.assertIn("n'est pas dans les arguments", str(context.exception))

    def test_self_attack(self):
        """Test auto-attaque"""
        af = AS({'a'}, {('a', 'a')})
        self.assertEqual(af.attackers_of('a'), {'a'})
        self.assertEqual(af.attacks('a'), {'a'})

    def test_empty_as_attacks(self):
        """Test sur un AS vide"""
        self.assertEqual(self.empty_as.A, set())
        self.assertEqual(self.empty_as.R, set())

    def test_single_argument_no_attack(self):
        """Test avec un seul argument sans attaque"""
        self.assertEqual(self.single_as.attackers_of('a'), set())
        self.assertEqual(self.single_as.attacks('a'), set())

    def test_cycle_attacks(self):
        """Test sur un AS avec cycle"""
        self.assertEqual(self.cycle_as.attackers_of('a'), {'c'})
        self.assertEqual(self.cycle_as.attacks('a'), {'b'})
        self.assertEqual(self.cycle_as.attackers_of('b'), {'a'})
        self.assertEqual(self.cycle_as.attacks('b'), {'c'})

    def test_bidirectional_attacks(self):
        """Test avec attaques bidirectionnelles"""
        af = AS({'a', 'b'}, {('a', 'b'), ('b', 'a')})
        self.assertEqual(af.attackers_of('a'), {'b'})
        self.assertEqual(af.attacks('a'), {'b'})
        self.assertEqual(af.attackers_of('b'), {'a'})
        self.assertEqual(af.attacks('b'), {'a'})


if __name__ == '__main__':
    unittest.main()
