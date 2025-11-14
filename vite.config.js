import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  base: '/mapa-int-imob-caetano-ronan/', // Substitua pelo nome exato do seu repositório no GitHub
});
