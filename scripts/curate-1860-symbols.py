"""Bounded reuse of already accredited historical symbol families.

No media downloads; prior1880+ windows and bytes stay unchanged. These are
representative designs, not a claim of identical material standards in each year.
"""
import json,pathlib,copy
ROOT=pathlib.Path(__file__).resolve().parents[1];path=ROOT/'public/data/identities.json'
def curate(data):
 data=copy.deepcopy(data)
 rows=[('PRT','1860-01-01','1879-12-31','Flag of Portugal (1830–1910).svg'),('OTT','1860-01-01','1879-12-31','Flag of the Ottoman Empire (1844–1922).svg'),('AUT-HUN','1869-12-31','1879-12-31','Ensign of Austro-Hungarian civil fleet (1869-1918).svg'),('DEU','1871-12-31','1879-12-31','Flag of the German Empire.svg'),('BRA-EMPIRE','1860-01-01','1879-12-31','Flag of Brazil (1853-1889).svg'),('HAW-KINGDOM','1860-01-01','1879-12-31','Flag of Hawaii.svg'),('TON','1875-12-31','1879-12-31','Flag of Tonga.svg')]
 for key,start,end,title in rows:
  country=data['countries'][key]
  source=next(f for c in data['countries'].values() for f in c['flags'] if f['media']['title']==title)
  country['flags']=[f for f in country['flags'] if f.get('acquisition')!='curated-symbols-1860-0.14']
  country['flags'].append(dict(start=start,end=end,media=source['media'],source=source['source'],intervalSource=source.get('intervalSource',source['source']),acquisition='curated-symbols-1860-0.14',note='Familia histórica representativa reutilizada del archivo acreditado, con ventana anterior explícita. El pabellón austrohúngaro es mercante, no una bandera nacional unitaria.'))
 return data
if __name__=='__main__':
 old=json.loads(path.read_text(encoding='utf8'));new=curate(old);assert curate(new)==new
 path.write_text(json.dumps(new,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
 print('Seven bounded symbol windows; later records unchanged')
