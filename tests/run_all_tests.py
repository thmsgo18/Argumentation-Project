#!/usr/bin/env python3
"""
Script pour exécuter tous les tests unitaires du projet.

Usage:
    python3 tests/run_all_tests.py
    python3 tests/run_all_tests.py -v  (mode verbose)
"""

import unittest
import sys
import os

# Ajouter le répertoire parent au path pour pouvoir importer les modules src
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


def run_all_tests(verbosity=2):
    """
    Exécute tous les tests unitaires du projet.
    
    Args:
        verbosity: Niveau de détail (1=minimal, 2=normal)
    
    Returns:
        True si tous les tests passent, False sinon
    """
    # Découvrir tous les tests dans le répertoire tests/
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Exécuter les tests
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    
    # Afficher le résumé
    print("\n" + "="*70)
    print(f"Tests exécutés: {result.testsRun}")
    print(f"Succès: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Échecs: {len(result.failures)}")
    print(f"Erreurs: {len(result.errors)}")
    print("="*70)
    
    # Retourner le succès
    return result.wasSuccessful()


if __name__ == '__main__':
    # Vérifier si l'option verbose est demandée
    verbosity = 2
    if len(sys.argv) > 1 and sys.argv[1] in ['-v', '--verbose']:
        verbosity = 2
    elif len(sys.argv) > 1 and sys.argv[1] in ['-q', '--quiet']:
        verbosity = 1
    
    # Exécuter les tests
    success = run_all_tests(verbosity)
    
    # Retourner le code de sortie approprié
    sys.exit(0 if success else 1)
