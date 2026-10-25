"""Resolve dated1880–1899 identities over two unchanged cartographic sources.

Names/QIDs in the early source sometimes identify a successor or an obsolete
regime. Explicit editorial corrections retain the original record and contour.
Unknown local series remain unknown; they never inherit a modern president.
"""
import json
import pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'public/data'
read=lambda p:json.loads(p.read_text(encoding='utf8'))

def prepare(identities):
    qids={}
    for key,c in identities['countries'].items():
        if c.get('qid'):
            qids.setdefault(c['qid'],key)
    rows=[]
    def row(names,key,label,code='',admin='',status='independent',source='',note='',first=1880,last=1899):
        rows.append(dict(names=names,key=key,label=label,entityCode=code or key,admin=admin,status=status,
                         start=first,end=last,source=source or 'https://github.com/Seshat-Global-History-Databank/cliopatria',note=note))
    # The explicit mapping takes precedence over unreliable source QIDs.
    row(['Empire of Brazil','Brazil'],'BRA-EMPIRE','Imperio del Brasil','BRAE',last=1888,
        source='https://mapa.an.gov.br/index.php/dicionario-periodo-imperial',note='Monarquía anterior a la proclamación republicana de noviembre1889; no utiliza dirigentes o símbolos de la república.')
    row(['Brazil'],'BRA','República de los Estados Unidos del Brasil','BRA',first=1889,
        source='https://www.gov.br/planalto/pt-br/conheca-a-presidencia/acervo/biblioteca-da-presidencia',note='La geometría de cierre1889 corresponde a la república. Los titulares anteriores del mismo año se identifican como predecesores, no miembros del Gobierno republicano.')
    row(['Joseon','Korea'],'JOS','Reino de Joseon','JOS',last=1896,note='La proclamación del Imperio coreano ocurrió el12/10/1897; el nombre imperial no se retrotrae a1880.',source='https://www.museum.go.kr/site/eng/home')
    row(['Korea'],'KEM','Imperio de Corea','KEM',first=1897,source='https://www.museum.go.kr/site/eng/home',note='Imperio proclamado en octubre1897. La referencia anual no convierte la proclamación en un cambio de costas.')
    row(['German Empire','Germany (Prussia)'],'DEU','Imperio alemán','DEU')
    row(['Russian Empire','Russia (Soviet Union)'],'RUE','Imperio ruso','RUE')
    row(['Austria-Hungary'],'AUT-HUN','Austria-Hungría · monarquía dual','AUH')
    row(['Qing Dynasty','Qing dynasty','China'],'QING','Imperio de la dinastía Qing','QNG')
    row(['Ottoman Empire','Turkey (Ottoman Empire)'],'OTT','Imperio otomano','OTT')
    row(['Kingdom of Italy','Italy/Sardinia'],'ITA','Reino de Italia','ITA')
    row(['Kingdom of Portugal','Portugal'],'PRT','Reino de Portugal','PRT')
    row(['Kingdom of Spain','Spain'],'ESP','Reino de España','ESP')
    row(['French Third Republic','France'],'FRA','Francia · Tercera República','FRA')
    row(['United States of America'],'USA','Estados Unidos','USA')
    row(['United Kingdom','Kingdom of Great Britain'],'GBR','Reino Unido','GBR',note='El nombre del registro temprano conserva una denominación anterior a1801; se corrige la identidad, no se acredita la exactitud de todo el contorno colonial.')
    row(['British Colonial Empire'],'HIST-Q8680','Colonias británicas · registro agrupado','',admin='GBR',status='colony',note='Registro colonial agrupado de la fuente. Las autoridades del Estado administrador no sustituyen una serie completa de gobernadores locales.')
    row(['British Africa'],'HIST-Q179848','África británica · registro agrupado','',admin='GBR',status='colony')
    row(['British Raj','India'],'IND','India británica · Raj','IND',admin='GBR',status='colony')
    row(['British Gold Coast'],'HIST-Q503623','Costa de Oro británica','',admin='GBR',status='colony')
    row(['British Cape Colony'],'HIST-Q370736','Colonia del Cabo','',admin='GBR',status='colony')
    row(['Trucial States'],'HIST-Q1852345','Estados de la Tregua','',admin='GBR',status='protectorate',note='Tratados de protección distintos de anexión. La geometría agrupada no identifica las fronteras interiores de cada emirato.')
    row(['Portuguese Colonies'],'HIST-Q200464','Colonias portuguesas · registro agrupado','',admin='PRT',status='colony')
    row(['French Africa'],'HIST-Q19951607','Posesiones francesas en África · registro agrupado','',admin='FRA',status='colony')
    row(['French Indochina'],'HIST-Q185682','Posesiones francesas en Indochina · referencia de fuente','',admin='FRA',status='colony',note='La Unión Indochina se constituyó en1887. La denominación agrupada anterior del inventario no acredita esa institución ni dominio francés de todos los territorios vietnamitas en1880.')
    row(['German Africa'],'HIST-Q5551337','África · contorno colonial alemán de fuente','',status='source-reference',note='La denominación alemana anterior a1884 es anacrónica. Este contorno de síntesis se conserva como referencia sin atribuirlo al Gobierno alemán ni inventar jefaturas locales; faltan fases territoriales acreditadas.')
    row(['Netherlands'],'NLD','Países Bajos','NLD')
    row(['Dutch East Indies'],'HIST-Q188161','Indias Orientales Neerlandesas','',admin='NLD',status='colony')
    row(['Netherlands Antilles'],'HIST-Q25227','Antillas neerlandesas · posesiones coloniales','',admin='NLD',status='colony',note='Denominación de agrupación territorial de la fuente; no se retrotrae el estatuto autónomo de1954.')
    row(['Denmark-Norway'],'DNK','Reino de Dinamarca','DNK',note='La unión Dinamarca-Noruega terminó en1814. Se corrige el nombre anacrónico del inventario, sin atribuir Noruega a Dinamarca en1880.')
    row(['United Kingdoms of Sweden and Norway'],'SWE','Unión de Suecia y Noruega','SWE',note='Unión de coronas y política exterior, no anexión de Noruega a un Estado sueco homogéneo. El inventario temprano agrupa su contorno.')
    row(['Kingdom of Belgium'],'BEL','Reino de Bélgica','BEL')
    row(['Swiss Confederation'],'CHE','Confederación Suiza','CHE')
    row(['Principality of Andorra'],'AND','Principado de Andorra','AND')
    row(['Kingdom of Monaco'],'MCO','Principado de Mónaco','MCO',note='El nombre Kingdom del inventario no corresponde al título del Estado.')
    row(['Empire of Haiti'],'HTI','República de Haití','HTI',note='La segunda monarquía imperial terminó en1859. No se asignan sus emperadores al territorio de1880.')
    row(['First Hellenic Republic'],'GRC','Reino de Grecia','GRC',note='La Primera República Helénica terminó en1832. En1880 Grecia era una monarquía.')
    row(['Argentine Confederation'],'ARG','República Argentina','ARG',note='El nombre de la antigua confederación se conserva sólo como denominación original de la fuente.')
    row(['Mexico'],'MEX','República de México','MEX',note='El QID del registro temprano remite a una entidad/región distinta; se aplica la identidad estatal documentada, sin usarlo para resolver dirigentes.')
    row(['United Principalities of Moldavia and Wallachia'],'ROU','Principado de Rumanía','ROU',last=1880)
    row(['United Principalities of Moldavia and Wallachia','Rumania'],'ROU','Reino de Rumanía','ROU',first=1881)
    row(['Kingdom of Serbia'],'SRK','Principado de Serbia','SRK',last=1881)
    row(['Kingdom of Serbia','Serbs'],'SRK','Reino de Serbia','SRK',first=1882,note='El identificador étnico Serbs no es una autoridad estatal: se conserva como dato original, resolviendo explícitamente el Estado.')
    row(['Montenegro'],'MNK','Principado de Montenegro','MNK')
    row(['Principality of Bulgaria'],'BGR','Principado de Bulgaria','BGR')
    row(["People's Republic of Zanzibar",'Zanzibar'],'ZAN','Sultanato de Zanzíbar','ZAN',note='La república popular corresponde a1964. El nombre anacrónico de la fuente no se usa para sus gobernantes del sigloXIX.')
    row(['Qajar Dynasty','Iran (Persia)'],'IRN','Persia · dinastía Qajar','IRN')
    row(['Emirate of Afghanistan','Afghanistan'],'AFG','Emirato de Afganistán','AFG')
    row(['Ethiopian Empire'],'ETH','Imperio etíope','ETH')
    row(['Rattanakosin Kingdom','Thailand'],'THA','Reino de Siam','THA')
    row(['House of Khalifa'],'BHR','Baréin · casa Al Jalifa','BHR')
    row(['Qatar Dynasty'],'QAT','Catar · emirato Al Thani','QAT')
    row(['Kingdom of Bhutan'],'BTN','Bhután · gobierno dual','BTN',note='La monarquía hereditaria Wangchuck se estableció en1907. No se retrotraen los cargos reales modernos.')
    row(['Sultanate of Oman'],'OMN','Sultanato de Mascate y Omán','OMN')
    row(['Sultanate of Brunei'],'BRN','Sultanato de Brunéi','BRN')
    row(["Kingdom of Hawaï'i",'Hawaii'],'HAW-KINGDOM','Reino de Hawái','HAW',last=1892)
    row(['Hawaii'],'HAW-PROVISIONAL','Hawái · Gobierno provisional','HAW-PROVISIONAL',first=1893,last=1893)
    row(['Hawaii'],'HAW-REPUBLIC','República de Hawái','HAW',first=1894,last=1897)
    row(['Hawaii'],'HAW','Hawái · administración tras anexión estadounidense','HAW',admin='USA',status='annexed-territory',first=1898)
    row(['Free Orange State','Orange Free State'],'ORF','Estado Libre de Orange','ORF')
    row(['South African Republic','Transvaal'],'TRV','República Sudafricana · Transvaal','TRV')
    row(['Natalia Republic'],'HIST-Q1029847','Natal · referencia territorial de fuente','',admin='GBR',status='colony',note='La República de Natalia terminó en1843. El nombre de la fuente no convierte Natal en una república boer independiente en1880.')
    row(['Talpur Dynasty'],'HIST-Q19569014','Sindh y Khairpur · referencia de fuente','',status='source-reference',note='La etiqueta dinástica no distingue el Sindh británico de Khairpur, donde continuó una rama principesca Talpur. El contorno no acredita soberanía homogénea; pendiente identificar el territorio exacto representado.')
    row(['Ottoman Tripolitania'],'HIST-Q1529261','Tripolitania otomana','',admin='OTT',status='province')
    row(['Khedivate of Egypt'],'EGY','Jedivato de Egipto','EGY',last=1881)
    row(['Khedivate of Egypt','Egypt'],'EGY','Egipto · ocupación británica y jedivato','EGY',admin='GBR',status='occupied',first=1882,note='Ocupación británica desde1882, distinta de la anexión y de la soberanía otomana nominal. La institución del jedive permanece.')
    row(['Merina Kingdom','Madagascar (Malagasy)'],'HIST-Q1071439','Reino merina · Madagascar','MDG-MERINA',last=1895)
    row(['Madagascar (Malagasy)'],'HIST-Q1071439','Madagascar · anexión francesa y fin de la monarquía','MDG-MERINA',admin='FRA',status='colony',first=1896,note='Anexión francesa6/8/1896; abolición de la monarquía28/2/1897. Las autoridades del mismo año conservan sus fechas y ámbitos.')
    row(['Zululand'],'ZUL','Zululandia · territorios fragmentados','ZUL',status='source-polity',note='La monarquía fue suprimida tras la guerra de1879; restauración limitada1883 y posterior fragmentación. No se dibuja un reino independiente uniforme a partir del título del inventario.')
    for name,key,label in [('Republic of Ecuador','ECU','Ecuador'),('Republic of Costa Rica','CRI','Costa Rica'),('Republic of El Salvador','SLV','El Salvador'),('Guatemala','GTM','Guatemala'),('Republic of Liberia','LBR','Liberia'),('Honduras','HND','Honduras'),('Republic of Nicaragua','NIC','Nicaragua'),('Dominican Republic','DOM','República Dominicana'),('Republic of Colombia','COL','Colombia'),('Oriental Republic of Uruguay','URY','Uruguay'),('Paraguay','PRY','Paraguay'),('Venezuela','VEN','Venezuela'),('Republic of Peru','PER','Perú'),('Republic of Chile','CHL','Chile'),('Bolivia','BOL','Bolivia'),('Nepal','NPL','Nepal'),('Greenland','GRL','Groenlandia'),('Swaziland','SWZ','Suazilandia')]:
        row([name,'Swaziland (Eswatini)'] if key=='SWZ' else [name],key,label,key,admin='DNK' if key=='GRL' else '',status='colony' if key=='GRL' else 'independent')
    return dict(format='dated-entity-resolution',coverageStart=1880,coverageEnd=1899,referenceDate='2026-10-25',
                qidKeys=qids,names={k:c['name'] for k,c in identities['countries'].items()},records=rows,
                source='https://github.com/Seshat-Global-History-Databank/cliopatria',
                license='CC0 (identity metadata); editorial historical corrections',
                note='Explicit identity corrections, not repaired geographic fronts. Original source names/QIDs retained. No successor statistics assigned to historical entities.')

if __name__=='__main__':
    d=prepare(read(OUT/'identities.json'))
    (OUT/'historical-1880-entities.json').write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
    print('Prepared1880 identity mapping',len(d['records']),'rules')
