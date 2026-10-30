"""Civil BCE/CE dates. Negative civil years are not astronomical ISO years."""
import re

def year_text(year):
    if not year:raise ValueError('No civil year zero')
    return ('-' if year<0 else '')+f'{abs(year):04d}'

def date_key(value):
    m=re.fullmatch(r'(-?\d{4,})-(\d{2})-(\d{2})',value)
    if not m or not int(m[1]):raise ValueError('Invalid civil date '+str(value))
    return tuple(map(int,m.groups()))

def period_name(start,end):
    if start>end or not start or not end or start<0<end:raise ValueError('Invalid single-era period')
    return f'bc{abs(start):04d}-bc{abs(end):04d}' if start<0 else f'{start:04d}-{end:04d}'

def check_window(start,end):
    # Explicit research batches may span up to four centuries; civil dates
    # and single-era constraints still apply to every record in the batch.
    if start>end or end>start+399:raise ValueError('Invalid historical window')
    period_name(start,end)
