"""Acquire reviewed, dated symbols with original provenance and explicit type.

Search results alone are never adopted. Unverified Wadai, medieval Bornu and
the unsourced uniform Sokoto flag are recorded as unresolved, not backdated.
"""
import pathlib,json,importlib.util,urllib.parse,hashlib,html,re,copy
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('h',ROOT/'scripts/enrich-1970-authorities.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
TAG='symbols-review-0.18'
ROWS=[
 ('HABSBURG-MONARCHY','Flag of the Habsburg Monarchy.svg','1800-01-01','1804-08-10','Colores dinásticos','Símbolo de los dominios de los Habsburgo; no bandera nacional moderna.'),
 ('HIST-Q12548','Banner of the Holy Roman Emperor without haloes (1400-1806).svg','1800-01-01','1806-08-06','Estandarte imperial','Estandarte del emperador; no elimina las identidades de sus Estados miembros.'),
 ('HIST-Q206696','Flag of the Helvetic Republic (French).svg','1798-04-12','1803-03-10','Bandera de la República Helvética','Tricolor republicano; no se prolonga después del Acta de Mediación.'),
 ('HIST-Q10957559','Flag of Principality of Moldavia before 1834.jpg','1800-01-01','1833-12-31','Reconstrucción de pabellón','Reconstrucción moderna atribuida a Norie y Hobbs1848. No acredita un diseño nacional uniforme ni fecha de adopción exacta.'),
 ('HIST-Q10957559','Civil Ensign of the Principality of Moldavia (1834-1861).jpg','1834-12-31','1858-12-31','Pabellón mercante','Pabellón marítimo; no se identifica con todos los estandartes principescos o militares.'),
 ('HIST-Q171393','Flag of Wallachia 1834.svg','1834-12-31','1858-12-31','Pabellón histórico','Referencia posterior a1834; se rechaza la candidata anterior marcada como ficticia.'),
 ('OTT','Flag of the Ottoman Empire (also used in Egypt).svg','1800-01-01','1843-12-31','Pabellón otomano','Variante de creciente y estrella anterior a la normalización de1844; no una norma digital uniforme.'),
 ('PAPAL-STATES','Flag of the Papal States (pre 1808).svg','1800-01-01','1807-12-31','Pabellón pontificio','Variante roja y amarilla anterior a1808.'),
 ('PAPAL-STATES','Flag of the Papal States (1808-1870).svg','1808-12-31','1824-12-31','Colores pontificios','Referencia amarilla y blanca; diseños de armas y pabellones distinguidos en variantes posteriores.'),
 ('HIST-Q199821','Flag of Gran Colombia (1819–1820).svg','1819-12-31','1820-12-31','Bandera histórica','Variante inicial de la unión; no se prolonga sobre las repúblicas sucesoras.'),
 ('HIST-Q199821','Flag of Gran Colombia.svg','1821-10-06','1830-12-31','Pabellón histórico','Variante con escudo; la referencia material del Batallón Húsares del Centro, ca1824, es un ejemplar militar.'),
 ('PER','Flag of Peru (1822–1825).svg','1822-05-31','1825-02-24','Bandera histórica','Variante vertical con sol anterior al diseño de1825.'),
 ('RIO-DE-LA-PLATA','Flag of Argentina (1818–1819, 1820–1829, 1861–2010).svg','1820-01-01','1829-12-31','Pabellón rioplatense','No implica existencia de una presidencia nacional en1820–1825.'),
 ('HIST-Q14551680','Flag of Lippe (1815-1880).svg','1815-12-31','1879-12-31','Bandera histórica','Referencia conservadora anterior al cambio aproximado de1880.'),
 ('HIST-Q14551680','Flagge Fürstentum Lippe.svg','1881-01-01','1900-12-31','Bandera histórica','Variante posterior al cambio aproximado de1880.'),
 ('HIST-Q836680','Flagge Herzogtum Nassau (1806-1866).svg','1806-12-31','1866-09-20','Bandera histórica','Ducado de Nassau, no la ciudad ni el condado estadounidense homónimos.'),
 ('HIST-Q20135','Flagge Großherzogtum Hessen ohne Wappen.svg','1807-01-01','1900-12-31','Bandera histórica','Variante sin armas del gran ducado; ventana interior de la entidad de1806.'),
 ('HIST-Q186320','Flag of the Grand Duchy of Baden (1855–1891).svg','1855-12-31','1890-12-31','Bandera histórica','Variante1855–1891; no se retrotrae al electorado.'),
 ('HIST-Q3462133','Flagge Herzogtum Sachsen-Coburg-Gotha (1826-1911).svg','1826-12-31','1900-12-31','Bandera histórica','Ducado formado en1826; no el electorado sajón.'),
 ('HIST-Q155570','Flagge Großherzogtum Sachsen-Weimar-Eisenach (1813-1897).svg','1815-12-31','1896-12-31','Bandera histórica','Ventana conservadora del gran ducado desde1815.'),
 ('HIST-Q159631','Flag of the Kingdom of Württemberg (1806 - 1816).png','1806-12-31','1815-12-31','Pabellón real','Se conserva la reproducción raster documentada; rechazada la vectorización con aviso de calidad pendiente.'),
 ('HIST-Q159631','Flagge Königreich Württemberg.svg','1817-01-01','1900-12-31','Bandera histórica','Colores negro y rojo posteriores a1816.'),
 ('HIST-Q153015','State flag of Saxony before 1815.svg','1800-01-01','1815-06-16','Pabellón estatal','Electorado y reino de Sajonia antes del cambio de1815.'),
 ('HIST-Q153015','Flagge Königreich Sachsen (1815-1918).svg','1815-06-17','1900-12-31','Bandera histórica','Colores blanco y verde de Sajonia.'),
 ('HIST-Q164079','Flag of Hanover 1837-1866.svg','1837-12-31','1866-09-20','Pabellón del reino','Variante posterior al fin de la unión personal británica.'),
 ('HIST-Q708821','Flag of Schwarzburg Sondershausen.svg','1800-01-01','1900-12-31','Colores principescos','Referencia de los colores de la casa; no fecha exacta de normalización del diseño.'),
 ('NAPLES-BOURBON','Flag of Kingdom of Naples (1759-1806; 1815-1816).png','1800-01-01','1805-12-31','Pabellón real','Reproducción del pabellón borbónico con armas de Fernando IV; distinta de la bandera angevina medieval.'),
 ('NAPLES-BOURBON','Flag of Kingdom of Naples (1759-1806; 1815-1816).png','1815-12-31','1816-12-11','Pabellón real','Restauración borbónica anterior a la constitución formal de las Dos Sicilias.'),
 ('NAPOLEONIC-NAPLES','Flag of Kingdom of Naples (1806-1808).svg','1806-12-31','1807-12-31','Pabellón napoleónico','Primera variante del reino, distinta de las de Murat.'),
 ('NAPOLEONIC-NAPLES','Flag of the Kingdom of Naples (1808).svg','1808-12-31','1810-12-31','Pabellón real','Variante del reino de Joaquín Murat anterior a1811.'),
 ('NAPOLEONIC-NAPLES','Flag of the Kingdom of Naples (1811).svg','1811-12-31','1814-12-31','Pabellón real','Variante de1811; no prolongada sobre la restauración borbónica.'),
 ('HIST-Q207521','Flag of Ethiopia (1897–1974).svg','1897-12-31','1900-12-31','Pabellón imperial','León de Judá sobre el tricolor; no retrotraído al principio del sigloXIX.'),
 ('HIST-Q887803','Old Flag of Brunei.svg','1850-01-01','1900-12-31','Pabellón del sultanato','Campo amarillo anterior a1906. Ventana interior, no una fecha de adopción acreditada.'),
 ('HIST-Q1658411','Flag of Sarawak (1870–1946, 1963–1973).svg','1870-12-31','1900-12-31','Pabellón del rajá','Variante posterior a1870, no proyectada al principio del gobierno Brooke.'),
 ('HIST-Q62589','Jack of Sweden and Norway (1844–1905).svg','1844-12-31','1900-12-31','Pabellón diplomático de la unión','También torrotito naval; Suecia y Noruega conservan pabellones nacionales propios.'),
 ('HIST-Q1077630','Flag of the Septinsular Republic.svg','1800-12-31','1806-12-31','Pabellón de la república','República de las Siete Islas; no la posterior administración británica.'),
 ('HIST-Q223793','Etrurian Kingdom and War Flag with lesser coat of arms.svg','1801-12-31','1806-12-31','Pabellón del reino y de guerra','Variante con armas menores del Reino de Etruria.'),
 ('HIST-Q698089','Flag of the Grandduchy of Wurzburg.svg','1806-12-31','1813-12-31','Pabellón del gran ducado','Ventana interior de la entidad; no bandera municipal contemporánea.'),
 ('HIST-Q153943','Flag of Kingdom of Westphalia.svg','1807-12-31','1812-12-31','Bandera del reino','Reproducción que remite al archivo municipal de Braunschweig; no implica anexión a Francia.'),
 ('HIST-Q706018','Flag of Hanover (1692).svg','1800-01-01','1802-12-31','Estandarte del electorado','Caballo sajón del electorado; no el pabellón marítimo del reino posterior.'),
 ('PRUSSIA','Flag of the Kingdom of Prussia (1750-1801).svg','1800-01-01','1800-12-31','Pabellón histórico','Variante anterior a1801; no anticipa el diseño de1803.'),
 ('SAR','Merchant Flag of the Kingdom of Sardinia (c.1799-1802).svg','1800-01-01','1801-12-31','Pabellón mercante','Referencia aproximada de1799–1802; no estandarte personal del rey.'),
 ('PRT','Flag of Portugal (1707).svg','1800-01-01','1815-12-31','Pabellón de la monarquía','Variante anterior al Reino Unido de Portugal, Brasil y Algarves.'),
 ('MAR','Flag of Morocco (1666–1915).svg','1800-01-01','1900-12-31','Pabellón dinástico','Campo rojo anterior al pentagrama verde de1915.'),
 ('HIST-Q208169','Civil and merchant flag of the Republic of Ragusa (c. 1667-1807).svg','1800-01-01','1806-12-31','Pabellón civil y mercante','Referencia marítima de la república anterior a su disolución.'),
 ('HIST-Q188553','Flag of the navy of the Batavian Republic.svg','1800-01-01','1805-12-31','Pabellón naval','Variante naval de la República Bátava, distinta del simple tricolor civil.'),
 ('BRN','Old Flag of Brunei.svg','1800-01-01','1900-12-31','Colores del sultanato','Campo amarillo tradicional anterior a1906; no fecha exacta de adopción acreditada.'),
]
PENDING=[
 dict(key='HIST-Q1132786',candidate='Wadai.png',reason='Diseño subido como obra propia, sin testimonio histórico independiente que acredite su uso1800–1900. No se copia la bandera de Darfur.'),
 dict(key='HIST-Q1139762',candidate='Flag of the Bornu Empire.svg',reason='La descripción remite al atlas deVallseca1439; no demuestra continuidad del símbolo hasta el sigloXIX.'),
 dict(key='HIST-Q600524',candidate='Flag of the Sokoto Caliphate.svg',reason='Aviso Lacking insignia source. Los estandartes militares verdes documentados no prueban una bandera nacional uniforme; falta una reproducción acreditada.'),
 dict(key='HIST-Q171393',candidate='Flag of Principality of Wallachia before1834.jpg',reason='Candidata marcada ficticia; no incorporada.'),
]

def main():
 data=json.loads((ROOT/'public/data/identities.json').read_text(encoding='utf8'));manifest=json.loads((ROOT/'public/media/manifest.json').read_text(encoding='utf8'));media={m['file']:m for m in manifest['entries']};by_title={m['title']:m for m in media.values()}
 pages={p['title']:p for p in json.loads((ROOT/'.cache/symbols018-pages.json').read_text(encoding='utf8'))};missing=[t for _,t,*_ in ROWS if 'File:'+t not in pages and t not in by_title]
 for start in range(0,len(missing),15):
  group=missing[start:start+15];params=dict(action='query',titles='|'.join('File:'+t for t in group),redirects=1,prop='imageinfo|revisions',rvprop='content|ids',rvslots='main',iiprop='url|extmetadata',format='json')
  result=h.get('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params),'symbols018-extra-'+hashlib.sha256('|'.join(group).encode()).hexdigest()[:16]);pages.update({p['title']:p for p in result.get('query',{}).get('pages',{}).values()})
 for c in data['countries'].values():c['flags']=[f for f in c['flags'] if f.get('acquisition')!=TAG]
 pending=copy.deepcopy(PENDING);accepted=[]
 for key,title,a,b,label,note in ROWS:
  try:
   m=by_title.get(title)
   if not m:
    page=pages.get('File:'+title,{});ii=page.get('imageinfo',[{}])[0];meta=ii.get('extmetadata',{});lic=meta.get('LicenseShortName',{}).get('value','');wiki=page.get('revisions',[{}])[0].get('slots',{}).get('main',{}).get('*','')
    if not ii.get('url') or re.search(r'\{\{\s*(Fictitious|Fictional|Fact disputed|Disputed|Inaccurate|Lacking insignia source)\b|Please do not use until',wiki,re.I):raise ValueError('Absent, unverified or disputed design')
    reviewed_attribution=title=='Flag of the Kingdom of Prussia (1750-1801).svg' and lic=='Attribution' and '{{Attribution|User:David Liuzzo|David Liuzzo}}' in wiki
    if not any(x in lic.lower() for x in ['public domain','cc0','cc by','cc-by']) and not reviewed_attribution:raise ValueError('Unverified licence '+lic)
    url=ii['url'];raw=h.download(url,max_bytes=5000000);ext='.svg' if title.lower().endswith('.svg') else '.jpg' if raw.startswith(b'\xff\xd8') else '.png' if raw.startswith(b'\x89PNG') else None
    if not ext or ext=='.svg' and (b'<svg' not in raw or re.search(rb'<script|javascript:|\bonload\s*=',raw,re.I)):raise ValueError('Invalid image bytes')
    file='media/flag-'+hashlib.sha256(title.encode()).hexdigest()[:20]+ext;(ROOT/'public'/file).write_bytes(raw)
    clean=lambda k:html.unescape(re.sub('<[^>]*>','',meta.get(k,{}).get('value','')))
    m=dict(file=file,title=title,url=ii['descriptionurl'],sourceUrl=url,artist=clean('Artist'),license=lic,licenseUrl=clean('LicenseUrl') or ii['descriptionurl']+'#Licensing',credit=clean('Credit'),attribution=clean('Attribution'),attributionRequired=True,sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw));media[file]=m;by_title[title]=m
   display={**m,'symbolLabel':label,'presentationNote':note}
   evidence='https://icom.museum/es/object/bandera-de-la-gran-colombia-del-batallon-de-husares-del-centro-ca-1824-73-x-78-cm/' if key=='HIST-Q199821' and a.startswith('1821') else m['url']
   display['symbolEvidenceURL']=evidence
   data['countries'][key]['flags'].append(dict(start=a,end=b,media=display,source=evidence,note=note,acquisition=TAG));accepted.append(dict(key=key,title=title,start=a,end=b,label=label,source=evidence,note=note));print('Symbol',key,title,flush=True)
  except Exception as e:pending.append(dict(key=key,title=title,reason=str(e)));print('Pending',key,title,str(e),flush=True)
 manifest['entries']=sorted(media.values(),key=lambda m:m['file']);h.save(ROOT/'public/data/identities.json',data);h.save(ROOT/'public/media/manifest.json',manifest);h.save(ROOT/'scripts/review-018-symbols.json',dict(accepted=accepted,pending=pending));print('Reviewed symbols',len(accepted),'pending',len(pending),flush=True)
if __name__=='__main__':main()
