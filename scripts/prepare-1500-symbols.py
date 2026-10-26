"""Period symbols: arms, dynastic devices and ensigns are labelled explicitly."""
import pathlib,json
ROOT=pathlib.Path(__file__).resolve().parents[1];ROWS=[]
def row(k,t,a,b,label,note):ROWS.append((k,t,a+'-01-01',b+'-12-31',label,note))
row('FRA','Arms of the Kingdom of France (Moderne).svg','1500','1588','Armas de la monarquía Valois','Escudo de azur y tres flores de lis. Es un símbolo heráldico, no una bandera nacional de diseño uniforme; no se anticipa el estandarte blanco borbónico.')
row('FRA','Royal Standard of the King of France.svg','1589','1599','Estandarte de la monarquía borbónica','Referencia dinástica posterior a la sucesión deEnriqueIV, no un pabellón nacional uniforme de todaFrancia.')
row('CASTILE','Royal Banner of the Crown of Castille (15th Century Style).svg','1500','1505','Estandarte de Castilla yLeón','Cuartelado de castillos y leones; diseño tradicional de la corona, no bandera nacional española moderna.')
row('CASTILE','Royal Banner of the Crown of Castille (Habsburg Style).svg','1506','1599','Estandarte de Castilla · Casa deAustria','Referencia heráldica castellana bajo losHabsburgo, distinta de las enseñas deAragón y de los pabellones militares de la unión de coronas.')
row('ARAGON','Royal Banner of Aragón.svg','1500','1599','Estandarte de la Corona deAragón','Palos heráldicos sobre oro; la unión dinástica no sustituye todos los símbolos territoriales por una bandera española moderna.')
row('ESP','Flag of Cross of Burgundy.svg','1530','1599','Enseña militar · cruz deBorgoña','La cruz llega en1506; la guía delIHCM fecha la primera bandera blanca con la cruz roja en1530. Este dibujo no se anticipa por confundir introducción de la divisa con el paño concreto.')
for k,t,a,b,label,note in [
 ('PRT','Flag of Portugal (1495).svg','1500','1520','Pabellón de la monarquía portuguesa','Variante atribuida aManuelI; la simplificación digital no acredita un diseño reglamentario idéntico en todos los barcos.'),
 ('PRT','Flag of Portugal (1521).svg','1521','1577','Pabellón de la monarquía portuguesa','Variante anterior al cambio de1578; se distinguen estandartes regios y pabellones navales.'),
 ('PRT','Flag of Portugal (1578).svg','1578','1599','Pabellón de la monarquía portuguesa','Variante conservada durante la unión ibérica; no implica anexión a una administración española única.'),
 ('ENGLAND','Flag of England.svg','1500','1599','Cruz deSanJorge','Enseña inglesa, no la bandera británica posterior.'),
 ('SCOTLAND','Flag of Scotland.svg','1500','1599','Cruz deSanAndrés','Referencia escocesa; la tonalidad digital no afirma un estándar cromático documentado para cada año.'),
 ('DENMARK-NORWAY','Flag of Denmark.svg','1500','1599','Dannebrog · referencia dinástica','Enseña de la monarquía danesa, no una bandera noruega moderna independiente ni prueba de control continuo deSuecia.'),
 ('KALMAR','Flag of Denmark.svg','1500','1523','Enseña de la corona danesa','Referencia de una corona dentro de la unión disputada, no bandera nacional uniforme de todos sus miembros.'),
 ('HIST-Q12548','Banner of the Holy Roman Emperor without haloes (1400-1806).svg','1500','1599','Estandarte imperial','Símbolo de la dignidad imperial, distinto de la soberanía y los estandartes de los Estados miembros.'),
 ('HABSBURG-MONARCHY','Coat of arms of the archduchy of Austria.svg','1500','1599','Blasón austriaco','Referencia dinástica deAustria; no bandera nacional uniforme de todos los dominios de todas las ramasHabsburgo.'),
 ('WURTTEMBERG-DUCHY','Wappenflagge Herzogtum Württemberg.svg','1500','1599','Bandera de armas ducal','Banner1495–1803; la continuidad heráldica no acredita gobierno efectivo del duque exiliado durante1519–1534.'),
 ('PRUSSIA-DUCHY','Flag of Ducal Prussia.svg','1525','1599','Enseña heráldica ducal','Águila prusiana con inicialS y corona en el cuello. No se anticipa a la secularización de1525 ni se convierte en bandera del reino de1701.'),
 ('FLORENCE-REPUBLIC','Flag of Florence.svg','1500','1531','Giglio · enseña cívica florentina','Lirio rojo en blanco como referencia cívica deFlorencia; no se confunde con las armasMédici ni se afirma adopción nacional moderna.'),
 ('JPN','Ashikaga mon.svg','1500','1573','Mon de losAshikaga','Emblema dinástico del shogunato. No es una bandera nacional deJapón ni representa los símbolos de todos los dominios rivales.'),
 ('DUTCH-REPUBLIC','Prinsenvlag.svg','1579','1599','Enseña del príncipe','Una de las enseñas de la revuelta; no se retrotrae la república antes de su formación ni se afirma uniformidad nacional.'),
 ('SAADI','Saadi flag.svg','1578','1599','Colores dinásticos · blanco','Referencia simplificada del estandarte blanco descrito paraAhmadalMansur; no reconstruye caligrafía ni variantes desconocidas.')]:row(k,t,a,b,label,note)
PENDING=[
 dict(key='AZTEC',reason='No se impone la bandera mexicana moderna ni una enseña nacional inventada a laTripleAlianza.'),
 dict(key='INCA',reason='La bandera arcoíris municipal contemporánea y laWiphala no acreditan un pabellón nacional inca del sigloXVI.'),
 dict(key='MING',reason='Los candidatos propios deCommons no acreditan una bandera nacional histórica uniforme; sigue pendiente evidencia material.'),
 dict(key='SAFAVID',reason='Sin cotejo suficiente del diseño concreto con un testimonio histórico de esta ventana.'),
 dict(key='HIST-Q33296',reason='Se conserva el rechazo de la bandera ficticiaAlam of theMughalEmpire; no se sustituye por otro dibujo no verificado.'),
 dict(key='JOS',reason='El sello de1637 no se retrotrae; la variante de1401 requiere un archivo y una atribución contrastados.'),
 dict(key='IBERIAN-UNION',reason='No se inventa una bandera nacional única para coronas y administraciones distintas.'),
 dict(key='BAVARIA-DUCHY',reason='La enseña electoral de1623 no se retrotrae al ducado. Pendiente una variante heráldica documentada.'),
 dict(key='RUSSIA-TSARDOM',reason='No se retrotrae el tricolor de1705; los sellos y estandartes anteriores requieren evidencia específica.')]
if __name__=='__main__':
 code=(ROOT/'scripts/prepare-review-018-symbols.py').read_text(encoding='utf8').replace("TAG='symbols-review-0.18'","TAG='symbols-review-0.21'").replace('symbols018-pages.json','symbols021-pages.json').replace('symbols018-extra-','symbols021-extra-').replace('review-018-symbols.json','review-021-symbols.json')
 code=code.replace("json.loads((ROOT/'.cache/symbols021-pages.json').read_text(encoding='utf8'))", "(json.loads((ROOT/'.cache/symbols021-pages.json').read_text(encoding='utf8')) if (ROOT/'.cache/symbols021-pages.json').exists() else [])")
 code=code.replace("if not ii.get('url') or re.search(","if re.search(r'Category:[^\\n]*fictional',wiki,re.I):raise ValueError('Fictional category')\n    if not ii.get('url') or re.search(")
 code=code.replace("display['symbolEvidenceURL']=evidence","evidence={'FRA':'https://expositions.bnf.fr/livres/armorial/grand/ars_4790_047v.htm' if a<'1589' else m['url'],'ESP':'https://ejercito.defensa.gob.es/Galerias/Descarga_pdf/Unidades/Madrid/Ihcm/2018/20180227-expo-banderas-ihcm.pdf','PRT':'https://purl.pt/37813'}.get(key,evidence)\n   display['symbolEvidenceURL']=evidence")
 code=code[:code.index('ROWS=[')]+code[code.index('\ndef main():'):];ns={'__file__':str(ROOT/'scripts/prepare-review-018-symbols.py'),'__name__':'symbols021','ROWS':ROWS,'PENDING':PENDING};exec(compile(code,'symbol-writer021','exec'),ns);ns['main']()
