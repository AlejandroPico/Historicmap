"""Acquire an expressly licensed official photograph, preserving every byte.

CC BY-NC-ND 3.0 RS: noncommercial collection, full frame, no edits/crops.
Source page identifies both prime ministers, photographer and site license.
"""
import datetime,hashlib,json,pathlib,urllib.request
root=pathlib.Path(__file__).resolve().parents[1]
source='https://www.srbija.gov.rs/vest/en/286105/serbia-mozambique-strengthening-bilateral-relations.php'
url='https://www.srbija.gov.rs/extimages/en/286/111/main_webp_auto_generated_macut-mozambik-wetransfer_1000037583-jpg_2026-08-31_1254_2026_08_31_2026_7.webp'
file='media/portrait-'+hashlib.sha256(url.encode()).hexdigest()[:20]+'.webp'
path=root/'public'/file
if not path.exists():
    request=urllib.request.Request(url,headers={'User-Agent':'Historicmap/0.5 (https://github.com/AlejandroPico/Historicmap)'})
    raw=urllib.request.urlopen(request,timeout=45).read()
    if len(raw)>5_000_000 or raw[:4]!=b'RIFF' or raw[8:12]!=b'WEBP':raise ValueError('Unexpected official image format')
    path.write_bytes(raw)
raw=path.read_bytes()
media=dict(file=file,title='Serbia, Mozambique strengthening bilateral relations',url=source,sourceUrl=url,artist='Slobodan Miljević',license='CC BY-NC-ND 3.0 RS',licenseUrl='https://creativecommons.org/licenses/by-nc-nd/3.0/rs/deed.en',attribution='Slobodan Miljević / Gobierno de la República de Serbia · «Serbia, Mozambique strengthening bilateral relations» · CC BY-NC-ND 3.0 RS. Sin modificaciones.',attributionRequired=True,credit='Gobierno de la República de Serbia, 31 de agosto de 2026',display='full-frame',caption='Maria Benvinda Levi (izquierda) con Đuro Macut, Belgrado, 31 de agosto de 2026. Fotografía íntegra.',sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw))
dataPath=root/'public/data/identities.json';data=json.loads(dataPath.read_text(encoding='utf8'))
for country in data['countries'].values():
    for leader in country['leaders']:
        if leader['person']=='Q6761049':leader['portrait']=media
dataPath.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
manifestPath=root/'public/media/manifest.json';manifest=json.loads(manifestPath.read_text(encoding='utf8'))
manifest['entries']=[m for m in manifest['entries'] if m['file']!=file]+[media]
manifest['entries'].sort(key=lambda m:m['file'])
manifestPath.write_text(json.dumps(manifest,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
auditPath=root/'.cache/identities/current-authorities-audit.json'
if auditPath.exists():
    audit=json.loads(auditPath.read_text(encoding='utf8'))
    audit['portraitPeople']=audit['portraitPeople']+sum(m['person']=='Q6761049' for m in audit['missing'])
    audit['missing']=[m for m in audit['missing'] if m['person']!='Q6761049']
    audit['mediaTotal']=len(manifest['entries'])
    auditPath.write_text(json.dumps(audit,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
print('Official full-frame photograph acquired; no transformation:',file)
