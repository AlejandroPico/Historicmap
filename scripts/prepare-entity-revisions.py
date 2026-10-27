"""Compile dated, entity-owned corrections. No historical facts live in this writer.

Canonical input: Países/<entity>/revision-historica.json and simbolos/.
Public identities/media are generated runtime copies. Network access is opt-in.
"""
import argparse, copy, hashlib, html, importlib.util, json, pathlib, re, urllib.parse
ROOT = pathlib.Path(__file__).resolve().parents[1]
TAG = 'entity-review-0.26.1'
read = lambda p: json.loads(p.read_text(encoding='utf8'))
def save(p, value):
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf8', newline='\n')
def save_data(p, value):
    p.write_text(json.dumps(value, ensure_ascii=False, separators=(',',':'))+'\n', encoding='utf8', newline='\n')

def main(acquire=False):
    spec=importlib.util.spec_from_file_location('acquisition',ROOT/'scripts/enrich-1970-authorities.py')
    api=importlib.util.module_from_spec(spec);spec.loader.exec_module(api)
    identities=read(ROOT/'public/data/identities.json')
    media_manifest=read(ROOT/'public/media/manifest.json');media={m['file']:m for m in media_manifest['entries']}
    by_title={m['title']:m for m in media.values()}
    portraits={l['person']:l['portrait'] for c in identities['countries'].values() for l in c['leaders'] if l.get('portrait')}
    history=read(ROOT/'public/data/country-history.json');governance=read(ROOT/'public/data/governance.json')
    history['records']=[r for r in history['records'] if r.get('acquisition')!=TAG]
    governance['records']=[r for r in governance['records'] if r.get('acquisition')!=TAG]
    inputs=sorted((ROOT/'Países').glob('*/revision-historica.json'))
    for path in inputs:
        revision=read(path);key=revision['key'];country=identities['countries'].get(key)
        if not country:raise ValueError('Unknown entity '+key)
        for field in ['flags','leaders','symbolReferences']:
            country[field]=[r for r in country.get(field,[]) if r.get('acquisition')!=TAG]
        for removal in revision.get('replace',[]):
            field=removal['field'];a,b=removal['start'],removal['end']
            # Keep both tails when replacing an interior interval.
            kept=[]
            import datetime
            for old in country.get(field,[]):
                if old['end']<a or old['start']>b:kept.append(old);continue
                if old['start']<a:
                    left=copy.deepcopy(old);left['end']=(datetime.date.fromisoformat(a)-datetime.timedelta(days=1)).isoformat();kept.append(left)
                if old['end']>b:
                    right=copy.deepcopy(old);right['start']=(datetime.date.fromisoformat(b)+datetime.timedelta(days=1)).isoformat();kept.append(right)
            country[field]=kept
        for symbol in revision.get('symbols',[]):
            if any(r['title']==symbol['title'] for r in revision.get('rejectedSymbols',[])):raise ValueError('Explicitly rejected symbol '+symbol['title'])
            title=symbol['title'];m=copy.deepcopy(symbol.get('media') or by_title.get(title))
            if not m:
                if not acquire:raise ValueError('Run --acquire once for '+title)
                params=dict(action='query',titles='File:'+title,redirects=1,prop='imageinfo|revisions',rvprop='content',rvslots='main',iiprop='url|extmetadata',format='json')
                response=api.get('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params),'entity-symbol-'+hashlib.sha256(title.encode()).hexdigest()[:20])
                page=next(iter(response['query']['pages'].values()));ii=page.get('imageinfo',[{}])[0];meta=ii.get('extmetadata',{});wiki=page.get('revisions',[{}])[0].get('slots',{}).get('main',{}).get('*','')
                if re.search(r'\{\{\s*(Fictitious|Fictional|Disputed|Inaccurate|Lacking insignia source)\b',wiki,re.I):raise ValueError('Unverified symbol '+title)
                license=meta.get('LicenseShortName',{}).get('value','')
                if not any(x in license.lower() for x in ['public domain','cc0','cc by','cc-by']):raise ValueError('License '+title+': '+license)
                raw=api.download(ii['url'],max_bytes=5000000)
                ext='.svg' if title.lower().endswith('.svg') else '.jpg' if raw.startswith(b'\xff\xd8') else '.png' if raw.startswith(b'\x89PNG') else None
                if not ext or ext=='.svg' and (b'<svg' not in raw or re.search(rb'<script|javascript:|\bonload\s*=',raw,re.I)):raise ValueError('Invalid media '+title)
                clean=lambda k:html.unescape(re.sub('<[^>]*>','',meta.get(k,{}).get('value','')))
                file='media/flag-'+hashlib.sha256(title.encode()).hexdigest()[:20]+ext
                m=dict(file=file,title=title,url=ii['descriptionurl'],sourceUrl=ii['url'],artist=clean('Artist'),license=license,licenseUrl=clean('LicenseUrl') or ii['descriptionurl']+'#Licensing',credit=clean('Credit'),attribution=clean('Attribution'),attributionRequired=True,sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw))
                (ROOT/'public'/file).write_bytes(raw)
            source_file=path.parent/'simbolos'/pathlib.Path(m['file']).name
            source_file.parent.mkdir(exist_ok=True)
            if not source_file.exists():source_file.write_bytes((ROOT/'public'/m['file']).read_bytes())
            raw=source_file.read_bytes()
            if hashlib.sha256(raw).hexdigest()!=m['sha256']:raise ValueError('Canonical symbol bytes '+str(source_file))
            (ROOT/'public'/m['file']).write_bytes(raw)
            m['canonicalFile']=source_file.relative_to(ROOT).as_posix();media[m['file']]=m;by_title[title]=m
            symbol['media']=m
            display={**m,'symbolLabel':symbol['label'],'presentationNote':symbol['note'],'symbolEvidenceURL':symbol['source']}
            if symbol.get('referenceOnly'):
                display.update(referenceOnly=True,evidenceDate=symbol['evidenceDate'])
            record=dict(start=symbol['start'],end=symbol['end'],media=display,source=symbol['source'],note=symbol['note'],acquisition=TAG)
            if record['start']>record['end']:raise ValueError('Inverted symbol '+key)
            country['symbolReferences' if symbol.get('referenceOnly') else 'flags'].append(record)
        for leader in revision.get('leaders',[]):
            if leader['start']>leader['end'] or not leader.get('source'):raise ValueError('Invalid office '+key)
            # Canonical portraits may be filled on the first acquisition. Keep
            # runtime property order stable on the next offline compilation.
            item={k:v for k,v in leader.items() if k not in ['portrait','curated','acquisition']}
            item.update(curated=True,acquisition=TAG)
            if leader.get('portrait'):item['portrait']=leader['portrait']
            if not item.get('portrait') and item['person'] in portraits:item['portrait']=portraits[item['person']]
            if item.get('portrait'):
                portrait=copy.deepcopy(item['portrait']);local=path.parent/'retratos'/pathlib.Path(portrait['file']).name
                local.parent.mkdir(exist_ok=True)
                if not local.exists():local.write_bytes((ROOT/'public'/portrait['file']).read_bytes())
                if hashlib.sha256(local.read_bytes()).hexdigest()!=portrait['sha256']:raise ValueError('Canonical portrait bytes '+str(local))
                portrait['canonicalFile']=local.relative_to(ROOT).as_posix();item['portrait']=portrait;leader['portrait']=portrait
                media[portrait['file']]={**media[portrait['file']],'canonicalFile':portrait['canonicalFile']}
            country['leaders'].append(item)
        for record in revision.get('institutions',[]):history['records'].append({**record,'keys':[key],'acquisition':TAG})
        for record in revision.get('governance',[]):governance['records'].append({**record,'keys':[key],'acquisition':TAG})
        for fix in revision.get('entityRules',[]):
            for file in fix['files']:
                if not re.fullmatch(r'historical-\d{4}-entities\.json',file):raise ValueError('Invalid resolution file')
                dest=ROOT/'public/data'/file;catalogue=read(dest)
                rules=[r for r in catalogue['records'] if not(r.get('acquisition')==TAG and r['key']==key)]
                record={**fix['record'],'key':key,'entityCode':key,'acquisition':TAG}
                record['start']=max(record['start'],catalogue['coverageStart']);record['end']=min(record['end'],catalogue['coverageEnd'])
                catalogue['records']=[record,*rules];save_data(dest,catalogue)
        save(path,revision)
        print(key,len(revision.get('symbols',[])),'symbols;',len(revision.get('leaders',[])),'offices',flush=True)
    # Historical identity aliases are generated from explicit canonical input.
    for path in inputs:
        revision=read(path)
        for target in revision.get('copyTo',[]):
            alias=target if isinstance(target,str) else target['key']
            if alias not in identities['countries']:raise ValueError('Unknown alias '+alias)
            for field in ['flags','symbolReferences']:
                records=copy.deepcopy(identities['countries'][revision['key']].get(field,[]))
                if isinstance(target,dict):
                    for r in records:r.update(start=max(r['start'],target['start']),end=min(r['end'],target['end']))
                    records=[r for r in records if r['start']<=r['end']]
                identities['countries'][alias][field]=records
    save_data(ROOT/'public/data/identities.json',identities);media_manifest['entries']=sorted(media.values(),key=lambda m:m['file']);save_data(ROOT/'public/media/manifest.json',media_manifest)
    save_data(ROOT/'public/data/country-history.json',history);save_data(ROOT/'public/data/governance.json',governance)
    print('Compiled',len(inputs),'entity-owned revisions')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--acquire',action='store_true');main(p.parse_args().acquire)
