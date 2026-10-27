"""Documentary seal, not a retroactively invented national flag."""
import pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
ROWS=[('FRA','Sceau de Robert II le pieux.jpg','1006-01-01','1030-12-31','Símbolo documental · sello de RobertoII','Reproducción de un tipo de sello documentado en1006–1030. Identifica al rey y su documentación, no una bandera nacional ni una norma textil.')]
EVIDENCE={'FRA':'https://sigilla.irht.cnrs.fr/5320'}
PENDING=[
 dict(key='ENGLAND',reason='Los tres leones son posteriores. No se usa una bandera deWessex reconstruida o armas póstumas deEduardo como bandera atestiguada delXI.'),
 dict(key='NORMANDY-DUCHY',reason='Los dos leones posteriores no acreditan una enseña uniforme del ducado delXI.'),
 dict(key='CASTILE-COUNTY',reason='El castillo heráldico castellano delXII no se anticipa al condado ni aFernandoI.'),
 dict(key='ARAGON-KINGDOM',reason='Los palos heráldicos de la casa posterior no se retrotraen aRamiroI oSanchoRamírez.'),
 dict(key='NORTHERN-SONG',reason='Sin testimonio suficiente para una bandera nacional uniforme delXI.'),
 dict(key='LIAO',reason='Estandartes dinásticos necesitan identificación temporal y de función.'),
 dict(key='FATIMID',reason='Colores dinásticos y símbolos religiosos no acreditan un paño digital uniforme.'),
 dict(key='JPN',reason='No se retrotraen emblemasHōjō, Minamoto ni banderas nacionales modernas.'),
 dict(key='HIST-Q12548',reason='No se usan águilas bicéfalas tardías ni diseños de armoriales posteriores como enseña uniforme delXI.')]
if __name__=='__main__':
 code=(ROOT/'scripts/prepare-review-018-symbols.py').read_text(encoding='utf8').replace("TAG='symbols-review-0.18'","TAG='symbols-review-0.26'").replace('symbols018-pages.json','symbols026-pages.json').replace('symbols018-extra-','symbols026-extra-').replace('review-018-symbols.json','review-026-symbols.json')
 code=code.replace("json.loads((ROOT/'.cache/symbols026-pages.json').read_text(encoding='utf8'))","(json.loads((ROOT/'.cache/symbols026-pages.json').read_text(encoding='utf8')) if (ROOT/'.cache/symbols026-pages.json').exists() else [])")
 code=code.replace("if not ii.get('url') or re.search(","if re.search(r'Category:[^\\n]*fictional',wiki,re.I):raise ValueError('Fictional category')\n    if not ii.get('url') or re.search(")
 code=code.replace("display['symbolEvidenceURL']=evidence","evidence=EVIDENCE.get(key,evidence)\n   display['symbolEvidenceURL']=evidence")
 code=code[:code.index('ROWS=[')]+code[code.index('\ndef main():'):];ns={'__file__':str(ROOT/'scripts/prepare-review-018-symbols.py'),'__name__':'symbols026','ROWS':ROWS,'PENDING':PENDING,'EVIDENCE':EVIDENCE};exec(compile(code,'symbol-writer026','exec'),ns);ns['main']()
