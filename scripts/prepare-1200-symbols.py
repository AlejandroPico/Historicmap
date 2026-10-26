"""Thirteenth-century symbols: attested heraldry, not later national flags."""
import pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
ROWS=[
 ('FRA','Arms of the Kingdom of France (Ancien).svg','1200-01-01','1299-12-31','Armas antiguas de Francia · sembrado de lises','Referencia heráldica capeta; no se anticipan las tres lises modernas ni se afirma una norma textil uniforme.'),
 ('CASTILE-KINGDOM','Royal Banner of the Kingdom of Castile.svg','1200-01-01','1229-12-31','Estandarte castellano · castillo','Referencia a las armas castellanas anteriores a la unión de1230. La reproducción digital no acredita una tela idéntica en cada año.'),
 ('LEON-KINGDOM','Royal Banner of Leon.svg','1200-01-01','1229-12-31','Estandarte leonés · león','Referencia de la corona leonesa anterior a1230, con bibliografía heráldica. No se sustituye por un símbolo nacional contemporáneo.'),
 ('CASTILE','Royal Banner of the Crown of Castille (Early Style).svg','1230-01-01','1299-12-31','Estandarte de Castilla y León · cuartelado','El cuartelado se vincula aFernandoIII y la unión de1230. No se retrotrae al reino castellano separado ni al acceso castellano de1217.'),
 ('ARAGON','Royal Banner of Aragón.svg','1200-01-01','1299-12-31','Estandarte de la Corona de Aragón','Palos heráldicos de la casa real; representación digital, no una norma de paño uniforme ni gobierno aragonés de todas las coronas de un mismo monarca.'),
 ('ENGLAND','Royal arms of England.svg','1200-01-01','1299-12-31','Armas reales de Inglaterra · tres leones','Composición documentada en el segundo gran sello deRicardoI hacia1198. Armas reales, distintas de una bandera británica o la generalización posterior de la cruz deSanJorge.'),
 ('SCOTLAND','Royal Banner of Scotland.svg','1249-01-01','1299-12-31','Armas reales escocesas · león y doble orla flordelisada','Ventana conservadora desdeAlejandroIII para la orla flordelisada documentada en sellos. Reproducción heráldica; no se afirma un tejido uniforme de todos los reinados.'),
 ('HIST-Q12548','Holy Roman Empire Arms-single head.svg','1200-01-01','1299-12-31','Armas imperiales · águila monocéfala','Referencia heráldica medieval, no águila bicéfala posterior. No elimina las identidades y dignidades de los miembros delImperio.'),
 ('FLORENCE-REPUBLIC','Flag of Florence.svg','1251-01-01','1299-12-31','Giglio rojo sobre blanco · referencia cívica','La inversión de los esmaltes se documenta en1251. No se retrotrae a la primera mitad del siglo el lirio rojo sobre blanco.'),
 ('JPN','Japanese Crest mitu Uroko.svg','1203-01-01','1299-12-31','Mon Hōjō · tres escamas','Emblema familiar representativo durante la regenciaHōjō, no bandera nacional japonesa. La leyenda de1192 no acredita una adopción exacta ni un patrón textil uniforme; no se usa la variante del clanHōjō tardío como prueba del sigloXIII.')]
EVIDENCE={
 'FRA':'https://expositions.bnf.fr/livres/armorial/grand/ars_4790_047v.htm',
 'CASTILE':'https://publicaciones.defensa.gob.es/media/downloadable/files/links/m/e/memorial_infanteria_51.pdf',
 'CASTILE-KINGDOM':'https://publicaciones.defensa.gob.es/media/downloadable/files/links/m/e/memorial_infanteria_51.pdf',
 'LEON-KINGDOM':'https://commons.wikimedia.org/wiki/File:Royal_Banner_of_Leon.svg',
 'ENGLAND':'https://www.reading.ac.uk/gcms/-/media/project/functions/research/graduate-centre-for-medieval-studies/documents/rms1982monograph-a-ailes-the-origins-of-the-royal-arms-of-england.pdf',
 'SCOTLAND':'https://www.theheraldrysociety.com/wp-content/uploads/2019/10/CoA-225-Ailes-paper.pdf',
 'HIST-Q12548':'https://drw-www.adw.uni-heidelberg.de/drw-cgi/zeige?index=lemmata&term=reichadler',
 'FLORENCE-REPUBLIC':'https://catalogo.beniculturali.it/detail/HistoricOrArtisticProperty/0900294159',
 'JPN':'https://trip.pref.kanagawa.jp/media/x1QT6DpJLn4A0ODnx7AZKMoP6Ly1IwTshf1H6Om0/ks_221028-compactado-min.pdf'}
PENDING=[
 dict(key='MONGOL-EMPIRE',reason='No se incorpora una bandera mongola moderna o un dibujo genérico como pabellón uniforme del imperio.'),
 dict(key='YUAN',reason='Sin testimonio suficiente de bandera nacional uniforme; los retratos imperiales no son banderas.'),
 dict(key='SOUTHERN-SONG',reason='No se atribuye una bandera nacional a partir de una reconstrucción sin testimonio temporal suficiente.'),
 dict(key='JIN-JURCHEN',reason='Estandartes y emblemas requieren identificación de función y período; no se copia el símbolo delJin manchú posterior.'),
 dict(key='NICAEA',reason='No se retrotraen enseñas paleólogas atestiguadas en elXIV ni dibujos sin fuente de insignia.'),
 dict(key='LATIN-EMPIRE',reason='Las reconstrucciones retrospectivas necesitan acreditar su uso y variantes delXIII.'),
 dict(key='PRT',reason='La variante de1495 no se retrotrae alXIII; archivos de las variantes medievales anteriores pendientes.'),
 dict(key='PAPAL-STATES',reason='No se usa la bandera pontificia delXIX ni se retrotrae una composición posterior de llaves ytiara.'),
 dict(key='JPN',candidate='Japanese Crest Houjou Uroko.svg',reason='El archivo describe la variante del clanHōjō tardío deIse. ParaKamakura se conserva el mon representativo de tres triángulos, sin afirmar fecha exacta de adopción.')]
if __name__=='__main__':
 code=(ROOT/'scripts/prepare-review-018-symbols.py').read_text(encoding='utf8').replace("TAG='symbols-review-0.18'","TAG='symbols-review-0.24'").replace('symbols018-pages.json','symbols024-pages.json').replace('symbols018-extra-','symbols024-extra-').replace('review-018-symbols.json','review-024-symbols.json')
 code=code.replace("json.loads((ROOT/'.cache/symbols024-pages.json').read_text(encoding='utf8'))","(json.loads((ROOT/'.cache/symbols024-pages.json').read_text(encoding='utf8')) if (ROOT/'.cache/symbols024-pages.json').exists() else [])")
 code=code.replace("if not ii.get('url') or re.search(","if re.search(r'Category:[^\\n]*fictional',wiki,re.I):raise ValueError('Fictional category')\n    if not ii.get('url') or re.search(")
 code=code.replace("display['symbolEvidenceURL']=evidence","evidence=EVIDENCE.get(key,evidence)\n   display['symbolEvidenceURL']=evidence")
 code=code[:code.index('ROWS=[')]+code[code.index('\ndef main():'):];ns={'__file__':str(ROOT/'scripts/prepare-review-018-symbols.py'),'__name__':'symbols024','ROWS':ROWS,'PENDING':PENDING,'EVIDENCE':EVIDENCE};exec(compile(code,'symbol-writer024','exec'),ns);ns['main']()
