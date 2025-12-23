import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from src.cli import parse_args


class TestCLI(unittest.TestCase):
    """Tests pour le parseur d'arguments en ligne de commande"""

    def test_parse_args_ve_pr(self):
        """Test parsing pour VE-PR"""
        args = parse_args(['-p', 'VE-PR', '-f', 'test.apx', '-a', 'a,b,c'])
        
        self.assertEqual(args['probleme'], 'VE-PR')
        self.assertEqual(args['file'], 'test.apx')
        self.assertEqual(args['arguments'], 'a,b,c')

    def test_parse_args_dc_pr(self):
        """Test parsing pour DC-PR"""
        args = parse_args(['-p', 'DC-PR', '-f', 'test.apx', '-a', 'b'])
        
        self.assertEqual(args['probleme'], 'DC-PR')
        self.assertEqual(args['file'], 'test.apx')
        self.assertEqual(args['arguments'], 'b')

    def test_parse_args_ds_st(self):
        """Test parsing pour DS-ST"""
        args = parse_args(['-p', 'DS-ST', '-f', 'af.txt', '-a', 'x'])
        
        self.assertEqual(args['probleme'], 'DS-ST')
        self.assertEqual(args['file'], 'af.txt')
        self.assertEqual(args['arguments'], 'x')

    def test_parse_args_ve_st(self):
        """Test parsing pour VE-ST"""
        args = parse_args(['-p', 'VE-ST', '-f', 'af.txt', '-a', 'a,c,d'])
        
        self.assertEqual(args['probleme'], 'VE-ST')
        self.assertEqual(args['file'], 'af.txt')
        self.assertEqual(args['arguments'], 'a,c,d')

    def test_parse_args_all_problems(self):
        """Test parsing pour tous les types de problèmes"""
        problems = ['VE-PR', 'DC-PR', 'DS-PR', 'VE-ST', 'DC-ST', 'DS-ST']
        
        for problem in problems:
            args = parse_args(['-p', problem, '-f', 'test.apx', '-a', 'a'])
            self.assertEqual(args['probleme'], problem)

    def test_parse_args_missing_p(self):
        """Test erreur quand -p est manquant"""
        with self.assertRaises(SystemExit):
            parse_args(['-f', 'test.apx', '-a', 'a'])

    def test_parse_args_missing_f(self):
        """Test erreur quand -f est manquant"""
        with self.assertRaises(SystemExit):
            parse_args(['-p', 'VE-PR', '-a', 'a'])

    def test_parse_args_missing_a(self):
        """Test erreur quand -a est manquant"""
        with self.assertRaises(SystemExit):
            parse_args(['-p', 'VE-PR', '-f', 'test.apx'])

    def test_parse_args_invalid_problem(self):
        """Test erreur avec un problème invalide"""
        with self.assertRaises(SystemExit):
            parse_args(['-p', 'INVALID', '-f', 'test.apx', '-a', 'a'])

    def test_parse_args_empty_argument(self):
        """Test parsing avec argument vide"""
        args = parse_args(['-p', 'DC-PR', '-f', 'test.apx', '-a', ''])
        self.assertEqual(args['arguments'], '')

    def test_parse_args_multiple_arguments(self):
        """Test parsing avec plusieurs arguments séparés par virgules"""
        args = parse_args(['-p', 'VE-PR', '-f', 'test.apx', '-a', 'a,b,c,d'])
        self.assertEqual(args['arguments'], 'a,b,c,d')

    def test_parse_args_single_argument(self):
        """Test parsing avec un seul argument"""
        args = parse_args(['-p', 'DC-PR', '-f', 'test.apx', '-a', 'x'])
        self.assertEqual(args['arguments'], 'x')

    def test_parse_args_file_path(self):
        """Test parsing avec différents chemins de fichiers"""
        paths = [
            'test.apx',
            './test.apx',
            '../test.apx',
            '/absolute/path/test.apx',
            'Fichiers-tests/test_as1.apx'
        ]
        
        for path in paths:
            args = parse_args(['-p', 'VE-PR', '-f', path, '-a', 'a'])
            self.assertEqual(args['file'], path)


if __name__ == '__main__':
    unittest.main()
