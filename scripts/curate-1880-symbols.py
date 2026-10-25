"""Conservative1880–1899 symbols using unchanged, individually licensed SVGs.

Reuses the bounded acquisition engine; --check-sources never changes public.
Earlier source dates are not inferred from contemporary national designs.
"""
import importlib.util,json,pathlib,re
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('symbols1900',ROOT/'scripts/curate-1900-symbols.py')
prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
engine=prior.engine
FIRST,LAST='1880-01-01','1899-12-31'
TAG='curated-symbols-1880-0.13'
SOURCES=dict(prior.SOURCES)
ROWS=[]
# Families already researched in1900, with the documented earlier span.
families=['GBR','FRA','ESP','ITA','JPN','PRT','BEL','NLD','SWE','GRC','LUX','ROU','BGR','NPL','THA','OTT','AUT-HUN']
for key in families:
 row=next(r for r in prior.ROWS if r[0]==key)
 if key=='THA':row=next(r for r in prior.ROWS if r[0]==key and '(1855)' in r[1])
 start='1880-01-01'
 if key=='ROU':start='1881-12-31'
 ROWS.append((key,row[1],start,LAST,row[4],row[5]+' Ventana1880–1899: se representa esta familia histórica, no una normalización cromática digital retrospectiva.'))
for key,filename,start,end,note in [
 ('DEU','Flag of the German Empire.svg',FIRST,LAST,'Tricolor imperial negro-blanco-rojo; no símbolos del régimen nazi posterior.'),
 ('RUE','Flag of Russia.svg','1896-12-31',LAST,'Tricolor nacional reconocido en1896. La ventana no afirma una bandera nacional única y uniforme para los años anteriores.'),
 ('QING','Flag of China (1889–1912).svg','1889-12-31',LAST,'Bandera imperial rectangular del dragón desde1889; no se retrotrae a la etapa de enseñas triangulares.'),
 ('AFG','Flag of Afghanistan (1880–1901).svg',FIRST,LAST,'Familia de la etapa de Abdur Rahman; cobertura anual, no día de adopción de todas sus variantes.'),
 ('EGY','Flag of Egypt (1882–1922).svg','1882-12-31',LAST,'Enseña del periodo del jedivato bajo ocupación británica, sin confundir ocupación con anexión.'),
 ('KEM','Flag of Korea (1899).svg','1899-12-31',LAST,'Variante de la fuente naval contemporánea1899; no normalización surcoreana de1949.'),
 ('SRK','Flag of Serbia (1882–1918).svg','1882-12-31',LAST,'Reino de Serbia desde1882. No se extiende retrospectivamente sobre el principado como un nuevo título real.'),
 ('CFS','Flag of the Congo Free State.svg','1885-12-31',LAST,'Estado Libre del Congo bajo soberanía personal de LeopoldoII, separado del Estado belga.'),
 ('TON','Flag of Tonga.svg',FIRST,LAST,'Familia de la bandera tongana adoptada en1875; la ilustración no reconstruye cada ejemplar material.'),
 ('HAW-KINGDOM','Flag of Hawaii.svg',FIRST,'1892-12-31','Bandera del reino; no indica anexión estadounidense.'),
 ('HAW-PROVISIONAL','Flag of Hawaii.svg','1893-01-01','1893-12-31','Continuidad de la familia gráfica bajo el Gobierno provisional; no continuidad de la monarquía.'),
 ('HAW-REPUBLIC','Flag of Hawaii.svg','1894-01-01','1897-12-31','Bandera de Hawái durante la república, distinta de la bandera federal estadounidense.'),
]:
 ROWS.append((key,filename,start,end,None,note))
for i,row in enumerate(json.loads((ROOT/'scripts/symbols-1880-research.json').read_text(encoding='utf8'))):
 source='america-'+str(i);SOURCES[source]=row['source']
 ROWS.append((row['key'],row['filename'],row['start'],row['end'],source,row['note']))
EXCLUDED=[
 dict(key='QING',start=FIRST,end='1888-12-31',reason='Falta adquirir una enseña triangular acreditada; no retroproyectar el dragón rectangular1889.'),
 dict(key='RUE',start=FIRST,end='1896-12-30',reason='Usos imperiales, civiles y mercantes requieren distinción; no se afirma un símbolo nacional único.'),
 dict(key='JOS',reason='Variantes anteriores al atlas naval1899 pendientes de cotejo y adquisición.'),
]
engine.ROWS,engine.SOURCES,engine.EXCLUDED=ROWS,SOURCES,EXCLUDED
engine.TAG,engine.PREFIX=TAG,'symbols-1880'
engine.base.START,engine.base.END=FIRST,LAST
engine.__doc__=__doc__
# Restore the generic pure curator; the1900-only Czechoslovak correction must
# not run against1880 or subtract valid twentieth-century symbols.
engine.curate=prior.original_curate
curate=engine.curate
if __name__=='__main__':raise SystemExit(engine.main())
