import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  
  // 👇 ADD THIS SECTION for network access
  server: {
    // 0.0.0.0 binds to all network interfaces on your machine (LAN, localhost, etc.)
    host: '0.0.0.0', 
    // You can optionally specify a port, otherwise Vite defaults to 5173
    port: 3000, 
  }
})