"""A documented institutional vacuum must not be replaced by a fictional president."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]/'public/data'
def read(f):return json.loads((root/f).read_text(encoding='utf-8'))
def save(f,v):(root/f).write_text(json.dumps(v,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8',newline='\n')
identities=read('identities.json')
identities['countries']['SOM']['territoryStatus']={
 'start':'1991-02-01','end':'1999-12-31',
 'text':'Tras la caída del Gobierno de Siad Barre en enero de 1991, Somalia carece de un Gobierno central efectivo. Hay autoridades regionales y facciones rivales. Los titulares reivindicados que aparecen en el registro no deben interpretarse como una presidencia con control de todo el país.',
 'source':'https://press.un.org/en/1999/19990902.stephen.doc.html',
}
save('identities.json',identities)
contexts=read('historical-context.json')
event={'id':'somalia-institutional-vacuum-1998-1999','title':'Somalia: ausencia de Gobierno central y autoridades regionales','type':'transition','start':'1998-01-01','end':'2000-01-01','countries':['SOM'],'text':'La ONU describe la ausencia de un Gobierno central reconocido y la persistencia de autoridades y facciones regionales. La ficha conserva el Estado como entidad territorial y explica el vacío institucional sin asignarle un presidente ficticio.','source':'https://press.un.org/en/1999/19990902.stephen.doc.html','sourceLabel':'ONU, Oficina Política para Somalia, 2 septiembre 1999','note':'Ventana anual 1998–1999, dentro del periodo posterior al colapso de 1991. No afirma ausencia de autoridades locales ni ausencia de conflicto.'}
contexts['events']=[e for e in contexts['events'] if e['id']!=event['id']]+[event]
save('historical-context.json',contexts)
print('Registered sourced Somali institutional vacuum without inventing a national officeholder.')
