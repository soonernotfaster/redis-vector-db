import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // Required based on https://github.com/vitejs/vite/issues/16522
    host: '127.0.0.1'
  }
})
