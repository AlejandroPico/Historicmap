"""The published vocabulary must remain reproducible from the pinned official input."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]


class EarthChronologyReproduction(unittest.TestCase):
    def test_published_vocabulary_matches_the_versioned_official_input(self):
        spec = importlib.util.spec_from_file_location('earth_chronology', ROOT / 'scripts/prepare-earth-chronology.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        published = json.loads((ROOT / 'Tierra/Cronologia/ics-2026-06.json').read_text(encoding='utf-8'))
        self.assertEqual(published, module.prepare())
