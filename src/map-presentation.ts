import dictionary from '../public/data/display-labels.json';
const labels=dictionary.labels as Record<string,string>;
/** Editorial translation only: keys, aliases and source geometry remain unchanged. */
export function displayLabel(value:unknown):string{
 const name=String(value??'');if(labels[name])return labels[name];
 const person=name.match(/^(King|Queen|Duke|Duchess|Marquis|Marquess|Emperor|Empress) (.+?) of (.+)$/);
 if(person){const ranks:Record<string,string>={King:'Rey',Queen:'Reina',Duke:'Duque',Duchess:'Duquesa',Marquis:'Marqués',Marquess:'Marqués',Emperor:'Emperador',Empress:'Emperatriz'};return ranks[person[1]]+' '+person[2]+' de '+(labels[person[3]]??person[3]);}
 const prefixes:Record<string,string>={'Kingdom':'Reino','Empire':'Imperio','Republic':'República','Duchy':'Ducado','County':'Condado','Principality':'Principado','Sultanate':'Sultanato','Caliphate':'Califato','Emirate':'Emirato','Marquisate':'Marquesado','Federation':'Federación','Confederation':'Confederación'};
 const match=name.match(/^(Kingdom|Empire|Republic|Duchy|County|Principality|Sultanate|Caliphate|Emirate|Marquisate|Federation|Confederation) of (.+)$/);
 if(match)return prefixes[match[1]]+' de '+(labels[match[2]]??match[2]);
 return name;
}
const culturalTones=['#b89372','#9da96c','#b18eac','#82aa8b','#b9a468','#8ba8ba','#b67e76','#a6a579','#8c9fbd','#b6a18e','#98b3a0','#b49b69','#9d8fad','#7fa8a2','#b79988','#aaa36b'];
/** The former grey fallback was a missing palette choice, not missing people. */
export function culturalColor(p:Record<string,unknown>):unknown{
 if(!p.contextKey||p.color&&p.color!=='#879a9a')return p.color;
 let hash=2166136261;for(const c of String(p.contextKey))hash=Math.imul(hash^c.charCodeAt(0),16777619);
 return culturalTones[(hash>>>0)%culturalTones.length];
}
