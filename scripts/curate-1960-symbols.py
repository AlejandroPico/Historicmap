"""Licensed historical flag variants for the new decade, with explicit annual coverage.

File descriptions/Commons chronology identify the design, not geopolitical
recognition. Rejected filenames/licences are recorded rather than replaced with
a modern successor symbol. Preserve all prior curations and media credits.
"""
import importlib.util,pathlib,json
root=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('symbols',root/'scripts/curate-1970-symbols.py');h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
tag='curated-symbols-0.9';rows=[]
def design(key,file,start,end):rows.append((key,file,start,end))
for row in [
 ('CAN','Flag of Canada (1957–1965).svg','1960-01-01','1964-12-31'),
 ('MEX','Flag of Mexico (1934-1968).svg','1960-01-01','1967-12-31'),
 ('NIC','Flag of Nicaragua (1908–1971).svg','1960-01-01','1969-12-31'),
 ('VEN','Flag of Venezuela (1954–2006).svg','1960-01-01','1969-12-31'),
 ('ECU','Flag of Ecuador.svg','1960-01-01','1969-12-31'),
 ('BRA','Flag of Brazil (1960–1968).svg','1960-12-31','1967-12-31'),
 ('PRY','Flag of Paraguay (1954–1988).svg','1960-01-01','1969-12-31'),
 ('ARG','Flag of Argentina.svg','1960-01-01','1969-12-31'),
 ('LUX','Flag of Luxembourg.svg','1960-01-01','1969-12-31'),
 ('POL','Flag of Poland (1928–1980).svg','1960-01-01','1969-12-31'),
 ('GRC','Flag of Greece (1822-1978).svg','1960-01-01','1969-12-31'),
 ('CYP','Flag of Cyprus (1960–2006).svg','1960-12-31','1969-12-31'),
 ('BGR','Flag of Bulgaria (1948–1967).svg','1960-01-01','1966-12-31'),
 ('ROU','Flag of Romania (1952–1965).svg','1960-01-01','1964-12-31'),
 ('ROU','Flag of Romania (1965–1989).svg','1965-12-31','1969-12-31'),
 ('MLI','Flag of Mali (1959–1961).svg','1960-12-31','1960-12-31'),
 ('MRT','Flag of Mauritania (1959–2017).svg','1960-12-31','1969-12-31'),
 ('BFA','Flag of Upper Volta.svg','1960-01-01','1969-12-31'),
 ('GHA','Flag of Ghana.svg','1960-01-01','1963-12-31'),
 ('GHA','Flag of Ghana (1964–1966).svg','1964-12-31','1965-12-31'),
 ('CMR','Flag of Cameroon (1957–1961).svg','1960-01-01','1960-12-31'),
 ('CMR','Flag of Cameroon (1961–1975).svg','1961-12-31','1969-12-31'),
 ('COD','Flag of the Republic of the Congo (Léopoldville) (1960–1963).svg','1960-12-31','1962-12-31'),
 ('COD','Flag of the Republic of the Congo (Léopoldville) (1963–1966).svg','1963-12-31','1965-12-31'),
 ('COD','Flag of the Democratic Republic of the Congo (1966–1971).svg','1966-12-31','1969-12-31'),
 ('TUN','Flag of Tunisia (1959–1999).svg','1960-01-01','1969-12-31'),
 ('SDN','Flag of Sudan (1956–1970).svg','1960-01-01','1969-12-31'),
 ('IRN','State flag of Iran (1933–1964).svg','1960-01-01','1963-12-31'),
 ('IRQ','Flag of Iraq (1959–1963).svg','1960-01-01','1962-12-31'),
 ('SAU','Flag of Saudi Arabia (1938–1973).svg','1960-01-01','1969-12-31'),
 ('YMK','Flag of the Mutawakkilite Kingdom of Yemen.svg','1960-01-01','1961-12-31'),
 ('KOR','Flag of South Korea (1949–1984).svg','1960-01-01','1969-12-31'),
 ('BTN','Flag of Bhutan (1956–1969).svg','1960-01-01','1968-12-31'),
 ('LKA','Flag of Ceylon (1951–1972).svg','1960-01-01','1969-12-31'),
 ('NPL','Flag of Nepal (1743–1962).svg','1960-01-01','1961-12-31'),
 ('THA','Flag of Thailand.svg','1960-01-01','1969-12-31'),
 ('PHL','Flag of the Philippines (1936–1985, 1986–1998).svg','1960-01-01','1969-12-31'),
 ('UAR','Flag of the United Arab Republic (1958–1971).svg','1960-01-01','1960-12-31'),
 ('EGY','Flag of the United Arab Republic (1958–1971).svg','1961-01-01','1969-12-31'),
 ('TAN','Flag of Tanganyika (1961–1964).svg','1961-12-31','1963-12-31'),
 ('SYR','Flag of Syria (1932–1958, 1961–1963).svg','1961-12-31','1962-12-31'),
 ('SYR','Flag of Syria (1963–1972).svg','1963-12-31','1969-12-31'),
 ('BDI','Flag of Burundi (1962–1966).svg','1962-12-31','1965-12-31'),
 ('BDI','Flag of Burundi (1966–1967).svg','1966-12-31','1966-12-31'),
 ('ZAN','Flag of the Sultanate of Zanzibar.svg','1963-12-10','1964-01-11'),
 ('HTI','Flag of Haiti (1964–1986).svg','1964-12-31','1969-12-31'),
 ('ZMB','Flag of Zambia (1964–1996).svg','1964-12-31','1969-12-31'),
 ('RHO','Flag of Rhodesia (1964–1968).svg','1965-12-31','1967-12-31'),
 ('LSO','Flag of Lesotho (1966–1987).svg','1966-12-31','1969-12-31'),
 ('GNQ','Flag of Equatorial Guinea (without coat of arms).svg','1968-12-31','1968-12-31'),
 ('GNQ','Flag of Equatorial Guinea.svg','1969-12-31','1969-12-31'),
 ('LBY','Flag of Libya (1969–1972).svg','1969-12-31','1969-12-31'),
 ('UNTEA','Flag of the United Nations.svg','1962-10-01','1963-04-30'),
]:design(*row)
accepted=[];rejected=[];pages=h.cached_pages()
for key,file,start,end in rows:
 try:
  media=h.acquire(file,pages);accepted.append((key,media,start,end))
  print('Accepted',key,file,flush=True)
 except Exception as error:rejected.append(dict(key=key,file=file,reason=str(error)));print('Rejected',key,file,str(error)[:90],flush=True)
data=json.loads((h.OUT/'data/identities.json').read_text(encoding='utf8'));manifest=json.loads((h.OUT/'media/manifest.json').read_text(encoding='utf8'));media={m['file']:m for m in manifest['entries']}
for country in data['countries'].values():country['flags']=[f for f in country['flags'] if f.get('acquisition')!=tag]
for key,m,start,end in accepted:
 data['countries'][key]['flags'].append(dict(start=start,end=end,media=m,source=m['url'],acquisition=tag,intervalSource=h.CHRONOLOGY,note='Ventana histórica de cobertura, generalmente al cierre anual; sus extremos no se presentan como adopción o derogación del diseño. Descripción y procedencia del archivo conservadas.'))
 media[m['file']]=m
h.save(h.OUT/'data/identities.json',data);manifest['entries']=sorted(media.values(),key=lambda m:m['file']);h.save(h.OUT/'media/manifest.json',manifest)
h.save(h.CACHE/'symbols-1960-audit.json',dict(accepted=[dict(key=k,file=m['file'],start=s,end=e) for k,m,s,e in accepted],rejected=rejected))
print('Accepted',len(accepted),'rejected',len(rejected),flush=True)
