"""Read named office candidates from their canonical entity folders."""
import pathlib,json,types
ROOT=pathlib.Path(__file__).resolve().parents[1]
GROUPS=[]
for p in sorted((ROOT/'Países').glob('*/periodos/0900-0999.json')):
 d=json.loads(p.read_text(encoding='utf8'))
 GROUPS.extend((d['key'],c['role'],c['titles'])for c in d.get('candidates',[]))
r=types.SimpleNamespace(GROUPS=GROUPS)
if __name__=='__main__':
 errors=[dict(key=k,role=role,title=t)for k,role,ts in GROUPS for t in ts]
 (ROOT/'.cache/rulers027-candidates.json').write_text(json.dumps(dict(records=[],errors=errors),ensure_ascii=False,indent=2)+'\n',encoding='utf8')
