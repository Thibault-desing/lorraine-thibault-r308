import tempfile
import unittest
from pathlib import Path

from tp1.partie_a import ajouter_etudiant, charger, meilleur_etudiant, moyenne_classe, sauvegarder


class EtudiantsTests(unittest.TestCase):
    def test_exemple_et_mise_a_jour(self):
        notes = {}
        for nom, note in [("Alice", 12), ("Bob", "15"), ("Claire", 9.5)]:
            self.assertTrue(ajouter_etudiant(notes, nom, note))
        self.assertEqual(moyenne_classe(notes), 12.17)
        self.assertEqual(meilleur_etudiant(notes), ("Bob", 15.0))
        ajouter_etudiant(notes, "Alice", 18)
        self.assertEqual(len(notes), 3)
        self.assertEqual(meilleur_etudiant(notes), ("Alice", 18.0))

    def test_vide_et_invalides(self):
        self.assertEqual(moyenne_classe({}), 0.0)
        self.assertIsNone(meilleur_etudiant({}))
        notes = {}
        for nom, note in [("", 12), ("A:B", 1), ("Ana", "x"), ("Ana", "nan"),
                          ("Ana", "inf"), ("Ana", None), ("A\nB", 1)]:
            self.assertFalse(ajouter_etudiant(notes, nom, note))
        self.assertEqual(notes, {})

    def test_fichiers(self):
        with tempfile.TemporaryDirectory() as dossier:
            fichier = Path(dossier) / "notes.txt"
            self.assertEqual(charger(fichier), {})
            self.assertTrue(sauvegarder({"Élodie": 14.5}, fichier))
            self.assertEqual(charger(fichier), {"Élodie": 14.5})
            fichier.write_text("Alice:12\nerreur\nBob:abc\nClaire:9.5\nX:nan\n", encoding="utf-8")
            self.assertEqual(charger(fichier), {"Alice": 12.0, "Claire": 9.5})
            self.assertFalse(sauvegarder({"Ana": 2}, Path(dossier) / "absent" / "x"))
            self.assertEqual(charger(Path(dossier)), {})

    def test_validation_avant_ecriture(self):
        with tempfile.TemporaryDirectory() as dossier:
            fichier = Path(dossier) / "notes.txt"
            fichier.write_text("Alice:12.0\n", encoding="utf-8")
            self.assertFalse(sauvegarder({"Ana": "invalide"}, fichier))
            self.assertEqual(charger(fichier), {"Alice": 12.0})
