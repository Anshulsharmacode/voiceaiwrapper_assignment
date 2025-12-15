import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  // Build assets under /static/ so Django can serve them via STATIC_URL
  base: "/static/",
})
