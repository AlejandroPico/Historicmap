"""Reviewed design windows for1950–1959; not exact adoption dates."""
import importlib.util,pathlib,json
root=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('symbols',root/'scripts/curate-1970-symbols.py');h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
tag='curated-symbols-0.10'
rows=[
 ('PRY','Flag of Paraguay (1842–1954).svg','1950-01-01','1953-12-31'),
 ('HUN','Flag of Hungary (1949-1956).svg','1950-01-01','1955-12-31'),
 ('HUN','Flag of Hungary (1946-1949, 1956-1957).svg','1956-12-31','1956-12-31'),
 ('TUN','Flag of Tunisia (1831–1959).svg','1956-03-20','1958-12-31'),
 ('MAL','Flag of Malaya (1950–1963).svg','1957-08-31','1963-09-15'),
 ('CAN','Flag of Canada (1921–1957).svg','1950-01-01','1956-12-31'),('CAN','Flag of Canada (1957–1965).svg','1957-12-31','1959-12-31'),
 ('MEX','Flag of Mexico (1934-1968).svg','1950-01-01','1959-12-31'),('NIC','Flag of Nicaragua (1908–1971).svg','1950-01-01','1959-12-31'),
 ('VEN','Flag of Venezuela (1930–1954).svg','1950-01-01','1953-12-31'),('VEN','Flag of Venezuela (1954–2006).svg','1954-12-31','1959-12-31'),
 ('ECU','Flag of Ecuador.svg','1950-01-01','1959-12-31'),('PRY','Flag of Paraguay (1954–1988).svg','1954-12-31','1959-12-31'),
 ('ARG','Flag of Argentina.svg','1950-01-01','1959-12-31'),('LUX','Flag of Luxembourg.svg','1950-01-01','1959-12-31'),
 ('POL','Flag of Poland (1928–1980).svg','1950-01-01','1959-12-31'),('GRC','Flag of Greece (1822-1978).svg','1950-01-01','1959-12-31'),
 ('BGR','Flag of Bulgaria (1948–1967).svg','1950-01-01','1959-12-31'),('ROU','Flag of Romania (1948–1952).svg','1950-01-01','1951-12-31'),('ROU','Flag of Romania (1952–1965).svg','1952-12-31','1959-12-31'),
 ('IRN','State flag of Iran (1933–1964).svg','1950-01-01','1959-12-31'),('IRQ','Flag of Iraq (1924–1959).svg','1950-01-01','1958-12-31'),('IRQ','Flag of Iraq (1959–1963).svg','1959-12-31','1959-12-31'),
 ('EGY','Flag of Egypt (1922–1958).svg','1950-01-01','1952-12-31'),('EGY','Flag of Egypt (1953–1958).svg','1953-12-31','1957-12-31'),
 ('SYR','Flag of Syria (1932–1958, 1961–1963).svg','1950-01-01','1957-12-31'),('UAR','Flag of the United Arab Republic (1958–1971).svg','1958-02-22','1959-12-31'),
 ('SAU','Flag of Saudi Arabia (1938–1973).svg','1950-01-01','1959-12-31'),('YMK','Flag of the Mutawakkilite Kingdom of Yemen.svg','1950-01-01','1959-12-31'),
 ('KOR','Flag of South Korea (1949–1984).svg','1950-01-01','1959-12-31'),('BTN','Flag of Bhutan (1949–1956).svg','1950-01-01','1955-12-31'),('BTN','Flag of Bhutan (1956–1969).svg','1956-12-31','1959-12-31'),
 ('LKA','Flag of Ceylon (1948–1951).svg','1950-01-01','1950-12-31'),('LKA','Flag of Ceylon (1951–1972).svg','1951-12-31','1959-12-31'),
 ('NPL','Flag of Nepal (1743–1962).svg','1950-01-01','1959-12-31'),('THA','Flag of Thailand.svg','1950-01-01','1959-12-31'),
 ('PHL','Flag of the Philippines (1936–1985, 1986–1998).svg','1950-01-01','1959-12-31'),('VDR','Flag of North Vietnam (1945–1955).svg','1950-01-01','1954-12-31'),
 ('VSV','Flag of South Vietnam.svg','1950-01-01','1955-10-25'),('SDN','Flag of Sudan (1956–1970).svg','1956-01-01','1959-12-31'),('GHA','Flag of Ghana.svg','1957-03-06','1959-12-31'),
 ('TUN','Flag of Tunisia (1959–1999).svg','1959-12-31','1959-12-31'),
]
accepted=[];rejected=[];pages=h.cached_pages()
for key,file,start,end in rows:
 try:
  media=h.acquire(file,pages);accepted.append((key,media,start,end));print('Accepted',key,file,flush=True)
 except Exception as error:rejected.append(dict(key=key,file=file,reason=str(error)));print('Rejected',key,file,str(error)[:90],flush=True)
data=json.loads((h.OUT/'data/identities.json').read_text(encoding='utf8'));manifest=json.loads((h.OUT/'media/manifest.json').read_text(encoding='utf8'));media={m['file']:m for m in manifest['entries']}
for country in data['countries'].values():country['flags']=[f for f in country['flags'] if f.get('acquisition')!=tag]
for key,m,start,end in accepted:
 if key not in data['countries']:rejected.append(dict(key=key,reason='Entity not yet prepared'));continue
 data['countries'][key]['flags'].append(dict(start=start,end=end,media=m,source=m['url'],acquisition=tag,intervalSource=h.CHRONOLOGY,note='Ventana documental de cobertura, generalmente al cierre anual; no afirma días de adopción o derogación. Los años de diseño y la licencia proceden del archivo acreditado.'))
 media[m['file']]=m
h.save(h.OUT/'data/identities.json',data);manifest['entries']=sorted(media.values(),key=lambda m:m['file']);h.save(h.OUT/'media/manifest.json',manifest)
h.save(h.CACHE/'symbols-1950-audit.json',dict(accepted=[dict(key=k,file=m['file'],start=s,end=e) for k,m,s,e in accepted],rejected=rejected))
print('Accepted',len(accepted),'rejected',len(rejected),flush=True)
