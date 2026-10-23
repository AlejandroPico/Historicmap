// Reproducible review artifact. This is our editorial palette, not the missing attached CSV.
import {writeFile} from 'node:fs/promises';
import {historicalPalette} from '../src/historical-palette.ts';
const rows=[['Entidad','Clave','Color','Naturaleza'],...historicalPalette.map(r=>[r.names[0],r.key,r.color,'Convención editorial; no ideología'])];
await writeFile(new URL('../docs/POLITICAL-PALETTE.csv',import.meta.url),rows.map(row=>row.map(v=>'"'+String(v).replaceAll('"','""')+'"').join(',')).join('\n')+'\n');
console.log('Exported',rows.length-1,'editorial families. Regime samples remain in political.ts. This is not the unavailable attached CSV.');
