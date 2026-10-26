import { defineConfig } from 'vitest/config';
export default defineConfig({ base: './', test:{include:['tests/*.test.ts'],maxWorkers:1,testTimeout:30000}, build: { target: 'esnext', chunkSizeWarningLimit: 1200 } });
