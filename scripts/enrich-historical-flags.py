"""Date flag records from explicit country/flag-identity claims, not appearance.

A matching P163 flag identity and its P18 filename are required to extend an
undated P41 image. Existing curated/date-qualified intervals take precedence.
--catalog-only warms the acquisition cache without changing public artifacts.
"""
import argparse, importlib.util, json, hashlib, pathlib, urllib.parse, urllib.request, html, re, datetime
spec=importlib.util.spec_from_file_location('historical',pathlib.Path(__file__).with_name('enrich-historical-authorities.py'));h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
def date_value(v):
    return v['time'].lstrip('+')[:10].replace('-00','-01') if isinstance(v,dict) and 'time' in v else None
def acquire(catalog_only=False):
    data=json.loads((h.OUT/'data/identities.json').read_text(encoding='utf8'));countries=data['countries'];relations=[]
    entities={q:e for q,e in h.parallel(h.entity,sorted({c['qid'] for c in countries.values() if re.fullmatch(r'Q\d+',c.get('qid',''))})) if e}
    for key,c in countries.items():
        e=entities.get(c['qid'],{})
        for s in e.get('claims',{}).get('P163',[]):
            q=s.get('mainsnak',{}).get('datavalue',{}).get('value',{}).get('id')
            if q and s.get('rank')!='deprecated':relations.append(dict(key=key,flag=q,start=h.qual(s,'P580'),end=h.qual(s,'P582'),sourceStatement=s.get('id')))
    flags={q:e for q,e in h.parallel(h.entity,sorted({r['flag'] for r in relations})) if e}
    # Follow explicitly recorded predecessor designs. A current flag identity
    # alone must not erase the flag used before a dated change of regime/design.
    frontier=list(relations);seen={(r['key'],r['flag']) for r in relations}
    for depth in range(6):
        extra=[]
        for r in frontier:
            e=flags.get(r['flag'],{});dates=[date_value(v) for v in h.values(e,'P571')];start=r['start'][0] if r['start'] else min((d for d in dates if d),default=None)
            if not start or start<=h.START:continue
            end=(datetime.date.fromisoformat(start)-datetime.timedelta(days=1)).isoformat()
            for v in h.values(e,'P1365')+h.values(e,'P155'):
                if not isinstance(v,dict) or not v.get('id') or (r['key'],v['id']) in seen:continue
                seen.add((r['key'],v['id']));extra.append(dict(key=r['key'],flag=v['id'],start=None,end=(end,11),sourceStatement='predecessor-of-'+r['flag']))
        if not extra:break
        flags.update({q:e for q,e in h.parallel(h.entity,sorted({r['flag'] for r in extra if r['flag'] not in flags})) if e});relations.extend(extra);frontier=extra
    candidates=[];undated=[]
    for r in relations:
        e=flags.get(r['flag'],{});images=h.values(e,'P18');starts=[date_value(v) for v in h.values(e,'P571')];ends=[date_value(v) for v in h.values(e,'P576')];start=r['start'][0] if r['start'] else min((s for s in starts if s),default=None);end=r['end'][0] if r['end'] else min((s for s in ends if s),default=h.TODAY)
        if not start:undated.append(dict(country=r['key'],flag=r['flag'],reason='No dated adoption/inception assertion'));continue
        if end<h.START or start>h.TODAY:continue
        if r['key'] in h.LIFETIMES:
            lo,hi=h.LIFETIMES[r['key']];start=max(start,lo);end=min(end,hi)
        for filename in images:
            if isinstance(filename,str) and filename.lower().endswith('.svg'):candidates.append(dict(country=r['key'],filename=filename,start=start,end=min(end,h.TODAY),source='https://www.wikidata.org/wiki/'+r['flag']))
    # Explicit historical design files fill gaps where the general P163 item
    # only illustrates the current flag. Their year ranges are annual evidence,
    # not claims of exact adoption days. A later dated design takes precedence.
    historical_files={
      'ZAF':[('Flag of South Africa (1928–1994).svg',1928,1994)],
      'ETH':[('Flag of Ethiopia (1987–1991).svg',1987,1991),('Flag of Ethiopia (1991–1996).svg',1991,1996)],
      'SYR':[('Flag of Syria (1980–2024).svg',1980,2024)],
      'COD':[('Flag of Zaire (1971–1997).svg',1971,1997),('Flag of the Democratic Republic of the Congo (1997–2003).svg',1997,2003),('Flag of the Democratic Republic of the Congo (2003–2006).svg',2003,2006)],
      'LBY':[('Flag of Libya (1977–2011).svg',1977,2011)],
      'RWA':[('Flag of Rwanda (1962–2001).svg',1962,2001)],
      'IRQ':[('Flag of Iraq (1963–1991).svg',1963,1991),('Flag of Iraq (1991–2004).svg',1991,2004),('Flag of Iraq (2004–2008).svg',2004,2008)],
      'AFG':[('Flag of Afghanistan (1987–1992).svg',1987,1992),('Flag of Afghanistan (1992–2001).svg',1992,1996),('Flag of Afghanistan (1992–2001).svg',2001,2002),('Flag of Afghanistan (2002–2004).svg',2002,2004),('Flag of Afghanistan (2004–2013).svg',2004,2013)],
      'MNG':[('Flag of Mongolia (1945–1992).svg',1945,1992),('Flag of Mongolia (1992–2011).svg',1992,2011)],
      'KHM':[('Flag of the State of Cambodia (1989–1992).svg',1989,1992),('Flag of Cambodia under UNTAC.svg',1992,1993)],
      'ALB':[('Flag of Albania (1946–1992).svg',1946,1992)],
      'MMR':[('Flag of Myanmar (1974–2010).svg',1974,2010)]}
    for key,files in historical_files.items():
        for filename,first,last in files:candidates.append(dict(country=key,filename=filename,start=f'{first}-01-01',end=f'{last}-12-31',source='https://commons.wikimedia.org/wiki/File:'+urllib.parse.quote(filename),annualOnly=True))
    h.save(h.CACHE/'historical-flags-catalog.json',dict(candidates=candidates,undated=undated));print('Flag identities',len(flags),'dated candidates',len(candidates),'undated',len(undated),flush=True)
    if catalog_only:return
    # The authority acquisition may have completed while metadata was loading.
    # Re-read immediately before updating, preserving its new people and media.
    data=json.loads((h.OUT/'data/identities.json').read_text(encoding='utf8'));countries=data['countries'];manifest=json.loads((h.OUT/'media/manifest.json').read_text(encoding='utf8'));media={m['file']:m for m in manifest['entries']};changed=[];rejected=[]
    for country in countries.values():country['flags']=[f for f in country['flags'] if f['start']<=f['end']]
    for c in candidates:
        if c['start']>c['end']:rejected.append(dict(**c,reason='Contradictory source inception/replacement dates'));continue
        country=countries[c['country']];matches=[f for f in country['flags'] if f['media']['title']==c['filename']]
        # A dated original P41/cured flag interval overrides generic P163
        # inception dates, which may concern an older design in the same family.
        if matches:
            for old in matches:
                if old['start']==h.TODAY and old['end']==h.TODAY:
                    old['start']=c['start'];old['end']=c['end'];old['source']=c['source'];changed.append(c)
            if not c.get('annualOnly') or any(f['start']<=c['start'] and f['end']>=c['end'] for f in matches):continue
        # Do not add a generic flag identity atop an existing dated design.
        if not c.get('annualOnly') and any(f['start']<h.TODAY and f['start']<=c['end'] and f['end']>=c['start'] for f in country['flags']):continue
        if c.get('annualOnly'):
            later=[f['start'] for f in country['flags'] if f['media']['title']!=c['filename'] and c['start']<f['start']<=c['end'] and f['start']<h.TODAY]
            if later:c['end']=(datetime.date.fromisoformat(min(later))-datetime.timedelta(days=1)).isoformat()
        if c['start']>c['end']:rejected.append(dict(**c,reason='Contradictory source interval after next dated design'));continue
        if any(f['start']==c['start'] and f['end']==c['end'] and f['media']['title']==c['filename'] for f in country['flags']):continue
        filename=c['filename'];digest=hashlib.sha256(filename.encode()).hexdigest()[:20]
        try:
            params=dict(action='query',titles='File:'+filename,redirects=1,prop='imageinfo',iiprop='url|extmetadata',format='json');info=h.get('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params),'commons-'+digest);page=next(iter(info.get('query',{}).get('pages',{}).values()),{});ii=page.get('imageinfo',[{}])[0];meta=ii.get('extmetadata',{});lic=meta.get('LicenseShortName',{}).get('value','');url=ii.get('url','')
            if not url or not any(v in lic.lower() for v in ['public domain','cc0','cc by','cc-by','pd-']):rejected.append(c);continue
            relative='media/flag-'+digest+'.svg';dest=h.OUT/relative
            if not dest.exists():
                raw=h.download(url)
                if b'<svg' not in raw or b'<script' in raw.lower() or b'javascript:' in raw.lower():rejected.append(c);continue
                dest.write_bytes(raw)
            clean=lambda v:html.unescape(re.sub('<[^>]*>','',v));m=dict(file=relative,title=filename,url=ii.get('descriptionurl',''),artist=clean(meta.get('Artist',{}).get('value','')),license=lic,licenseUrl=meta.get('LicenseUrl',{}).get('value',''),attribution=clean(meta.get('Attribution',{}).get('value','')),attributionRequired=meta.get('AttributionRequired',{}).get('value')=='true',credit=clean(meta.get('Credit',{}).get('value','')),sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),bytes=dest.stat().st_size,sourceUrl=url);media[relative]=m;country['flags'].append(dict(start=c['start'],end=c['end'],source=c['source'],media=m));changed.append(c)
        except Exception as error:rejected.append(dict(**c,reason=str(error)))
    h.save(h.OUT/'data/identities.json',data);manifest['entries']=sorted(media.values(),key=lambda m:m['file']);h.save(h.OUT/'media/manifest.json',manifest)
    audit=dict(changed=changed,rejected=rejected,undated=undated,annual=[dict(year=y,countryKeys=sum(any(f['start']<=min(f'{y}-12-31',h.TODAY) and f['end']>=min(f'{y}-12-31',h.TODAY) for f in country['flags']) for country in countries.values())) for y in range(1990,int(h.TODAY[:4])+1)])
    h.save(h.CACHE/'historical-flags-audit.json',audit);print('Flag intervals changed',len(changed),'rejected',len(rejected),'annual endpoints',audit['annual'][0],audit['annual'][-1],flush=True)
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--catalog-only',action='store_true');args=parser.parse_args();acquire(args.catalog_only)
