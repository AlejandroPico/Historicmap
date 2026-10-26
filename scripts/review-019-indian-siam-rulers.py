"""Named office research for early modern India and Ayutthaya."""
import pathlib,importlib.util
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('r',ROOT/'scripts/review-019-core-rulers.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
r.GROUPS=[
 ('HIST-Q33296','Emperador mogol',['Aurangzeb','Bahadur Shah I','Jahandar Shah','Farrukhsiyar','Rafi ud-Darajat','Shah Jahan II','Muhammad Shah','Ahmad Shah Bahadur','Alamgir II','Shah Jahan III','Shah Alam II']),
 ('HIST-Q83618','Chhatrapati · soberano maratha',['Rajaram I','Shivaji II','Shahu I','Rajaram II of Satara','Shahu II']),
 ('HIST-Q83618','Peshwa · Gobierno de la confederación',['Balaji Vishwanath','Baji Rao I','Balaji Baji Rao','Madhavrao I','Narayan Rao','Raghunath Rao','Madhavrao II','Baji Rao II']),
 ('AYUTTHAYA','Rey de Ayutthaya',['Phetracha','Sanphet VIII','Thai Sa','Borommakot','Uthumphon','Ekkathat'])]
code=(ROOT/'scripts/review-019-core-rulers.py').read_text(encoding='utf8');code=code[code.index('def main():'):code.index("if __name__")].replace('core019-rulers.json','indian-siam019-rulers.json');r.__dict__['GROUPS']=r.GROUPS;exec(compile(code,'indian-siam019','exec'),r.__dict__);r.main()
