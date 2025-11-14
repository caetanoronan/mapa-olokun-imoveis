import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  base: '/mapa-olokun-imoveis/', // Nome do repositório no GitHub
});
