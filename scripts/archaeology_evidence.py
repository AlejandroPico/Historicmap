"""Validate archaeological consultation windows separately from political terms."""
from civil_dates import period_name,date_key

def check_archaeology(d):
    if d.get('format')!='archaeological-evidence':raise ValueError('Missing archaeological evidence format')
    a,b=d['coverageStart'],d['coverageEnd'];period_name(a,b)
    if any(d.get(field)for field in ['leaders','symbols','entityRules']):raise ValueError('Archaeological reference cannot manufacture rulers, national symbols or political borders')
    for r in d.get('authorityNotes',[]):
        start,end=date_key(r['start']),date_key(r['end'])
        if not r.get('source')or not r.get('text')or start>end or not a<=start[0]<=end[0]<=b:raise ValueError('Invalid archaeological authority note')
    for r in d.get('places',[]):
        x,y=r['coordinates']
        if not a<=r['start']<=r['end']<=b or not r.get('source')or not r.get('note')or r.get('referenceKind')!='archaeological-site' or r.get('capital') or not(-180<=x<=180 and -90<=y<=90):raise ValueError('Invalid archaeological site reference')
    for r in d.get('governance',[]):
        if r.get('tags')!=['unclassified']:raise ValueError('Archaeological complexity alone does not establish a political constitution')
    for r in d.get('contexts',[]):
        start,end=date_key(r['start']),date_key(r['end'])
        if r.get('type')!='transition' or r.get('confidence')!='archaeological-reference' or not r.get('source')or not r.get('text')or start>=end or not a<=start[0]<=b or end[0]>b+1:raise ValueError('Invalid archaeological context or unsupported event type')
