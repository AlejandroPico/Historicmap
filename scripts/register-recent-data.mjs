import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
const root=new URL('../public/data/',import.meta.url);
const manifest=JSON.parse(await readFile(new URL('manifest.json',root)));
const specifications={
 'recent-control.geojson':{source:'CShapes 2.0 GW geometry and United Nations UNIKOM historical account',url:'https://peacekeeping.un.org/sites/default/files/past/unikom/background.html',license:'CC-BY-NC-SA-4.0 (CShapes geometry); original factual annotation',transform:'Kuwait occupation by Iraq at annual close 1990. Exact CShapes outline active in 1990, not the later demarcation. Underlying Kuwaiti territory remains separate; layer toggles occupation paint. Not active at annual close 1991; no interpolated campaign fronts.'},
 'affiliations.json':{format:'dated-organizations',source:'Official institutional membership chronologies and declarations',url:'https://www.nato.int/cps/en/natohq/topics_52044.htm',license:'Factual membership metadata; sources per interval, original editorial compilation',transform:'27 regional/intercontinental organizations; dated membership and category intervals, end exclusive. Annual map at Dec 31 capped at acquisition; country card lists every relationship overlapping year. Separate suspension/associate/partner status; historical state codes are not successor statistics. Source-year observations explicitly noted. See docs/HISTORICAL-AFFILIATIONS.md.'},
 'historical-context.json':{format:'dated-historical-context',source:'United Nations, institutional and government historical records',url:'https://www.un.org/en/about-us/history-of-the-un',license:'Original editorial summaries; institutional sources linked per event',transform:'Selected sourced transitions and conflict phases; start inclusive, end exclusive, not a global belligerency classification or front-line geometry. Annual selection by interval; absence is not peace. See docs/HISTORICAL-CONTEXT.md.'},
 'historical-supplements.geojson':{source:'Natural Earth pinned country outlines; UN territorial/state chronology and Office of the Historian',url:'https://www.naturalearthdata.com/about/terms-of-use/',license:'Public domain (Natural Earth geometry); factual institutional metadata',transform:'23 explicit contemporary reference outlines for states/territory omitted by CShapes, 1990–2019. Coordinates unchanged. Coverage floor is not independence date. Palau from 1994-10-01. Western Sahara separate UN non-self-governing territory; no invented control line. Each card identifies outline as reference, not historical survey.'},
};
for(const [file,spec] of Object.entries(specifications)){
 const bytes=await readFile(new URL(file,root)),data=JSON.parse(bytes);
 const entry={file,bytes:bytes.length,sha256:createHash('sha256').update(bytes).digest('hex'),version:`Historicmap 0.6; reference ${data.referenceDate??'2026-10-22'}`,...spec,...(data.features?{features:data.features.length}:{}),...(data.organizations?{organizations:data.organizations.length,records:data.organizations.reduce((n,o)=>n+o.memberships.length,0)}:{}),...(data.events?{records:data.events.length}:{})};
 manifest.entries=manifest.entries.filter(e=>e.file!==file);manifest.entries.push(entry);
}
manifest.entries.sort((a,b)=>a.file.localeCompare(b.file));
await writeFile(new URL('manifest.json',root),JSON.stringify(manifest,null,2)+'\n');
console.log('Registered dated organizations, historical contexts and explicit outline supplements.');
