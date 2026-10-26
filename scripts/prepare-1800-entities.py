"""1800–1819 identities on untouched annual Cliopatria geometry."""
import pathlib,json,copy
OUT=pathlib.Path(__file__).resolve().parents[1]/'public/data'
read=lambda f:json.loads((OUT/f).read_text(encoding='utf8'))
def prepare(base,ids):
 d=copy.deepcopy(base);d.update(coverageStart=1800,coverageEnd=1819,referenceDate='2026-10-26')
 remove={'FRA','ESP','HTI','GBR','ITA','GRC','TEXAS','COL','MEX','HIST-Q285658','HIST-Q199821'}
 d['records']=[dict(r,start=1800,end=1819) for r in d['records'] if r['start']==1820 and r['end']==1839 and r['key'] not in remove]
 for k,c in ids['countries'].items():
  if c.get('qid'):d['qidKeys'].setdefault(c['qid'],k)
 d['names'].update({k:c['name'] for k,c in ids['countries'].items()})
 def row(names,key,label,a=1800,b=1819,admin='',status='independent',note=''):
  d['records'].append(dict(names=names,key=key,label=label,entityCode=key,start=a,end=b,admin=admin,status=status,source='https://github.com/Seshat-Global-History-Databank/cliopatria',note=note+' Síntesis anual de fuente; no reconstrucción de fronteras diarias.'))
 fr=['French First Republic','French Consulate','First French Empire','Bourbon Kingdom of France','France']
 row(fr,'FRA','Francia · Consulado',b=1803)
 row(fr,'FRA','Francia · Primer Imperio',a=1804,b=1813,note='Proclamación imperial en mayo1804, distinta de la coronación de diciembre.')
 row(fr,'FRA','Francia · Primera Restauración',a=1814,b=1814,note='El año también incluye el final del primer reinado imperial.')
 row(fr,'FRA','Francia · Cien Días y Segunda Restauración',a=1815,b=1815,note='Las autoridades del año conservan fases separadas; el mapa anual no representa todos los frentes del periodo.')
 row(fr,'FRA','Francia · Restauración borbónica',a=1816)
 row(['Kingdom of Spain','Spanish Empire'],'ESP','España · monarquía de Carlos IV',b=1807)
 row(['Kingdom of Spain','Spanish Empire'],'ESP','España · guerra y autoridades rivales',a=1808,b=1813,note='José Bonaparte, juntas y regencias fernandinas disputan el poder. El contorno no separa los frentes internos; no implica control uniforme de un bando.')
 row(['Kingdom of Spain','Spanish Empire'],'ESP','España · restauración de Fernando VII',a=1814)
 row(['Kingdom of Great Britain','British Empire'],'GBR','Gran Bretaña e Irlanda · coronas separadas',b=1800)
 row(['Kingdom of Great Britain','British Empire'],'GBR','Reino Unido de Gran Bretaña e Irlanda',a=1801)
 row(['Italian Republic'],'ITALIAN-REPUBLIC-1802','República Italiana napoleónica',a=1802,b=1804)
 row(['Italian Republic'],'NAPOLEONIC-ITALY','Reino de Italia napoleónico',a=1805,b=1814,note='La etiqueta republicana y el QID de la Italia actual de la fuente no identifican este reino.')
 row(['Kingdom of Naples (Napoleonic)'],'NAPLES-BOURBON','Reino de Nápoles borbónico',b=1805,note='Se rechaza la etiqueta napoleónica anterior a1806.')
 row(['Kingdom of Naples (Napoleonic)'],'NAPOLEONIC-NAPLES','Reino de Nápoles napoleónico',a=1806,b=1814)
 row(['Kingdom of Naples (Napoleonic)'],'NAPLES-BOURBON','Nápoles · restauración borbónica',a=1815,b=1815)
 row(['Haiti','Empire of Haiti'],'HTI','Saint-Domingue · revolución y dominio colonial',b=1803,admin='FRA',status='contested-colony',note='La revolución y los poderes locales no se equiparan a una administración colonial uniforme. Independencia en1804.')
 row(['Haiti','Empire of Haiti'],'HTI','Haití · independencia y Primer Imperio',a=1804,b=1806,note='La independencia y la proclamación imperial son momentos diferentes. El año1806 incluye la muerte de Dessalines y la ruptura posterior.')
 row(['Haiti','Empire of Haiti'],'HTI','Haití · poderes del norte y del sur',a=1807,note='La geometría agregada no separa reino septentrional y república meridional. Las autoridades no gobiernan uniformemente toda la isla.')
 return d
if __name__=='__main__':
 d=prepare(read('historical-1820-entities.json'),read('identities.json'));(OUT/'historical-1800-entities.json').write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n');print('Prepared',len(d['records']),'dated identity rules')
