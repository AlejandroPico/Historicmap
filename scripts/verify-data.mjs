import { readFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
const root = new URL('../public/data/',import.meta.url);
const manifest = JSON.parse(await readFile(new URL('manifest.json',root),'utf8'));
if (manifest.entries.length !== 26) throw new Error('Expected 26 cartographic snapshots');
for (const entry of manifest.entries) {
  const bytes = await readFile(new URL(entry.file,root));
  if (createHash('sha256').update(bytes).digest('hex') !== entry.sha256) throw new Error(`Checksum mismatch ${entry.file}`);
  const data = JSON.parse(bytes);
  if (data.type !== 'FeatureCollection' || data.features.length !== entry.features) throw new Error(`Invalid ${entry.file}`);
  if (!entry.license || !entry.url || !entry.version) throw new Error(`Missing provenance ${entry.file}`);
}
console.log(`Verified ${manifest.entries.length} snapshots, provenance and SHA-256.`);
