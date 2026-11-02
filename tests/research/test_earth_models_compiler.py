"""Exercise the real compiler with Linux and Windows checkouts of its text CSV."""
import hashlib
import csv
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


class EarthModelCompilerTests(unittest.TestCase):
    def test_line_endings_do_not_change_compilation_but_changed_data_still_does(self):
        source = ROOT / 'Tierra/Investigacion/parte-1/muestras-indicadores-video.csv'
        lf = source.read_bytes().replace(b'\r\n', b'\n')
        expected = hashlib.sha256(lf).hexdigest()
        with tempfile.TemporaryDirectory(prefix='historicmap-earth-models-') as temp:
            root = Path(temp)
            script = root / 'scripts/prepare-earth-models.py'
            script.parent.mkdir()
            script.write_bytes((ROOT / 'scripts/prepare-earth-models.py').read_bytes())
            raw = root / 'Tierra/Fanerozoico/originales/PhanDA_GMSTandCO2_percentiles.csv'
            raw.parent.mkdir(parents=True)
            raw.write_bytes((ROOT / raw.relative_to(root)).read_bytes())
            target = root / source.relative_to(ROOT)
            target.parent.mkdir(parents=True)

            def compile_with(data):
                target.write_bytes(data)
                subprocess.run([sys.executable, str(script)], cwd=root, check=True,
                               capture_output=True)
                folder = root / 'Tierra/Fanerozoico'
                return ((folder / 'referencia-audiovisual.json').read_bytes(),
                        (folder / 'phanda.json').read_bytes())

            linux = compile_with(lf)
            windows = compile_with(lf.replace(b'\n', b'\r\n'))
            self.assertEqual(linux, windows)
            self.assertEqual(json.loads(linux[0])['transcriptionSha256'], expected)
            # A valid numeric cell change must still invalidate the source fingerprint.
            rows = list(csv.reader(io.StringIO(lf.decode('utf-8'))))
            column = rows[0].index('temperatureC_parsed')
            rows[1][column] = str(float(rows[1][column]) + 1)
            output = io.StringIO(newline='')
            csv.writer(output, lineterminator='\n').writerows(rows)
            changed = compile_with(output.getvalue().encode('utf-8'))
            self.assertNotEqual(json.loads(changed[0])['transcriptionSha256'], expected)
            self.assertNotEqual(json.loads(changed[0])['samples'], json.loads(linux[0])['samples'])


if __name__ == '__main__':
    unittest.main()
