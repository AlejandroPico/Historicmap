"""Explicit historical office statements1700–1799, candidates only."""
import pathlib,importlib.util
ROOT=pathlib.Path(__file__).resolve().parents[1]
# Same reviewed office registry and human/citizenship checks, new bounded query.
source=(ROOT/'scripts/acquire-1800-offices.py').read_text(encoding='utf8')
source=source.replace('1800–1819','1700–1799').replace('1819-12-31','1799-12-31').replace('1800-01-01','1700-01-01').replace('offices-1800-1819-','offices-1700-1799-').replace('historical-offices-0.17','historical-offices-0.19').replace('historical-offices-017.json','historical-offices-019.json')
exec(compile(source,str(ROOT/'scripts/acquire-1800-offices.py'),'exec'),{'__name__':'__main__','__file__':str(ROOT/'scripts/acquire-1800-offices.py')})
