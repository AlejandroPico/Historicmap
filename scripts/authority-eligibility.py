"""Eligibility for generic authority acquisition; source office claims alone
can include fictional holders of real offices. Explicit collective authorities
are separate from individual people. Curated historical statements are not
silently discarded for missing generic metadata.
"""
REVIEWED_COLLECTIVES={'Q30917'}  # Swiss Federal Council, documented collegial head.

def real_authority(entity):
    if entity.get('id') in REVIEWED_COLLECTIVES:
        return True
    types={s.get('mainsnak',{}).get('datavalue',{}).get('value',{}).get('id')
           for s in entity.get('claims',{}).get('P31',[]) if s.get('rank')!='deprecated'}
    return 'Q5' in types and not types.intersection({'Q15632617','Q95074'})
