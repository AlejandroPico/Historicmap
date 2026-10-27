"""Apply frozen visual review: an associated object is not automatically a portrait."""
import json,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf8'))
save=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
if __name__=='__main__':
 path=ROOT/'scripts/media-corrections-025.json';d=read(ROOT/'public/data/identities.json')
 if '--freeze'in sys.argv:
  media=read(ROOT/'.cache/new-media025.json');rejected=[];accepted=[]
  for index in [2,17,19,22,28,33,45,46,53,71,73,83,88,92,98,115,127,146,147,167,170,174,177,178,181,194,196,200,208,219,220,226]:
   m=media[index];people={l['person']for c in d['countries'].values()for l in c['leaders']if l.get('portrait',{}).get('file')==m['file']}
   for q in people:rejected.append(dict(person=q,title=m['title'],file=m['file'],reason='Visual review: associated object, text-only currency, unverified effigy, scene without an identifiable individual, or mismatched ruler (Bohemond V versus IV). Not adopted as a personal portrait.'))
  for index,caption in [(43,'Efigie del sello de Edgar de Escocia; reproducción, no fotografía del soberano.'),(62,'Efigie ecuestre de un sello de Vladislao II; reproducción documental.'),(63,'Efigie ecuestre del sello de Godofredo II de Bretaña.'),(64,'Efigie de sello de Conrado de Brandeburgo; reproducción documental.'),(100,'Efigie ecuestre del sello de Conan IV de Bretaña.'),(109,'Efigie ecuestre del sello de Pons de Trípoli.'),(120,'Efigie de sello de Federico de Bohemia; reproducción documental.'),(133,'Representación de Min Sithu como espíritu nat; imagen religiosa posterior, no retrato contemporáneo acreditado.'),(143,'Efigie del sello de Carlos VII de Suecia.'),(159,'Efigie ecuestre del sello de Amalarico de Lusignan.'),(180,'Medallón con efigie de Vladislao; representación posterior.'),(190,'Efigie ecuestre del sello de Enrique de Champaña.'),(205,'Efigie de sello de Alejandro I de Escocia; reproducción documental.'),(217,'Relieve de Angkor asociado a Suryavarman II; representación monumental.')]:
   m=media[index];people={l['person']for c in d['countries'].values()for l in c['leaders']if l.get('portrait',{}).get('file')==m['file']}
   for q in people:accepted.append(dict(person=q,title=m['title'],file=m['file'],caption=caption))
  save(path,dict(accepted=accepted,rejected=rejected,scope='Visual inspection of all228 newly acquired files; associated source objects remain attributed in the manifest but rejected pairs are absent from cards.'))
 review=read(path);bad={(r['person'],r['title'])for r in review['rejected']};captions={(r['person'],r['title']):r['caption']for r in review['accepted']}
 for c in d['countries'].values():
  for l in c['leaders']:
   if not l.get('portrait'):continue
   pair=(l['person'],l['portrait']['title'])
   if pair in bad:l.pop('portrait')
   elif pair in captions:l['portrait']['caption']=captions[pair]
 save(ROOT/'public/data/identities.json',d)
 p=ROOT/'scripts/media-exclusions.json';ex=read(p);pairs={(r['person'],r['title'])for r in ex}
 for r in review['rejected']:
  if(r['person'],r['title'])not in pairs:ex.append(r)
 save(p,ex);print('Rejected associated images',len(review['rejected']),'captioned effigies',len(review['accepted']))
