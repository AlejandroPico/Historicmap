"""Bounded corrections after the 1990–2026 cartographic coverage audit."""
import importlib.util, pathlib, json, re, hashlib, urllib.parse, urllib.request, html, sys, time
spec=importlib.util.spec_from_file_location('historical',pathlib.Path(__file__).with_name('enrich-historical-authorities.py'));h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
data=json.loads((h.OUT/'data/identities.json').read_text(encoding='utf8'));countries=data['countries'];manifest=json.loads((h.OUT/'media/manifest.json').read_text(encoding='utf8'));media={m['file']:m for m in manifest['entries']}
for c in countries.values():c['leaders']=[l for l in c['leaders'] if l.get('acquisition')!='manual-historical-0.6']
terms=[
 ('BRN','Q57327','Hassanal Bolkiah','Sultán · jefatura del Estado','1967-10-05',h.TODAY,'https://www.mof.gov.bn/minister-of-finance/'),
 ('BRN','Q57327','Hassanal Bolkiah','Primer ministro · jefatura del Gobierno','1984-01-01',h.TODAY,'https://www.pmo.gov.bn/prime-minister/'),
 ('PRY','Q440837','Andrés Rodríguez','Presidente de la República','1989-02-03','1993-08-15','https://www.wikidata.org/wiki/Q440837'),
 ('PRY','Q376549','Juan Carlos Wasmosy','Presidente de la República','1993-08-15','1998-08-15','https://www.wikidata.org/wiki/Q376549'),
 ('PRY','Q460003','Raúl Cubas Grau','Presidente de la República','1998-08-15','1999-03-28','https://www.wikidata.org/wiki/Q460003'),
 ('AFG','Q43944','Hamid Karzai','Presidente de la Administración Interina','2001-12-22','2002-06-13','https://2001-2009.state.gov/p/sca/rls/6675.htm'),
 ('AFG','Q43944','Hamid Karzai','Presidente de la Administración Transitoria','2002-06-13','2004-12-07','https://www.wikidata.org/wiki/Q43944'),
 ('AFG','Q43944','Hamid Karzai','Presidente de la República Islámica','2004-12-07','2014-09-29','https://www.gov.uk/government/news/foreign-secretary-welcomes-inauguration-of-new-president-of-afghanistan'),
 ('ZAF','Q151813','Frederik de Klerk','Presidente del Estado · jefaturas del Estado y del Gobierno','1989-09-20','1994-05-10','https://www.presidency.gov.za/history'),
 ('CHN','Q16597','Jiang Zemin','Secretario General del Partido Comunista de China','1989-06-24','2002-11-15','https://english.www.gov.cn/news/topnews/202212/02/content_WS6389d626c6d0a757729e3f58.html'),
 ('CHN','Q15029','Hu Jintao','Secretario General del Partido Comunista de China','2002-11-15','2012-11-15','https://www.wikidata.org/wiki/Q15029'),
 ('CHN','Q15031','Xi Jinping','Secretario General del Partido Comunista de China','2012-11-15',h.TODAY,'https://www.wikidata.org/wiki/Q15031'),
 ('COG','Q57418','Denis Sassou-Nguesso','Presidente · primera etapa','1979-01-01','1992-08-31','https://ambacongogabon.wordpress.com/chronologie-des-presidents-du-congo/'),
 ('COG','Q521920','André Milongo','Primer ministro de transición','1991-01-01','1992-12-31','https://documents1.worldbank.org/curated/en/925951511187348004/pdf/multi0page.pdf'),
 ('AFG','Q188667','Burhanuddin Rabbani','Presidente del Estado Islámico · Gobierno reconocido internacionalmente','1992-06-28','2001-12-22','https://www.wikidata.org/wiki/Q188667'),
 ('AFG','Q317797','Gulbudin Hekmatiar','Primer ministro del Estado Islámico','1993-01-01','1994-12-31','https://publications.gc.ca/collections/collection_2016/grc-rcmp/PS64-129-2016-eng.pdf'),
 ('TJK','Q57366','Emomali Rahmon','Presidente del Consejo Supremo · jefatura del Estado','1992-11-19','1994-11-15','https://www.mfa.tj/en/main/view/2422/the-founder-of-peace-and-national-unity-leader-of-the-nation-president-of-the-republic-of-tajikistan'),
 ('TJK','Q57366','Emomali Rahmon','Presidente de la República','1994-11-16',h.TODAY,'https://mfa.tj/tg/main/view/1808/ruzi-prezidenti-jumhurii-tojikiston'),
 ('PAN','Q887699','Ernesto Pérez Balladares','Presidente · jefaturas del Estado y del Gobierno','1994-09-01','1999-09-01','https://libros.ined.ac.pa/index.php/eined/catalog/download/3/3/22'),
 ('LBY','Q19878','Muamar el Gadafi','Dirigente de facto · Guía de la Revolución','1969-09-01','2011-08-23','https://www.wikidata.org/wiki/Q19878'),
 ('LBY','Q147036','Zentani Muhammad az-Zentani','Secretario General del Congreso General del Pueblo · jefatura formal del Estado','1992-01-01','2008-03-03','https://www.wikidata.org/wiki/Q147036')]
for key,q,name,role,start,end,source in terms:countries[key]['leaders'].append(dict(person=q,name=name,role=role,start=start,end=end,source=source,precision=11,curated=True,acquisition='manual-historical-0.6'))
for country in countries.values():
    for l in country['leaders']:
        if l.get('acquisition')!='manual-historical-0.6':continue
        if l['person']=='Q57418' and l['start']<'1990':l['precision']=9;l['note']='Primera etapa presidencial documentada en la cronología diplomática del Congo; inicio consignado con precisión anual.'
        if l['person'] in ['Q521920','Q317797']:
            l['precision']=9;l['note']='Mandato acreditado aquí con precisión anual. Los extremos de calendario representan años con ejercicio del cargo, no días exactos de nombramiento o cese ni presencia durante todo el año.'
        if l['person']=='Q188667':l['note']='Desde la caída de Kabul en 1996, Gobierno reconocido internacionalmente con control territorial variable y fuerzas de la Alianza del Norte. No gobernaba toda la superficie de Afganistán; se muestran también las autoridades talibanes.'
        if l['person']=='Q19878':l['note']='Autoridad de facto. El final del 23 de agosto de 2011 corresponde a la caída del centro de poder en Trípoli, no a su muerte en octubre. La jefatura formal del Estado se registra por separado.'
        if l['person']=='Q147036':l['precision']=9;l['note']='Inicio consignado con precisión anual: la afirmación P39 utiliza enero de 1992, mientras otras cronologías sitúan el nombramiento en noviembre. No se acredita aquí un día exacto de inicio.'
# Some cached query rows provided a valid picture but a bare QID label. Such
# records are intentionally hidden in the UI, so repair the label from the
# actual entity instead of mistaking it for an absent mandate.
unknown={l['person'] for c in countries.values() for l in c['leaders'] if re.fullmatch(r'Q\d+',l['name']) and l['end']>=h.START}
portraits={l['person']:l['portrait'] for c in countries.values() for l in c['leaders'] if l.get('portrait')};targets=unknown|{t[1] for t in terms}
people={q:e for q,e in h.parallel(h.entity,sorted(targets)) if e}
for q in {t[1] for t in terms}:
    if not any(isinstance(v,dict) and v.get('id')=='Q5' for v in h.values(people.get(q,{}),'P31')):raise ValueError('Curated authority must be a verified human entity: '+q)
for q,e in people.items():
    if q in portraits:continue
    photos=h.values(e,'P18')
    if not photos:continue
    filename=photos[0];digest=hashlib.sha256(filename.encode()).hexdigest()[:20]
    try:
        params=dict(action='query',titles='File:'+filename,redirects=1,prop='imageinfo',iiprop='url|extmetadata',iiurlwidth=320,format='json');info=h.get('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params),'commons-'+digest);page=next(iter(info.get('query',{}).get('pages',{}).values()),{});ii=page.get('imageinfo',[{}])[0];meta=ii.get('extmetadata',{});lic=meta.get('LicenseShortName',{}).get('value','');url=(ii.get('thumburl') or ii.get('url') or '').split('?')[0]
        accepted=any(v in lic.lower() for v in ['public domain','cc0','cc by','cc-by','pd-']) or lic in ['Attribution','OGL 3','OGL v1.0','GODL-India','European Parliament','KOGL Type 1','PDM-owner']
        if not url or not accepted or 'nd' in lic.lower() or filename.lower().endswith('.svg'):continue
        ext='.png' if '.png' in url.lower() else '.jpg';relative='media/portrait-'+digest+ext;dest=h.OUT/relative
        if not dest.exists():
            if '--reuse-media-only' in sys.argv:continue
            if '--bounded-media' in sys.argv:
                with urllib.request.urlopen(urllib.request.Request(url,headers=h.UA),timeout=20) as response:raw=response.read()
                time.sleep(1.2)
            else:raw=h.download(url)
            if not raw.startswith((b'\xff\xd8',b'\x89PNG')) or len(raw)>5_000_000:continue
            dest.write_bytes(raw)
        clean=lambda v:html.unescape(re.sub('<[^>]*>','',v));m=dict(file=relative,title=filename,url=ii.get('descriptionurl',''),artist=clean(meta.get('Artist',{}).get('value','')),license=lic,licenseUrl=meta.get('LicenseUrl',{}).get('value',''),attribution=clean(meta.get('Attribution',{}).get('value','')),attributionRequired=meta.get('AttributionRequired',{}).get('value')=='true',credit=clean(meta.get('Credit',{}).get('value','')),sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),bytes=dest.stat().st_size,sourceUrl=url);media[relative]=m;portraits[q]=m
    except Exception as error:print('Curated portrait unavailable',q,str(error)[:100],flush=True)
repaired=0
for country in countries.values():
    for l in country['leaders']:
        if l['person'] in people and re.fullmatch(r'Q\d+',l['name']):l['name']=h.label(people[l['person']]);repaired+=1
        if l['person'] in portraits:l['portrait']=portraits[l['person']]
    country['leaders'].sort(key=lambda l:(l['start'],l['name'],l['role']))
h.save(h.OUT/'data/identities.json',data);manifest['entries']=sorted(media.values(),key=lambda m:m['file']);h.save(h.OUT/'media/manifest.json',manifest)
print('Focal terms',len(terms),'bare QID labels repaired',repaired,'licensed media',len(media),flush=True)
