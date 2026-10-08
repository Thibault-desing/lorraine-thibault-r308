import tempfile
import unittest
from pathlib import Path

from tp1.partie_c import MOTS_PAR_DEFAUT, charger_mots, choisir_mot, masque, normaliser_mot


class MotsTests(unittest.TestCase):
    def test_masque(self):
        self.assertEqual(masque("PYTHON"), ["_"] * 6)
        self.assertEqual(masque(""), [])

    def test_accents_et_majuscules(self):
        self.assertEqual(choisir_mot(["Python"]), "PYTHON")
        self.assertEqual(choisir_mot(["éléphant"]), "ÉLÉPHANT")
        self.assertEqual(normaliser_mot("e\u0301léphant"), "ÉLÉPHANT")
        self.assertIn(choisir_mot([]), MOTS_PAR_DEFAUT)

    def test_fichier_invalide_ou_absent(self):
        with tempfile.TemporaryDirectory() as dossier:
            fichier = Path(dossier) / "mots.txt"
            self.assertEqual(charger_mots(fichier), MOTS_PAR_DEFAUT)
            fichier.write_text("Python\n\n123\néléphant\n", encoding="utf-8")
            self.assertEqual(charger_mots(fichier), ["PYTHON", "ÉLÉPHANT"])
            fichier.write_text("123", encoding="utf-8")
            self.assertEqual(charger_mots(fichier), MOTS_PAR_DEFAUT)
