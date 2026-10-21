"""Acquire the exact source archives recorded in manifest.json; verify before extracting."""
import hashlib, io, json, lzma, pathlib, tarfile, urllib.request, zipfile
root=pathlib.Path(__file__).resolve().parents[1]
cache=root/'.cache'; cache.mkdir(exist_ok=True)
entries=json.loads((root/'public/data/manifest.json').read_text(encoding='utf8'))['entries']
def download(entry,name):
    path=cache/name
    if not path.exists():
        request=urllib.request.Request(entry['url'],headers={'User-Agent':'Historicmap source importer'})
        with urllib.request.urlopen(request,timeout=180) as response: path.write_bytes(response.read())
    if hashlib.sha256(path.read_bytes()).hexdigest()!=entry['sourceSha256']:
        raise ValueError(f'Source archive changed: {name}. Review upstream before explicitly updating the manifest.')
    return path
cs=next(e for e in entries if e['file']=='history.topojson')
archive=download(cs,'cshapes.tar.gz')
with tarfile.open(archive) as tar:
    raw=tar.extractfile('cshapes/inst/extdata/cshapes_2_gw.topojson.xz').read()
    (cache/'cshapes-topology.json').write_bytes(lzma.decompress(raw))
clio=next(e for e in entries if e['file']=='ww2.geojson')
archive=download(clio,'cliopatria.zip')
dest=cache/'cliopatria'; dest.mkdir(exist_ok=True)
with zipfile.ZipFile(archive) as zipped:
    members=[n for n in zipped.namelist() if n.endswith('.geojson')]
    if len(members)!=1: raise ValueError('Ambiguous source GeoJSON')
    (dest/pathlib.Path(members[0]).name).write_bytes(zipped.read(members[0]))
(cache/'cliopatria-sha.txt').write_text(clio['version'],encoding='utf8')
print('Verified CShapes and Cliopatria source archives; extracted only named data files.')
