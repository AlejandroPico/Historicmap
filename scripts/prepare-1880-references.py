"""Separate reference additions and administrative windows for the1880 extension.

Original1900 supplements and wartime preparation inputs remain immutable.
Greenland is an explicit omission correction through2019, not a new1880 state.
"""
import copy,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'public/data'
read=lambda f:json.loads((OUT/f).read_text(encoding='utf8'))
def save(f,d):(OUT/f).write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')

def prepare():
    originals=read('historical-supplements.geojson');features=[]
    for f in originals['features']:
        p=f['properties'];code=p.get('entityCode') or p.get('code')
        if code not in ['AND','LIE','MCO','SMR','KWT','BHR','TON'] or code=='TON' and p['start']>='1970':continue
        new=copy.deepcopy(f);new['id']=925001+len(features)
        new['properties'].update(start='1886-01-01',end='1899-12-31',coverageStartIsFloor=True,
            note='Contorno contemporáneo de referencia para una omisión del inventario1886–1899; no levantamiento de frontera del sigloXIX ni fecha de independencia.',
            referenceYear=2026,territorialReference=True)
        if code in ['KWT','BHR']:
            new['properties'].update(status='protected-monarchy',code='',administratorKey='',ownerName='',group=p['name'])
        if code=='TON':
            new['properties'].update(status='independent',politicalStatus='Monarquía tongana independiente',administratorKey='',ownerName='Tonga',group='Tonga')
        features.append(new)
    world=read('countries.geojson');greenland=copy.deepcopy(next(f for f in world['features'] if f['properties'].get('code')=='GRL'))
    greenland['id']=925000
    greenland['properties'].update(identityKey='GRL',entityCode='GRL',code='',name='Groenlandia',originalName='Greenland',
        status='dependent-territory',administratorKey='DNK',localAuthorityKey='GRL',ownerName='Dinamarca',group='Dinamarca',
        start='1886-01-01',end='2019-12-31',coverageStartIsFloor=True,territorialReference=True,referenceYear=2026,
        geometrySource='https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-0-countries/',
        source='https://stm.dk/statsministeriet/rigsfaellesskabet/groenland/?embed=true',
        politicalStatus='Territorio vinculado a Dinamarca · instituciones según la fecha',
        note='CShapes no incluye un registro deGroenlandia. Se utiliza el contorno de referenciaNaturalEarth, no una reconstrucción histórica. La vinculación danesa no implica autonomía idéntica antes1953,1979 o2009. No se atribuye ocupación alemana por la ocupación deDinamarca.')
    features.append(greenland)
    early=read('early-modern.geojson');hawaii=copy.deepcopy(next(f for f in early['features'] if f['properties']['name']=="Kingdom of Hawaï'i" and f['properties']['start']<=1885<=f['properties']['end']))
    hawaii['id']=925100
    hawaii['properties'].update(name='Hawaii',originalName='Hawaii',identityKey='HAW-KINGDOM',entityCode='HAW',code='',
        start='1886-01-01',end='1897-12-31',territorialReference=True,referenceYear=1885,
        source='https://github.com/Seshat-Global-History-Databank/cliopatria',geometrySource='https://github.com/Seshat-Global-History-Databank/cliopatria',
        geometrySourceLabel='Cliopatria · contorno de referencia1885',
        note='Islas omitidas porCShapes antes1898. Contorno deCliopatria1885 conservado como referencia para1886–1897; desde1898 se utiliza exclusivamenteCShapes. Monarquía, Gobierno provisional y república se resuelven por fecha; no se interpola un frente.')
    features.append(hawaii)
    save('historical-1880-supplements.geojson',dict(type='FeatureCollection',features=features,
         metadata=dict(license='Natural Earth public domain; Cliopatria CC BY4.0 for Hawaii',method='Unchanged reference contours; no source geography overwritten.')))
    # The1898/1899 incorporation must use the exact dated CShapes Hawaii
    # contour, not this coarser earlier reference: prepare-1880-islands.ts.

    records=[]
    def add(id,names,admin,local,start,label,source,note,end='1900-01-01',head=False,codes=None):
        records.append(dict(id='extension-1880-'+id,names=names,codes=codes or [],admin=admin,localKey=local,start=start,end=end,
                            label=label,source=source,note=note,headOfStateOnly=head))
    note='Los cargos nacionales del Estado administrador y los locales conservan ámbitos distintos. El límite de la ventana no acredita fundación o fin de la relación.'
    add('greenland',['Greenland','Groenlandia'],'DNK','GRL','1880-01-01','Groenlandia · administración y autonomía dentro del Reino de Dinamarca',
        'https://stm.dk/statsministeriet/rigsfaellesskabet/groenland/?embed=true',
        'Administración colonial antes1953, integración constitucional1953, autogobierno1979 y régimen de autonomía2009 son fases distintas. La ficha conserva autoridades locales cuando están documentadas y autoridades estatales danesas. No se inventa un presidente antes del autogobierno.',end='2020-01-01',codes=['GRL'])
    add('canada',['Canada'],'GBR','CAN','1880-01-01','Dominio de Canadá · Corona y Gobierno responsable',
        'https://www.canada.ca/en/canadian-heritage/services/crown-canada.html',note,head=True,codes=['CAN'])
    add('new-zealand',['New Zealand'],'GBR','NZL','1880-01-01','Colonia neozelandesa con Gobierno responsable',
        'https://nzhistory.govt.nz/politics/history-of-the-governor-general',note,codes=['NZL'])
    add('brunei',['Brunei','Sultanate of Brunei'],'GBR','BRN','1888-12-31','Sultanato bajo protección británica desde1888',
        'https://history.state.gov/countries/brunei',note+' Ventana anual desde el cierre1888, no día exacto de firma.',codes=['BRN'])
    add('kuwait',['Kuwait'],'GBR','KWT','1899-01-23','Jeque de Kuwait y acuerdo de protección británica',
        'https://history.state.gov/countries/kuwait',note,codes=['KWT'])
    add('bahrain',['Bahrain','Baréin','House of Khalifa'],'GBR','BHR','1880-01-01','Baréin · gobernante local y relaciones de protección británicas',
        'https://history.state.gov/countries/bahrain',note+' El acuerdo de1861 y el exclusivo de1892 no equivalen a una anexión.',codes=['BHR'])
    add('afghanistan',['Afghanistan','Emirate of Afghanistan'],'GBR','AFG','1880-01-01','Emirato afgano y control británico de relaciones exteriores',
        'https://www.nam.ac.uk/explore/third-afghan-war-and-revolt-waziristan',note+' Se conserva al emir como gobernante interno, no se denomina soberano afgano al monarca británico.',codes=['AFG'])
    add('egypt',['Egypt','Khedivate of Egypt'],'GBR','EGY','1882-12-31','Jedivato y ocupación militar británica',
        'https://www.nam.ac.uk/explore/war-egypt',note+' Observación anual de la ocupación iniciada1882; no anexión. La soberanía otomana nominal persiste.',codes=['EGY'])
    add('madagascar',['Madagascar (Malagasy)','Merina Kingdom'],'FRA','HIST-Q1071439','1896-08-06','Anexión francesa y final de la monarquía merina',
        'https://www.servicehistorique.sga.defense.gouv.fr/ark/493032',note+' La anexión6/8/1896 y abolición monárquica28/2/1897 son hechos distintos; no se prolongan reinas en el Gobierno colonial posterior.',codes=['MDG-MERINA'])
    for id,names,admin,local in [('angola',['Angola'],'PRT','ANG'),('mozambique',['Mozambique'],'PRT','MOZ'),('guinea-bissau',['Guinea Bissau','Guinea-Bissau'],'PRT','GNB'),('sahara',['Spanish Sahara'],'ESP',''),('surinam',['Surinam'],'NLD','SUR'),('guyana',['French Guyana'],'FRA','GUF'),('guadeloupe',['Guadeloupe'],'FRA','GLP'),('martinique',['Martinique'],'FRA','MTQ')]:
        add(id,names,admin,local,'1880-01-01','Autoridades locales y del Estado administrador',
            'https://icr.ethz.ch/data/cshapes/',note+' La base de1886–1899 documenta la relación, no un control interior homogéneo de toda la región desde1880.')
    save('historical-1880-administrations.json',dict(format='dated-territorial-administrations',referenceDate='2026-10-22',coverageStart='1880-01-01',records=records,
         license='Original factual compilation with individual institutional sources',intervals='Relation end exclusive; office intervals inclusive.'))
    return len(features),len(records)

if __name__=='__main__':
    print('1880 additions:',prepare())
