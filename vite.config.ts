import { defineConfig, type Plugin } from 'vitest/config';
import { writeEncyclopedia } from './scripts/build-encyclopedia.mjs';

/** Compila enciclopedia/_generado al arrancar y al cambiar páginas durante el desarrollo. */
function encyclopedia(): Plugin {
  const compile = () => { const r = writeEncyclopedia(); for (const e of r.errors) console.error('[enciclopedia] ' + e); };
  return {
    name: 'historicmap-encyclopedia',
    buildStart() { compile(); },
    configureServer(server) {
      const changed = (file: string) => {
        if (!/[\\/]enciclopedia[\\/]/.test(file) || /[\\/]_generado[\\/]/.test(file) || !file.endsWith('.md')) return;
        compile(); server.ws.send({ type: 'full-reload' });
      };
      server.watcher.on('add', changed); server.watcher.on('change', changed); server.watcher.on('unlink', changed);
    }
  };
}

export default defineConfig({ base: './', plugins: [encyclopedia()], test:{include:['tests/*.test.ts'],maxWorkers:1,testTimeout:30000}, build: { target: 'esnext', chunkSizeWarningLimit: 1200 } });
