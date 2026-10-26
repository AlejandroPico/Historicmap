"""Dated representative symbols, distinct from modern national flags."""
import pathlib,importlib.util,json
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('s',ROOT/'scripts/prepare-review-018-symbols.py');s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
ROWS=[]
def row(k,t,a,b,label,note):ROWS.append((k,t,a+'-01-01',b+'-12-31',label,note))
row('FRA','Royal Standard of the King of France.svg','1600','1699','Estandarte real','Enseña representativa de la monarquía borbónica, no bandera nacional tricolor.')
row('ESP','Flag of Cross of Burgundy.svg','1600','1699','Enseña militar · cruz de Borgoña','Símbolo militar de la monarquía hispánica; coexistían estandartes reales y pabellones navales distintos. No afirma un paño nacional uniforme para todos sus dominios.')
for a,b in [('1600','1648'),('1660','1699')]:row('ENGLAND','Flag of England.svg',a,b,'Cruz de San Jorge','Enseña inglesa; no se anticipa la unión política de1707 ni la bandera de1801.')
for a,b in [('1600','1651'),('1660','1699')]:row('SCOTLAND','Flag of Scotland.svg',a,b,'Cruz de San Andrés','Referencia escocesa. La tonalidad digital no es una norma cromática documentada para cada año.')
row('ENGLISH-COMMONWEALTH','Flag of the Commonwealth (1649-1651).svg','1649','1650','Pabellón de la Commonwealth','Variante inicial con cruz deSanJorge y arpa; no se extiende sobre la monarquía deCarlosI.')
row('ENGLISH-COMMONWEALTH','Commonwealth-Flag-1651.svg','1651','1657','Pabellón de la Commonwealth','Variante de1651; la reorganización institucional delProtectorado no equivale a una bandera monárquica.')
row('ENGLISH-COMMONWEALTH','Flag of the Commonwealth (1658–1660).svg','1658','1659','Pabellón del interregno','Variante posterior a1658, limitada al período republicano activo en la selección anual. No continúa después de laRestauración.')
row('PRT','Flag of Portugal (1578).svg','1600','1615','Pabellón de la monarquía portuguesa','Portugal conserva pabellones e instituciones propios durante la unión dinástica conEspaña.')
row('PRT','Flag of Portugal (1616).svg','1616','1639','Pabellón naval portugués','Variante con orla verde de1616, reproducida desde el catálogo histórico de laBiblioteca Nacional dePortugal; no equivale a anexión española.')
row('PRT','Flag of Portugal (1640).svg','1640','1666','Pabellón de la Restauración','Variante tras la proclamación deJoãoIV, anterior al cambio de1667.')
row('PRT','Flag of Portugal (1667).svg','1667','1699','Pabellón de la monarquía portuguesa','Variante anterior a1707; no se adelanta el diseño posterior.')
row('DUTCH-REPUBLIC','Prinsenvlag.svg','1600','1649','Enseña del príncipe','Naranja, blanco y azul; una de las enseñas históricas, no un diseño nacional único y obligatorio en todos los ámbitos. El tricolor rojo también aparece durante el siglo.')
row('DUTCH-REPUBLIC','Flag of the Netherlands.svg','1653','1699','Pabellón de los Estados','Referencia roja, blanca y azul posterior a la transición de colores del sigloXVII; no se proyecta automáticamente sobre1600.')
row('HIST-Q12548','Banner of the Holy Roman Emperor without haloes (1400-1806).svg','1600','1699','Estandarte imperial','Enseña del emperador, distinta de los símbolos de los Estados miembros.')
row('HABSBURG-MONARCHY','Coat of arms of the archduchy of Austria.svg','1600','1699','Blasón austriaco','Bindenschild heráldico deAustria como referencia dinástica. No es una bandera nacional uniforme de todos los dominios Habsburgo.')
row('BAVARIA-ELECTORATE','Flag of the Electorate of Bavaria.svg','1623','1699','Pabellón heráldico del electorado','No se anticipa la dignidad electoral a1623 ni la real a1806.')
row('SAXONY-ELECTORATE','State flag of Saxony before 1815.svg','1600','1699','Pabellón de Sajonia','Referencia heráldica del electorado anterior al reino del sigloXIX.')
row('HIST-Q157367','Flag of Brandenburg (1657-1701).svg','1657','1699','Enseña electoral','Variante anterior a1701, con dignidad electoral; no se adelantan los atributos reales dePrusia.')
row('WURTTEMBERG-DUCHY','Wappenflagge Herzogtum Württemberg.svg','1600','1699','Bandera de armas ducal','Banner heráldico1495–1803; no la bandera del reino posterior.')
row('PAPAL-STATES','Flag of the Papal States (pre 1808).svg','1600','1699','Pabellón pontificio','Colores rojo y amarillo anteriores a1808, no los colores nacionales actuales delVaticano.')
row('HIST-Q208169','Civil and merchant flag of the Republic of Ragusa (c. 1667-1807).svg','1667','1699','Pabellón civil y mercante','Ventana posterior a1667; no se inventa su adopción anterior.')
row('DENMARK-NORWAY','Flag of Denmark.svg','1600','1699','Dannebrog · pabellón monárquico','Referencia de la monarquía danesa-noruega, no una bandera noruega moderna independiente.')
row('JPN','Tokugawa family crest.svg','1603','1699','Mon de los Tokugawa','Emblema dinástico del Gobierno shogunal; no bandera nacional ni pabellón naval de finales del sigloXIX.')
row('QING','Plain Yellow Banner.svg','1636','1699','Enseña institucional · Bandera Amarilla','Representación de una institución de lasOchoBanderas, no bandera nacional uniforme deChina ni el diseño nacional del sigloXIX.')
row('JOS','Joseongukwangjiin (The Seal of the King of Joseon, 1637-1653).svg','1637','1652','Sello del rey de Joseon','Reproducción del sello de investidura de1637; un sello de autoridad, no bandera nacional.')
row('JOS','Joseongukwangjiin (The Seal of the King of Joseon, 1653-1776).svg','1653','1699','Sello del rey de Joseon','Variante de1653 con caracteres chinos y manchúes; no se anticipa elTaegeukgi.')
row('AYUTTHAYA','Flag of Thailand (Ayutthaya period).svg','1680','1699','Pabellón marítimo rojo','Ventana interior del uso documentado desde la época deNarai. No se afirma su adopción exacta ni su uso uniforme desde1600.')
row('SAADI','Saadi flag.svg','1600','1603','Colores dinásticos · blanco','Referencia simplificada del estandarte blanco saadí documentado en las descripciones deAhmadalMansur. No reconstruye la caligrafía bordada ni todos los pabellones de sus sucesores.')
row('MAR','Flag of Morocco (1666–1915).svg','1666','1699','Pabellón dinástico alauí','Campo rojo posterior al establecimiento alauí; no se atribuye al sultanato saadí anterior.')
PENDING=[
 dict(key='MING',candidate='Ming dynasty red trian flag.png',reason='Obra propia de2026 sin descripción ni testimonio histórico del diseño. No se adopta como bandera nacional.'),
 dict(key='SAFAVID',candidate='Flag Safavid1678.jpg',reason='El título no acredita una datación material ni continuidad. Falta cotejo del diseño con un testimonio histórico.'),
 dict(key='HIST-Q33296',candidate='Alam of the Mughal Empire.svg',reason='Categoría de bandera ficticia. No se retrotraen ilustraciones del sigloXIX ni se infiere un pabellón uniforme de la época mogola.'),
 dict(key='IBERIAN-UNION',candidate='Bandera nacional única de la unión',reason='Unión de coronas y administraciones distintas. No se inventa un paño nacional común aEspaña yPortugal.'),
 dict(key='RUSSIA-TSARDOM',candidate='Flag of Russia.svg before1705',reason='La prescripción mercante de1705 no acredita uso uniforme desde1600. La enseña personal de1693 requiere un archivo y alcance propios.'),
 dict(key='HESSE-KASSEL',candidate='Arms of the house of Hesse-Kassel (1736-1803).svg',reason='Variante posterior; no se retrotraen armas específicas de1736 a1600.')]
if __name__=='__main__':
 code=(ROOT/'scripts/prepare-review-018-symbols.py').read_text(encoding='utf8');code=code.replace("TAG='symbols-review-0.18'","TAG='symbols-review-0.20'").replace('symbols018-pages.json','symbols020-pages.json').replace('symbols018-extra-','symbols020-extra-').replace('review-018-symbols.json','review-020-symbols.json')
 code=code.replace("json.loads((ROOT/'.cache/symbols020-pages.json').read_text(encoding='utf8'))", "(json.loads((ROOT/'.cache/symbols020-pages.json').read_text(encoding='utf8')) if (ROOT/'.cache/symbols020-pages.json').exists() else [])")
 code=code.replace("if not ii.get('url') or re.search(","if re.search(r'Category:[^\\n]*fictional',wiki,re.I):raise ValueError('Fictional category')\n    if not ii.get('url') or re.search(")
 code=code[:code.index('ROWS=[')]+code[code.index('\ndef main():'):];ns={'__file__':str(ROOT/'scripts/prepare-review-018-symbols.py'),'__name__':'symbols020','ROWS':ROWS,'PENDING':PENDING};exec(compile(code,'symbol-writer020','exec'),ns);ns['main']()
