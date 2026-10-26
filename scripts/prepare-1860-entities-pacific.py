import json,pathlib,subprocess,sys,hashlib,importlib.util
root=pathlib.Path(__file__).resolve().parents[1]; out=root/'public/data'
read=lambda p:json.loads(pathlib.Path(p).read_text(encoding='utf8'))
def save(p,d):pathlib.Path(p).write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
# The same resolver accepts an independently bounded earlier catalogue.
cat=read(out/'historical-1880-entities.json');cat['coverageStart']=1860;cat['coverageEnd']=1879;cat['referenceDate']='2026-10-26'
cat['records']=[dict(r,start=1860,end=1879) for r in cat['records'] if r['start']==1880 and r['end']==1899 and r['key'] not in ['DEU','ITA','FRA','ESP','JPN','AUT-HUN','ZUL']]
cat['qidKeys'].update(Q27306='PRUSSIA',Q131964='AUSTRIAN-EMPIRE',Q371334='MEX-EMPIRE',Q150981='NGC',Q165154='SAR',Q81931='CSA')
ids=read(out/'identities.json')['countries'];cat['names'].update({k:c['name'] for k,c in ids.items()})
for key,c in ids.items():
 if c.get('qid'):cat['qidKeys'].setdefault(c['qid'],key)
def rule(names,key,label,a,b):
 cat['records'].append(dict(names=names,key=key,label=label,entityCode=key,admin='',status='independent',start=a,end=b,source='https://www.wikidata.org/wiki/'+ids.get(key,{}).get('qid','Q142'),note='Identidad editorial fechada; el contorno de la fuente permanece intacto y no certifica las fases mensuales del año.'))
rule(['Second French Empire','France','French Third Republic'],'FRA','Segundo Imperio francés',1860,1869)
rule(['Second French Empire','France','French Third Republic'],'FRA','República Francesa',1870,1879)
rule(['Kingdom of Sardinia'],'SAR','Reino de Cerdeña',1860,1860)
rule(['Kingdom of Italy'],'ITA','Reino de Italia',1861,1879)
rule(['Kingdom of Prussia'],'PRUSSIA','Reino de Prusia',1860,1879)
rule(['Austrian Empire'],'AUSTRIAN-EMPIRE','Imperio austríaco',1860,1866)
rule(['Austria-Hungary'],'AUT-HUN','Austria-Hungría',1867,1879)
rule(['German Empire'],'DEU','Imperio alemán',1871,1879)
rule(['Tokugawa Shogunate'],'JPN','Shogunato Tokugawa',1860,1867)
rule(['Empire of Japan','Japan'],'JPN','Imperio del Japón',1868,1879)
rule(['Kingdom of Spain','Spanish Empire'],'ESP','Monarquía española · Isabel II',1860,1867)
rule(['Kingdom of Spain','Spanish Empire'],'ESP','España · Gobierno provisional',1868,1870)
rule(['Kingdom of Spain','Spanish Empire'],'ESP','Monarquía española · Amadeo I',1871,1872)
rule(['First Spanish Republic','Spanish Empire'],'ESP','Primera República española',1873,1873)
rule(['First Spanish Republic','Kingdom of Spain','Spanish Empire'],'ESP','España · transición y Restauración',1874,1874)
rule(['First Spanish Republic','Kingdom of Spain','Spanish Empire'],'ESP','Monarquía española · Alfonso XII',1875,1879)
for r in cat['records']:
 if r['key']=='BGR':r['start']=1878
 if r['key']=='HIST-Q1852345':r['status']='protected-treaty';r['note']='Estados de la Tregua: acuerdos marítimos históricos; el compromiso de1892 de no ceder territorio sin consentimiento británico aún no existía en esta ventana. No equivalen a anexión.'
 r['note']=r.get('note','').replace('en1880','en esta ventana').replace('a1880','a esta ventana')
rule(['Zululand'],'ZUL','Reino zulú',1860,1879)
save(out/'historical-1860-entities.json',cat)
# Component index: source coordinates remain in the original file, never duplicate land.
index=read(out/'pacific-components.json')['records'] if (out/'pacific-components.json').exists() else read(root/'.cache/pacific-014-clio-component-index.json')
save(out/'pacific-components.json',dict(format='source-component-index',referenceDate='2026-10-26',records=index))
# Contemporary contours are explicitly reference land, not reconstructed historical coasts.
ne=read(out/'countries.geojson');by={f['properties']['code']:f for f in ne['features']}
features=[]
doi='https://www.doi.gov/oia/islands/'
def phase(code,a,b,admin,label,source,head=False):
 f=json.loads(json.dumps(by[code]));name=f['properties']['name'];p=dict(name=name,originalName=name,identityKey=code,entityCode=code,code='',start=f'{a}-01-01',end=f'{b}-12-31',status='dependency' if admin else 'source-reference',politicalStatus=label,territorialReference=True,geometrySource='https://www.naturalearthdata.com/',geometrySourceLabel='Natural Earth 1:10m · contorno contemporáneo de referencia',referenceYear=2026,source=source,note=label+'. Contorno contemporáneo para hacer seleccionable la isla omitida en el inventario histórico; no acredita límites, anexión de todos los islotes ni una administración uniforme durante cada transición anual.')
 if admin:p.update(administratorKey=admin,localAuthorityKey=code,ownerName=ids.get(admin,{}).get('name',admin),headOfStateOnly=head)
 if 'independiente' in label:p['status']='independent';p['code']=code
 elif 'autogobierno en libre asociación' in label:p['status']='self-governing'
 f.update(id=f'pacific-{code}-{a}',properties=p);features.append(f)
for code,phases,source in [
 ('GUM',[(1886,1897,'ESP','Guam bajo administración española'),(1898,1940,'USA','Guam bajo administración estadounidense; transferencia de 1898'),(1941,1943,'JPN','Guam bajo ocupación japonesa desde diciembre de 1941'),(1944,2019,'USA','Guam bajo administración estadounidense tras la recuperación de 1944')],doi+'guam'),
 ('MNP',[(1886,1898,'ESP','Marianas septentrionales bajo España'),(1899,1913,'DEU','Marianas septentrionales bajo Alemania'),(1914,1943,'JPN','Marianas septentrionales bajo Japón'),(1944,2019,'USA','Administración estadounidense; Commonwealth desde 1978')],doi+'cnmi'),
 ('PLW',[(1860,1884,'','Palaos: poderes locales y reclamaciones externas; autoridad uniforme no documentada'),(1886,1898,'ESP','Palaos bajo España'),(1899,1913,'DEU','Palaos bajo Alemania'),(1914,1943,'JPN','Palaos bajo Japón'),(1944,1993,'USA','Palaos bajo administración estadounidense'),(1994,2019,'','Palaos independiente desde el 1 de octubre de 1994')],'https://history.state.gov/countries/palau'),
 ('FSM',[(1860,1885,'','Islas Carolinas: autoridades locales; soberanía uniforme no documentada'),(1886,1898,'ESP','Carolinas bajo España'),(1899,1913,'DEU','Carolinas bajo Alemania'),(1914,1943,'JPN','Carolinas bajo Japón'),(1944,1985,'USA','Territorio en fideicomiso administrado por Estados Unidos'),(1986,2019,'','Estados Federados de Micronesia: libre asociación desde noviembre de 1986')],'https://history.state.gov/countries/micronesia'),
 ('MHL',[(1860,1884,'','Islas Marshall: autoridades locales'),(1885,1913,'DEU','Islas Marshall bajo Alemania'),(1914,1943,'JPN','Islas Marshall bajo Japón'),(1944,1985,'USA','Fideicomiso administrado por Estados Unidos'),(1986,2019,'','Islas Marshall: libre asociación desde el 21 de octubre de 1986')],'https://history.state.gov/countries/marshall-islands'),
 ('ASM',[(1860,1899,'','Samoa oriental: autoridades samoanas'),(1900,2019,'USA','Samoa Americana: cesión de Tutuila en 1900; Manuʻa en 1904')],doi+'american-samoa'),
 ('COK',[(1860,1887,'','Islas Cook: autoridades insulares'),(1888,1900,'GBR','Islas Cook: protectorado británico'),(1901,1964,'NZL','Islas Cook bajo administración neozelandesa'),(1965,2019,'','Islas Cook: autogobierno en libre asociación')],'https://teara.govt.nz/en/pacific-islands-and-new-zealand/print'),
 ('NIU',[(1860,1899,'','Niue: autoridades locales'),(1900,1900,'GBR','Niue: protectorado británico'),(1901,1973,'NZL','Niue bajo administración neozelandesa'),(1974,2019,'','Niue: autogobierno en libre asociación')],'https://collections.tepapa.govt.nz/topic/10657'),
 ('WSM',[(1860,1899,'','Samoa: autoridades y rivalidades locales; no frontera colonial retrospectiva'),(1900,1913,'DEU','Samoa occidental bajo Alemania'),(1914,1961,'NZL','Samoa occidental bajo administración neozelandesa'),(1962,2019,'','Samoa independiente desde 1962')],'https://www.archives.govt.nz/discover-our-stories/the-rise-of-the-mau-and-the-fall-of-colonial-rule-in-samoa'),
 ('PYF',[(1860,1900,'','Archipiélagos polinesios: incorporaciones francesas graduales; sin administrador único acreditado'),(1901,1903,'FRA','Establecimientos franceses de Oceanía')],'https://www.polynesie-francaise.pref.gouv.fr/'),
 ('WLF',[(1860,1886,'','Wallis y Futuna: autoridades insulares'),(1887,2019,'FRA','Wallis y Futuna bajo protección y administración francesa')],'https://www.outre-mer.gouv.fr/'),
 ('PCN',[(1860,1886,'','Pitcairn: constitución local de 1838; referencia del archipiélago actual'),(1887,2019,'GBR','Pitcairn: asentamiento británico; incorporación de islas exteriores posterior')],'https://www.government.pn/history'),
 ('KIR',[(1860,1891,'','Islas Gilbert y archipiélagos: autoridades insulares'),(1892,1978,'GBR','Protectorado y colonia británicos; islas incorporadas en distintas fechas'),(1979,2019,'','Kiribati independiente desde 1979')],'https://thecommonwealth.org/our-member-countries/kiribati/history'),
 ('TUV',[(1860,1891,'','Islas Ellice: autoridades insulares'),(1892,1977,'GBR','Protectorado y colonia británicos'),(1978,2019,'','Tuvalu independiente desde 1978')],'https://thecommonwealth.org/our-member-countries/tuvalu/history'),
 ('NRU',[(1860,1887,'','Nauru: autoridades insulares'),(1888,1913,'DEU','Nauru bajo Alemania'),(1914,1941,'','Nauru: administración australiana y mandato conjunto británico, australiano y neozelandés'),(1942,1945,'JPN','Nauru bajo ocupación japonesa; final en 1945'),(1946,1967,'','Nauru: fideicomiso conjunto administrado por Australia'),(1968,2019,'','Nauru independiente desde 1968')],'https://thecommonwealth.org/our-member-countries/nauru/history'),
 ('VUT',[(1860,1905,'','Nuevas Hébridas: autoridades locales y rivalidades coloniales'),(1906,1979,'','Nuevas Hébridas: condominio conjunto franco-británico'),(1980,2019,'','Vanuatu independiente desde 1980')],'https://thecommonwealth.org/our-member-countries/vanuatu/history'),
 ('FJI',[(1860,1870,'','Fiyi: jefaturas y poderes locales; no reino unitario retrospectivo')],'https://thecommonwealth.org/our-member-countries/fiji/history'),
 ]:
 for a,b,admin,label in phases:phase(code,a,b,admin,label,source)
save(out/'pacific-references.geojson',dict(type='FeatureCollection',features=features))
print('Prepared early identities',len(cat['records']),'Pacific phases',len(features),'source components',len(index))
