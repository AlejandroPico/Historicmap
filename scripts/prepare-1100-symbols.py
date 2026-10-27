"""Twelfth-century heraldic references, with conservative dated windows."""
import pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
ROWS=[
 ('CASTILE-KINGDOM','Royal Banner of the Kingdom of Castile.svg','1177-01-01','1199-12-31','Armas castellanas · castillo','Representación heráldica; ventana conservadora del reinado deAlfonsoVIII. El testimonio de un sello no acredita un paño digital uniforme.'),
 ('LEON-KINGDOM','Royal Banner of Leon.svg','1173-01-01','1199-12-31','Armas leonesas · león','Referencia heráldica desde los sellos documentados deFernandoII; no prueba de una bandera nacional uniforme.'),
 ('ARAGON','Royal Banner of Aragón.svg','1170-01-01','1199-12-31','Señal real de Aragón · palos','Emblema dinástico representativo de los sellos deAlfonsoII; número y forma de los palos pueden variar. No una norma textil nacional uniforme.'),
 ('BARCELONA-COUNTY','Royal Banner of Aragón.svg','1170-01-01','1199-12-31','Señal de la casa real · palos','Emblema dinástico deAlfonsoII como rey deAragón y conde deBarcelona, con instituciones territoriales diferentes.'),
 ('ENGLAND','Royal arms of England.svg','1198-01-01','1199-12-31','Armas reales inglesas · tres leones','Composición del segundo gran sello deRicardoI de1198. No se retrotrae aEnriqueII, Esteban o los reyes normandos.')]
EVIDENCE={
 'CASTILE-KINGDOM':'https://www.boe.es/biblioteca_juridica/abrir_pdf.php?id=PUB-DH-2018-87',
 'LEON-KINGDOM':'https://www.boe.es/biblioteca_juridica/abrir_pdf.php?id=PUB-DH-2018-87',
 'ARAGON':'https://www.boe.es/biblioteca_juridica/abrir_pdf.php?id=PUB-DH-2018-87',
 'BARCELONA-COUNTY':'https://www.boe.es/biblioteca_juridica/abrir_pdf.php?id=PUB-DH-2018-87',
 'ENGLAND':'https://www.reading.ac.uk/gcms/-/media/project/functions/research/graduate-centre-for-medieval-studies/documents/rms1982monograph-a-ailes-the-origins-of-the-royal-arms-of-england.pdf'}
PENDING=[
 dict(key='FRA',reason='Fleur de lis atestiguada en el sello real de1180; pendiente un recurso del sello o testimonio suficiente para el sembrado azul concreto, sin retrotraer las tres lises.'),
 dict(key='HIST-Q12548',reason='Águila monocéfala medieval; pendiente testimonio temporal específico delXII, sin retrotraer diseños bicéfalos o el formato de un armorial posterior.'),
 dict(key='PRT',reason='Escudos y quinas iniciales presentan variantes; no se retrotraen las banderas posteriores de1495 o1707.'),
 dict(key='NORTHERN-SONG',reason='No se adopta una bandera nacional reconstruida sin testimonio de período y función.'),
 dict(key='JIN-JURCHEN',reason='No confundir con elJin manchú posterior ni adjudicar una bandera moderna.'),
 dict(key='PAPAL-STATES',reason='No se retrotrae la bandera amarilla yblanca ni las llaves ytiara de composiciones posteriores.'),
 dict(key='JPN',reason='El monHōjō incorporado en elXIII no se retrotrae al gobiernoTaira o al primer régimenMinamoto.')]
if __name__=='__main__':
 code=(ROOT/'scripts/prepare-review-018-symbols.py').read_text(encoding='utf8').replace("TAG='symbols-review-0.18'","TAG='symbols-review-0.25'").replace('symbols018-pages.json','symbols025-pages.json').replace('symbols018-extra-','symbols025-extra-').replace('review-018-symbols.json','review-025-symbols.json')
 code=code.replace("json.loads((ROOT/'.cache/symbols025-pages.json').read_text(encoding='utf8'))","(json.loads((ROOT/'.cache/symbols025-pages.json').read_text(encoding='utf8')) if (ROOT/'.cache/symbols025-pages.json').exists() else [])")
 code=code.replace("if not ii.get('url') or re.search(","if re.search(r'Category:[^\\n]*fictional',wiki,re.I):raise ValueError('Fictional category')\n    if not ii.get('url') or re.search(")
 code=code.replace("display['symbolEvidenceURL']=evidence","evidence=EVIDENCE.get(key,evidence)\n   display['symbolEvidenceURL']=evidence")
 code=code[:code.index('ROWS=[')]+code[code.index('\ndef main():'):];ns={'__file__':str(ROOT/'scripts/prepare-review-018-symbols.py'),'__name__':'symbols025','ROWS':ROWS,'PENDING':PENDING,'EVIDENCE':EVIDENCE};exec(compile(code,'symbol-writer025','exec'),ns);ns['main']()
