"""Additional named rulers, regents and canonical polity identities."""
import pathlib,importlib.util,urllib.parse,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('r',ROOT/'scripts/review-019-core-rulers.py');r=importlib.util.module_from_spec(s);s.loader.exec_module(r);h=r.h
r.GROUPS=[
 ('SAVOY-DUCHY','Duque de Saboya',['Charles Emmanuel I, Duke of Savoy','Victor Amadeus I, Duke of Savoy','Francis Hyacinth, Duke of Savoy','Charles Emmanuel II, Duke of Savoy','Victor Amadeus II of Sardinia']),
 ('ETH','Emperador de Etiopía',['Za Dengel','Susenyos I','Fasilides','Yohannes I','Iyasu I']),
 ('HIST-Q796583','Rey del Kongo',['Álvaro II of Kongo','Álvaro III of Kongo','Pedro II of Kongo','Garcia I of Kongo','Ambrósio I of Kongo','Álvaro IV of Kongo','Álvaro V of Kongo','Álvaro VI of Kongo','Garcia II of Kongo','António I of Kongo']),
 ('FRA','Regencia de Francia',['Marie de Medici','Anne of Austria']),
 ('RUSSIA-TSARDOM','Regente de Rusia',['Sophia Alekseyevna']),
 ('PRT','Regencia de Portugal',['Luisa de Guzmán']),
 ('ESP','Regencia de España',['Mariana of Austria']),
 ('DUTCH-REPUBLIC','Gran pensionario de Holanda',['Johan de Witt']),
 ('QING','Regencia manchú',['Dorgon']),
 ('HESSE-DARMSTADT','Landgrave de Hesse-Darmstadt',['George II, Landgrave of Hesse-Darmstadt']),
 ('SWE','Rey de Suecia',['Sigismund III Vasa'])]
code=(ROOT/'scripts/review-019-core-rulers.py').read_text(encoding='utf8');code=code[code.index('def main():'):code.index("if __name__")].replace('core019-rulers.json','rulers020-extra-candidates.json').replace('core019meta-','extra020meta-');exec(compile(code,'extra020','exec'),r.__dict__)
if __name__=='__main__':
 r.main()
 titles=['Shun dynasty','Duchy of Bavaria','Electorate of Brandenburg','Commonwealth of England','Iberian Union','Saadi Sultanate','Later Jin (1616–1636)','Southern Ming']
 params=dict(action='wbgetentities',sites='enwiki',titles='|'.join(titles),props='labels|claims|sitelinks',redirects='yes',format='json');d=h.get('https://www.wikidata.org/w/api.php?'+urllib.parse.urlencode(params),'020-polity-checks');h.save(ROOT/'.cache/polities020-verified.json',d)
 for q,e in d['entities'].items():
  if 'id' in e:print('POLITY',q,h.label(e),e.get('sitelinks',{}).get('enwiki',{}).get('title'),flush=True)
 for name in ['Frederick William Great Elector','Suleiman II Ottoman sultan']:
  params=dict(action='wbsearchentities',search=name,language='en',limit=3,format='json');d=h.get('https://www.wikidata.org/w/api.php?'+urllib.parse.urlencode(params),'020-name-'+name.replace(' ','-'));print('CHECK',name,[(v['id'],v.get('label'),v.get('description')) for v in d.get('search',[])],flush=True)
