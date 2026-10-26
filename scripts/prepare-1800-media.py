"""Reuse the reviewed original-byte symbol acquisition, with bounded new rows."""
import importlib.util,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('symbols',ROOT/'scripts/curate-1840-media.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
m.TAG='curated-symbols-1800-0.17'
m.PORTRAITS=[]
m.ROWS=[('GBR','Flag of Great Britain (1707–1800).svg',1800,1800),('ITALIAN-REPUBLIC-1802','Flag of the Italian Republic (1802).svg',1803,1804),('NAPOLEONIC-ITALY','Flag of the Napoleonic Kingdom of Italy.svg',1806,1813)]
m.REUSE=[('PRUSSIA','Flag of the Kingdom of Prussia (1803-1892).svg',1804,1819),('PRUSSIA','Flag of the Kingdom of Prussia (1803-1892).svg',1820,1839),('AUSTRIAN-EMPIRE','Flag of the Habsburg Monarchy.svg',1805,1819)]
if __name__=='__main__':
 m.main()
 import shutil
 shutil.copy2(ROOT/'.cache/media1840-audit.json',ROOT/'.cache/media1800-audit.json')
