"""Use precise life dates only as an identity guard, never as office dates."""
import re

def precise_life_year(entity,prop):
    for claim in entity.get('claims',{}).get(prop,[]):
        if claim.get('rank')=='deprecated':continue
        value=claim.get('mainsnak',{}).get('datavalue',{}).get('value',{})
        if value.get('precision',0)<9 or value.get('before',0) or value.get('after',0):continue
        match=re.match(r'([+-]\d+)-',value.get('time',''))
        if match and int(match[1]):return int(match[1])
    return None
