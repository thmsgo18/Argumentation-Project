import sys
import os
import tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from src.apx_parser import parse_apx


class TestApxParser(unittest.TestCase):
    """Tests pour le parser de fichiers .apx"""

    def setUp(self):
        """Crée un répertoire temporaire pour les tests"""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Nettoie les fichiers temporaires"""
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)

    def create_temp_file(self, content: str) -> str:
        """Crée un fichier temporaire avec le contenu donné"""
        file_path = os.path.join(self.temp_dir, "test.apx")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return file_path

    def test_parse_simple_as(self):
        """Test parsing d'un AS simple"""
        content = "arg(a).\narg(b).\natt(a,b).\n"
        file_path = self.create_temp_file(content)
        
        A, R = parse_apx(file_path)
        
        self.assertEqual(A, {'a', 'b'})
        self.assertEqual(R, {('a', 'b')})

    def test_parse_multiple_arguments(self):
        """Test parsing avec plusieurs arguments"""
        content = "arg(a).\narg(b).\narg(c).\narg(d).\n"
        file_path = self.create_temp_file(content)
        
        A, R = parse_apx(file_path)
        
        self.assertEqual(A, {'a', 'b', 'c', 'd'})
        self.assertEqual(R, set())

    def test_parse_multiple_attacks(self):
        """Test parsing avec plusieurs attaques"""
        content = "arg(a).\narg(b).\narg(c).\natt(a,b).\natt(b,c).\n"
        file_path = self.create_temp_file(content)
        
        A, R = parse_apx(file_path)
        
        self.assertEqual(A, {'a', 'b', 'c'})
        self.assertEqual(R, {('a', 'b'), ('b', 'c')})

    def test_parse_empty_file(self):
        """Test parsing d'un fichier vide"""
        content = ""
        file_path = self.create_temp_file(content)
        
        A, R = parse_apx(file_path)
        
        self.assertEqual(A, set())
        self.assertEqual(R, set())

    def test_parse_self_attack(self):
        """Test parsing d'une auto-attaque"""
        content = "arg(a).\natt(a,a).\n"
        file_path = self.create_temp_file(content)
        
        A, R = parse_apx(file_path)
        
        self.assertEqual(A, {'a'})
        self.assertEqual(R, {('a', 'a')})

    def test_parse_case_insensitive(self):
        """Test que les arguments sont convertis en minuscules"""
        content = "arg(A).\narg(B).\natt(A,B).\n"
        file_path = self.create_temp_file(content)
        
        A, R = parse_apx(file_path)
        
        self.assertEqual(A, {'a', 'b'})
        self.assertEqual(R, {('a', 'b')})

    def test_parse_with_blank_lines(self):
        """Test parsing avec des lignes vides"""
        content = "arg(a).\n\narg(b).\n\natt(a,b).\n"
        file_path = self.create_temp_file(content)
        
        A, R = parse_apx(file_path)
        
        self.assertEqual(A, {'a', 'b'})
        self.assertEqual(R, {('a', 'b')})

    def test_parse_argument_not_declared_error(self):
        """Test erreur quand un argument est utilisé avant d'être déclaré"""
        content = "att(a,b).\narg(a).\narg(b).\n"
        file_path = self.create_temp_file(content)
        
        with self.assertRaises(ValueError) as context:
            parse_apx(file_path)
        
        error_msg = str(context.exception).lower()
        self.assertTrue("avant" in error_msg and "déclaré" in error_msg)

    def test_parse_complex_as(self):
        """Test parsing du AS de l'exemple du sujet"""
        content = "arg(a).\narg(b).\narg(c).\narg(d).\natt(a,b).\natt(b,c).\natt(b,d).\n"
        file_path = self.create_temp_file(content)
        
        A, R = parse_apx(file_path)
        
        self.assertEqual(A, {'a', 'b', 'c', 'd'})
        self.assertEqual(R, {('a', 'b'), ('b', 'c'), ('b', 'd')})

    def test_parse_with_underscores(self):
        """Test parsing d'arguments avec underscores"""
        content = "arg(arg_1).\narg(arg_2).\natt(arg_1,arg_2).\n"
        file_path = self.create_temp_file(content)
        
        A, R = parse_apx(file_path)
        
        self.assertEqual(A, {'arg_1', 'arg_2'})
        self.assertEqual(R, {('arg_1', 'arg_2')})


if __name__ == '__main__':
    unittest.main()
