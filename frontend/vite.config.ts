import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    hmr: true,
    watch: {
      usePolling: true
    }
  },
  optimizeDeps: {
    force: true
  },
  clearScreen: false
}) 