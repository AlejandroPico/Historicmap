"""Reviewed representative ensigns, dynastic devices and seals; not generic flags.

Reuses the accredited original-byte writer. Documentary types remain visible
and neither fictional designs nor later national flags are backdated.
"""
import pathlib,importlib.util,json
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('s',ROOT/'scripts/prepare-review-018-symbols.py');s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
ROWS=[]
def row(k,t,a,b,label,note):ROWS.append((k,t,a+'-01-01',b+'-12-31',label,note))
row('HABSBURG-MONARCHY','Flag of the Habsburg Monarchy.svg','1700','1799','Colores dinásticos','Referencia dinástica negra y amarilla; no bandera nacional moderna uniforme.')
row('HIST-Q12548','Banner of the Holy Roman Emperor without haloes (1400-1806).svg','1700','1799','Estandarte imperial','Enseña del emperador, distinta de los símbolos de cada Estado del Sacro Imperio.')
row('BAVARIA-ELECTORATE','Flag of the Electorate of Bavaria.svg','1700','1805','Pabellón heráldico del electorado','Reconstrucción heráldica representativa del electorado; no una norma nacional moderna.')
row('SAXONY-ELECTORATE','State flag of Saxony before 1815.svg','1700','1805','Pabellón del electorado','Variante de Sajonia anterior a1815. El título de rey no se anticipa al período electoral.')
row('HANOVER-ELECTORATE','Flag of Hanover (1692).svg','1700','1799','Estandarte del electorado','Caballo sajón de Hannover; no pabellón marítimo del reino posterior.')
row('WURTTEMBERG-DUCHY','Wappenflagge Herzogtum Württemberg.svg','1700','1802','Bandera de armas ducal','Reconstrucción del banner heráldico1495–1803. No se usan los colores del reino del sigloXIX.')
row('PRUSSIA','Flag of the Kingdom of Prussia (1701-1750).svg','1701','1749','Pabellón del reino','Diseño inicial anterior a la variante1750–1801; no se aplica al electorado antes de1701.')
row('PRUSSIA','Flag of the Kingdom of Prussia (1750-1801).svg','1750','1799','Pabellón del reino','Referencia anterior al cambio de1801; conserva atribución específica del autor.')
row('FRA','Royal Standard of the King of France.svg','1700','1788','Estandarte real','Enseña de la monarquía borbónica; no la bandera tricolor de la Revolución.')
row('PRT','Flag of Portugal (1667).svg','1700','1706','Pabellón de la monarquía','Variante anterior al cambio de armas de1707.')
row('PRT','Flag of Portugal (1707).svg','1707','1799','Pabellón de la monarquía','Variante de1707 anterior a la creación del Reino Unido de Portugal, Brasil y Algarves.')
row('ENGLAND','Flag of England.svg','1700','1706','Cruz de San Jorge','Enseña del reino anterior a la unión de1707; no se atribuye a Escocia.')
row('SCOTLAND','Flag of Scotland.svg','1700','1706','Cruz de San Andrés','Representación de la enseña escocesa; no pretende fijar una tonalidad digital normativa en1700.')
row('DENMARK-NORWAY','Flag of Denmark.svg','1700','1799','Dannebrog · pabellón de la monarquía','Referencia de la monarquía danesa-noruega; no implica una bandera noruega independiente moderna.')
row('DUTCH-REPUBLIC','Flag of the Netherlands.svg','1700','1794','Pabellón neerlandés','Tricolor de la República; los pabellones provinciales y de compañías eran distintos.')
row('PAPAL-STATES','Flag of the Papal States (pre 1808).svg','1700','1799','Pabellón pontificio','Colores rojo y amarillo anteriores a1808; no los colores actuales del Vaticano.')
row('MAR','Flag of Morocco (1666–1915).svg','1700','1799','Pabellón dinástico','Campo rojo alauí anterior a la estrella verde de1915.')
row('HIST-Q208169','Civil and merchant flag of the Republic of Ragusa (c. 1667-1807).svg','1700','1799','Pabellón civil y mercante','Referencia marítima de Ragusa; no una bandera de otro Estado adriático.')
row('NAPLES-BOURBON','Flag of Kingdom of Naples (1759-1806; 1815-1816).png','1759','1799','Pabellón real','Armas borbónicas de la etapa de FernandoIV; no se retrotrae a la etapa española o austriaca.')
row('OTT','Flag of the Ottoman Empire (also used in Egypt).svg','1793','1799','Pabellón otomano','Ventana posterior a1793; no se impone este diseño a todos los estandartes otomanos anteriores.')
row('RUSSIA-TSARDOM','Flag of Russia.svg','1705','1720','Pabellón mercante ruso','Tricolor blanco, azul y rojo prescrito por PedroI para buques mercantes en1705. No es la bandera imperial negra, amarilla y blanca del sigloXIX.')
row('RUE','Flag of Russia.svg','1721','1857','Pabellón mercante ruso','Tricolor mercante documentado desde1705. La presencia de esta enseña no equivale a una bandera estatal uniforme en todos los ámbitos.')
row('JPN','Tokugawa family crest.svg','1700','1853','Mon de los Tokugawa','Emblema dinástico de las tres hojas de malva del Gobierno shogunal; no una bandera nacional ni el supuesto pabellón naval de finales de la década de1860.')
row('QING','Plain Yellow Banner.svg','1700','1861','Enseña institucional · Bandera Amarilla','Reproducción representativa de una de las Ocho Banderas del imperio. No es una bandera nacional de toda China ni acredita normalización de este dibujo digital en1700.')
row('JOS','Joseongukwangjiin (The Seal of the King of Joseon, 1653-1776).svg','1700','1775','Sello del rey de Joseon','Reproducción del sello usado en la investidura real, con caracteres chinos y manchúes. Es un sello de autoridad, no una bandera nacional.')
row('JOS','Joseongukwangjiin (The Seal of the King of Joseon, 1776-1876).svg','1776','1875','Sello del rey de Joseon','Variante de1776 con escritura sigilar china y manchú. No se anticipa el Taegeukgi del sigloXIX.')
for k,a,b in [('AYUTTHAYA','1700','1766'),('THONBURI','1767','1781'),('THA','1782','1816')]:row(k,'Flag of Thailand (Ayutthaya period).svg',a,b,'Pabellón marítimo rojo','Enseña roja lisa de la navegación siamesa, documentada desde Ayutthaya. No significa que todos los estandartes reales fueran idénticos.')
row('HIST-Q83618','Flag of the Maratha Empire.svg','1710','1817','Enseña maratha · Bhagwa','Pabellón azafrán de cola de golondrina documentado en la navegación maratha del sigloXVIII. Ventana editorial interior; fecha de adopción exacta desconocida, no bandera nacional digital uniforme.')
row('IRN','Fath Ali Shah Flag.svg','1800','1833','Pabellón diplomático de Fath Alí Shah','Reproducción del pabellón diplomático atribuido a Fath Alí. Ventana interior de observación, no fecha de adopción exacta; distinto de los estandartes militares.')
row('GBR','Flag of Great Britain (1707–1800).svg','1707','1799','Bandera de la unión','Variante anterior a1801; no incorpora la cruz roja diagonal de la unión con Irlanda.')
row('HIST-Q157367','Flag of Brandenburg (1657-1701).svg','1700','1700','Enseña electoral','Gorro electoral, sin anticipar la corona real y los atributos de1701.')
row('HESSE-KASSEL','Arms of the house of Hesse-Kassel (1736-1803).svg','1736','1802','Armas del landgraviato','Variante heráldica1736–1803, no bandera nacional moderna.')
row('HESSE-DARMSTADT','Wappen-HD (1736–1804).svg','1736','1803','Armas del landgraviato','Variante1736–1804; no se adelantan los colores del gran ducado de1806.')
row('BRUNSWICK-WOLFENBUTTEL','Blason duché ni Brunswick.svg','1700','1799','Armas dinásticas','Leones de Brunswick como referencia heráldica, no una bandera nacional azul y amarilla posterior.')
row('MECKLENBURG-SCHWERIN','Wappen Mecklenburg-Schwerin 2.svg','1700','1799','Armas ducales','Armas de Mecklemburgo-Schwerin, sin anticipar la bandera de los grandes ducados del sigloXIX.')
for key in ['BADEN-DURLACH','BADEN-BADEN']:row(key,'Banner of Baden (3^2).svg','1700','1770','Bandera de armas de Baden','Colores heráldicos de la casa de Baden. No significa una administración unitaria de sus ramas ni una bandera nacional uniforme.')

PENDING=[
 dict(key='JPN',candidate='Flag of the Tokugawa Shogunate.svg',reason='La descripción corresponde a una atribución naval de finales de1860; se rechaza para1700 y1800. Se usa mon dinástico explícito.'),
 dict(key='QING',candidate='Flag of China (1889–1912).svg',reason='Bandera nacional posterior al período; se ofrece una enseña institucional identificada, no se backdata el pabellón nacional.'),
 dict(key='JOS',candidate='Flag of the king of Joseon.svg',reason='Diseño atribuido a1882. Para1700–1800 se documenta un sello de autoridad con su tipo explícito.'),
 dict(key='HIST-Q33296',candidate='Alam of the Mughal Empire.svg',reason='Categoría Green and yellow fictional flags. No se usa una reconstrucción de1840 como prueba de bandera uniforme en1700.'),
 dict(key='SAFAVID',candidate='Flag Safavid 1678.jpg',reason='El título no es una datación material: obra propia subida en2024 sin referencia independiente del diseño.'),
 dict(key='ZAND',candidate='Zand Ya Karim Flag.svg',reason='Requiere cotejo de la reproducción con testimonios históricos; un sitio partidista no basta como prueba independiente.'),
 dict(key='AFSHARID',candidate='Naval flag of Afsharid (Naderi Navy).png',reason='Diseño azul no cotejado con las enseñas descritas por el testimonio de1737 citado enIranica; no se adopta sin verificación.'),
 dict(key='HIST-Q696241',candidate='Banner of the Kokand Khans.svg',reason='Enseña blanca tradicional documentada bibliográficamente, pero ventana de uso aún por contrastar antes de retrotraerla a1709.'),
 dict(key='HIST-Q1139762',candidate='Flag of the Bornu Empire.svg',reason='El testimonio de1439 no demuestra continuidad1700–1800.'),
]

if __name__=='__main__':
 # Use the same original-byte and licensing checks, extended to fictional categories.
 code=(ROOT/'scripts/prepare-review-018-symbols.py').read_text(encoding='utf8')
 code=code.replace("TAG='symbols-review-0.18'","TAG='symbols-review-0.19'")
 code=code.replace("symbols018-pages.json","symbols019-pages.json").replace("symbols018-extra-","symbols019-extra-").replace("review-018-symbols.json","review-019-symbols.json")
 code=code.replace("json.loads((ROOT/'.cache/symbols019-pages.json').read_text(encoding='utf8'))", "(json.loads((ROOT/'.cache/symbols019-pages.json').read_text(encoding='utf8')) if (ROOT/'.cache/symbols019-pages.json').exists() else [])")
 code=code.replace("Absent, unverified or disputed design","Absent, unverified or disputed design")
 code=code.replace("title=='Flag of the Kingdom of Prussia (1750-1801).svg'", "title in ['Flag of the Kingdom of Prussia (1750-1801).svg','Flag of the Kingdom of Prussia (1701-1750).svg']")
 code=code.replace("if not ii.get('url') or re.search(","if re.search(r'Category:[^\\n]*fictional',wiki,re.I):raise ValueError('Fictional category')\n    if not ii.get('url') or re.search(")
 # Remove only the declaration blocks; the writer itself remains unchanged.
 code=code[:code.index('ROWS=[')]+code[code.index('\ndef main():'):]
 ns={'__file__':str(ROOT/'scripts/prepare-review-018-symbols.py'),'__name__':'symbol_writer','ROWS':ROWS,'PENDING':PENDING}
 exec(compile(code,'reviewed-symbol-writer019','exec'),ns);ns['main']()
 data=json.loads((ROOT/'public/data/identities.json').read_text(encoding='utf8'))
 evidence={
  'RUE':'https://www.prlib.ru/news/1163137','RUSSIA-TSARDOM':'https://www.prlib.ru/news/1163137',
  'JPN':'https://www.edo-tokyo-museum.or.jp/assets/img/2021/07/oedo_list_E.pdf',
  'HIST-Q83618':'https://www.cambridge.org/core/books/abs/naval-resistance-to-britains-growing-power-in-india-16601800/introduction/8AF86A549E63B833D45579154D4CB2F3',
  'IRN':'https://www.iranicaonline.org/articles/flags-i/'}
 for k,url in evidence.items():
  for f in data['countries'][k]['flags']:
   if f.get('acquisition')=='symbols-review-0.19':f['source']=url;f['media']['symbolEvidenceURL']=url
 s.h.save(ROOT/'public/data/identities.json',data)
