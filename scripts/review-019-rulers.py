"""Named sovereign research: retain all Reign fields for explicit office review."""
import pathlib,json,importlib.util,concurrent.futures,urllib.parse,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('r',ROOT/'scripts/review-018-german-rulers.py');r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
h=r.h
GROUPS=[
 ('PRUSSIA','Rey de Prusia',['Frederick I of Prussia','Frederick William I of Prussia','Frederick II of Prussia','Frederick William II of Prussia','Frederick William III of Prussia']),
 ('SAXONY-ELECTORATE','Elector de Sajonia',['Augustus II the Strong','Augustus III of Poland','Frederick Christian, Elector of Saxony','Frederick Augustus I of Saxony']),
 ('BAVARIA-ELECTORATE','Elector de Baviera',['Maximilian II Emanuel, Elector of Bavaria','Charles VII, Holy Roman Emperor','Maximilian III Joseph, Elector of Bavaria','Charles Theodore, Elector of Bavaria','Maximilian I Joseph of Bavaria']),
 ('HESSE-KASSEL','Landgrave de Hesse-Kassel',['Charles I, Landgrave of Hesse-Kassel','Frederick I of Sweden','William VIII, Landgrave of Hesse-Kassel','Frederick II, Landgrave of Hesse-Kassel','William I, Elector of Hesse']),
 ('HESSE-DARMSTADT','Landgrave de Hesse-Darmstadt',['Ernest Louis, Landgrave of Hesse-Darmstadt','Louis VIII, Landgrave of Hesse-Darmstadt','Louis IX, Landgrave of Hesse-Darmstadt','Louis I, Grand Duke of Hesse']),
 ('WURTTEMBERG-DUCHY','Duque de Wurtemberg',['Eberhard Louis, Duke of Württemberg','Charles Alexander, Duke of Württemberg','Charles Eugene, Duke of Württemberg','Louis Eugene, Duke of Württemberg','Frederick II Eugene, Duke of Württemberg','Frederick I of Württemberg']),
 ('BADEN-DURLACH','Margrave de Baden-Durlach',['Frederick VII, Margrave of Baden-Durlach','Charles III William, Margrave of Baden-Durlach','Charles Frederick, Grand Duke of Baden']),
 ('BADEN-BADEN','Margrave de Baden-Baden',['Louis William, Margrave of Baden-Baden','Louis George, Margrave of Baden-Baden','Augustus George, Margrave of Baden-Baden']),
 ('LIPPE-COUNTY','Conde de Lippe',['Frederick Adolph, Count of Lippe','Simon Henry Adolph, Count of Lippe','Simon August, Count of Lippe','Leopold I, Prince of Lippe']),
 ('SAXE-WEIMAR','Duque de Sajonia-Weimar',['William Ernest, Duke of Saxe-Weimar','Ernest Augustus I, Duke of Saxe-Weimar-Eisenach','Ernest Augustus II, Duke of Saxe-Weimar-Eisenach','Charles Augustus, Grand Duke of Saxe-Weimar-Eisenach']),
 ('BRUNSWICK-WOLFENBUTTEL','Duque de Brunswick-Wolfenbüttel',['Anthony Ulrich, Duke of Brunswick','Augustus William, Duke of Brunswick','Louis Rudolph, Duke of Brunswick','Ferdinand Albert II, Duke of Brunswick','Charles I, Duke of Brunswick-Wolfenbüttel','Charles William Ferdinand, Duke of Brunswick']),
 ('MECKLENBURG-SCHWERIN','Duque de Mecklemburgo-Schwerin',['Frederick William, Duke of Mecklenburg-Schwerin','Charles Leopold, Duke of Mecklenburg-Schwerin','Christian Ludwig II, Duke of Mecklenburg-Schwerin','Frederick II, Duke of Mecklenburg-Schwerin','Frederick Francis I, Grand Duke of Mecklenburg-Schwerin']),
 ('MECKLENBURG-STRELITZ','Duque de Mecklemburgo-Strelitz',['Adolphus Frederick II, Duke of Mecklenburg-Strelitz','Adolphus Frederick III, Duke of Mecklenburg-Strelitz','Adolphus Frederick IV, Duke of Mecklenburg-Strelitz','Charles II, Grand Duke of Mecklenburg-Strelitz']),
 ('HANOVER-ELECTORATE','Elector de Hannover',['Ernest Augustus, Elector of Hanover','George I of Great Britain','George II of Great Britain','George III']),
 ('HABSBURG-MONARCHY','Soberano de los dominios de los Habsburgo',['Leopold I, Holy Roman Emperor','Joseph I, Holy Roman Emperor','Charles VI, Holy Roman Emperor','Maria Theresa','Joseph II, Holy Roman Emperor','Leopold II, Holy Roman Emperor','Francis II, Holy Roman Emperor']),
]
ENTITY_TITLES={'BAVARIA-ELECTORATE':'Electorate of Bavaria','SAXONY-ELECTORATE':'Electorate of Saxony','HESSE-KASSEL':'Landgraviate of Hesse-Kassel','HESSE-DARMSTADT':'Landgraviate of Hesse-Darmstadt','WURTTEMBERG-DUCHY':'Duchy of Württemberg','BADEN-DURLACH':'Margraviate of Baden-Durlach','BADEN-BADEN':'Margraviate of Baden-Baden','LIPPE-COUNTY':'County of Lippe','SAXE-WEIMAR':'Saxe-Weimar','BRUNSWICK-WOLFENBUTTEL':'Principality of Brunswick-Wolfenbüttel','MECKLENBURG-SCHWERIN':'Duchy of Mecklenburg-Schwerin','MECKLENBURG-STRELITZ':'Duchy of Mecklenburg-Strelitz','HANOVER-ELECTORATE':'Electorate of Hanover','SAVOY-DUCHY':'Duchy of Savoy','THONBURI':'Thonburi Kingdom'}

def main():
 replacements={'Simon Henry Adolph, Count of Lippe':'Simon Henry Adolph, Count of Lippe-Detmold','Simon August, Count of Lippe':'Simon August, Count of Lippe-Detmold','Augustus William, Duke of Brunswick':'Augustus William, Duke of Brunswick-Lüneburg'}
 GROUPS.append(('HIST-Q12548','Emperador del Sacro Imperio',['Francis I, Holy Roman Emperor']))
 rows=[(key,role,replacements.get(title,title)) for key,role,titles in GROUPS for title in titles];out=[];errors=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  for row,v in zip(rows,pool.map(r.safe,rows)):
   if isinstance(v,dict):out.append(v)
   else:errors.append(dict(title=row[2],error=v))
 all_titles=list(dict.fromkeys([v['title'] for v in out]+list(ENTITY_TITLES.values())));entities=[]
 for offset in range(0,len(all_titles),20):
  group=all_titles[offset:offset+20];params=dict(action='wbgetentities',sites='enwiki',titles='|'.join(group),props='labels|claims|sitelinks',redirects='yes',format='json');d=h.get('https://www.wikidata.org/w/api.php?'+urllib.parse.urlencode(params),'rulers019-meta-'+hashlib.sha256('|'.join(group).encode()).hexdigest()[:18])
  for q,e in d.get('entities',{}).items():
   if 'missing' in e:continue
   title=e.get('sitelinks',{}).get('enwiki',{}).get('title');h.save(h.CACHE/('historical-entity-'+q+'.json'),dict(entities={q:e}))
   for v in out:
    if v['title']==title:v.update(person=q,name=h.label(e),human=any(t.get('id')=='Q5' for t in h.values(e,'P31') if isinstance(t,dict)))
   for key,t in ENTITY_TITLES.items():
    if title==t:entities.append(dict(key=key,qid=q,name=h.label(e),title=title))
 for v in out:print(v['key'],v.get('person'),v['title'],v['parsed'],flush=True)
 h.save(ROOT/'.cache/rulers019-candidates.json',dict(records=out,entities=entities,errors=errors));print('Polity identities',entities,'errors',errors,flush=True)
if __name__=='__main__':main()
