"""Apply frozen visual review: an associated object is not automatically a portrait."""
import json,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf8'))
save=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
if __name__=='__main__':
 path=ROOT/'scripts/media-corrections-026.json';d=read(ROOT/'public/data/identities.json')
 if '--freeze'in sys.argv:
  media=read(ROOT/'.cache/new-media026.json');rejected=[];accepted=[]
  for index in [5, 16, 33, 35, 39, 42, 46, 49, 53, 57, 66, 70, 76, 77, 82, 89, 96, 108, 112, 124, 127, 128, 129, 145, 152, 154, 162, 163, 167, 168, 172]:
   m=media[index];people={l['person']for c in d['countries'].values()for l in c['leaders']if l.get('portrait',{}).get('file')==m['file']}
   for q in people:rejected.append(dict(person=q,title=m['title'],file=m['file'],reason='Visual review: associated object, text-only currency, unverified effigy, scene without an identifiable individual, or mismatched ruler (Bohemond V versus IV). Not adopted as a personal portrait.'))
  for index,caption in [(11, 'Miniatura de Gagik II ante Constantino IX; escena histórica, no retrato del natural.'), (12, 'Icono posterior de Vladímir y sus hijos; representación religiosa.'), (28, 'Representación histórica posterior de Olaf Tryggvason por Peter Nicolai Arbo.'), (51, 'Reconstrucción escultórica de Samuel de Bulgaria; no retrato contemporáneo.'), (60, 'Representación de Berenguer Ramón I en un pergamino genealógico posterior.'), (65, 'Representación de Roger I de Sicilia junto a Judith; imagen histórica posterior.'), (100, 'Efigie del sello de Roberto II; reproducción de un tipo documentado en1006–1030.'), (118, 'Retrato imaginario posterior de Macbeth por Jacob Jacobsz de Wet II; no acredita su apariencia real.'), (140, 'Efigie numismática atribuida a Anund Jacob en una reproducción; no fotografía del soberano.'), (143, 'Retrato familiar de Sviatoslav II en el Izbornik; no fotografía del soberano.')]:
   m=media[index];people={l['person']for c in d['countries'].values()for l in c['leaders']if l.get('portrait',{}).get('file')==m['file']}
   for q in people:accepted.append(dict(person=q,title=m['title'],file=m['file'],caption=caption))
  save(path,dict(accepted=accepted,rejected=rejected,scope='Visual inspection of all173 newly acquired files; associated source objects remain attributed in the manifest but rejected pairs are absent from cards.'))
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
