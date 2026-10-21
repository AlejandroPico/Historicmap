import { mkdir, writeFile, readFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
const root = new URL('../public/data/', import.meta.url);
await mkdir(root, { recursive: true });
async function json(url) {
  for (let attempt = 0; attempt < 4; attempt++) {
    try {
      const response = await fetch(url, { headers: { 'User-Agent': 'Historicmap/0.1 source importer' }, signal: AbortSignal.timeout(180000) });
      if (!response.ok) throw new Error(`${response.status}: ${url}`);
      return await response.json();
    } catch (error) {
      if (attempt === 3) throw error;
      await new Promise(resolve => setTimeout(resolve,1000*(attempt+1)));
    }
  }
}
const historical = await json('https://api.github.com/repos/aourednik/historical-basemaps/commits/master');
const natural = await json('https://api.github.com/repos/nvkelso/natural-earth-vector/commits/master');
// This importer owns only the original snapshot collection; retain newer layers.
const oldManifest = JSON.parse(await readFile(new URL('manifest.json',root)));
const entries = oldManifest.entries.filter(e=>!e.file.startsWith('coastlines-')&&!e.file.startsWith('world_')&&e.file!=='countries.geojson');
const historicalYears = [-10000,-3000,-1000,-500,100,500,1000,1492,1800,1914,1945,1994,2010];
const jobs = [
  {file:'countries.geojson', url:`https://raw.githubusercontent.com/nvkelso/natural-earth-vector/${natural.sha}/geojson/ne_10m_admin_0_countries.geojson`, source:'Natural Earth', version:natural.sha, license:'Public domain', year:2026},
  ...historicalYears.map(year => {
    const file = `world_${year < 0 ? `bc${-year}` : year}.geojson`;
    return {file, year, url:`https://raw.githubusercontent.com/aourednik/historical-basemaps/${historical.sha}/geojson/${file}`,source:'Historical Basemaps · A. Ourednik',version:historical.sha,license:'GPL-3.0'};
  }),
  ...[1,20,66,100,200,300,400,541,750,1000,1500,1800].map(ma => ({file:`coastlines-${ma}.geojson`,year:-ma*1e6,url:`https://gws.gplates.org/reconstruct/coastlines/?time=${ma}&model=CAO2024&wrap=true`,source:'GPlates / Cao et al. (2024)', version:'CAO2024; anchor_plate_id=0; wrap=true',license:'CC-BY-4.0 (model data; see docs/SOURCES.md)'})),
];
// Limit simultaneous requests to avoid overwhelming upstream scientific services.
for (let i = 0; i < jobs.length; i += 3) {
  await Promise.all(jobs.slice(i,i+3).map(async job => {
    const data = await json(job.url);
    if (data.type !== 'FeatureCollection' || !data.features?.length) throw new Error(`Empty or invalid: ${job.file}`);
    // Geometry coordinates remain intact; retain only properties used by this atlas.
    for (const [id, feature] of data.features.entries()) {
      const p = feature.properties ?? {};
      feature.id = id;
      const group = p.SUBJECTO || p.ADMIN || p.NAME || 'Continente';
      const color = [...group].reduce((hash,c)=>(Math.imul(hash,31)+c.charCodeAt(0))>>>0,0)%12;
      feature.properties = { name:p.NAME_ES || p.NAME || p.ADMIN || p.name || 'Masa continental', group, precision:p.BORDERPRECISION ?? null, code:p.ADM0_A3 || p.ISO_A3 || '', color };
    }
    const content = JSON.stringify(data);
    await writeFile(new URL(job.file,root), content);
    entries.push({...job, features:data.features.length, bytes:Buffer.byteLength(content), sha256:createHash('sha256').update(content).digest('hex')});
    console.log(`${job.file}: ${data.features.length} features`);
  }));
}
entries.sort((a,b)=>a.file.localeCompare(b.file));
await writeFile(new URL('manifest.json',root),JSON.stringify({importedAt:new Date().toISOString(),transform:'Property selection only; original geometry coordinates retained.',entries},null,2)+'\n');
