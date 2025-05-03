import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import path from "path";
import { componentTagger } from "lovable-tagger";

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
  server: {
    host: "::",  // Allow connection on all network interfaces (IPv6).
    port: 8080,  // Port for the development server.
  },
  plugins: [
    react(),
    mode === 'development' && componentTagger(),  // Run componentTagger only in development mode.
  ].filter(Boolean),
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),  // Alias for src folder.
    },
  },
  build: {
    outDir: path.resolve(__dirname, './build'), // Output directory for production build.
  },
}));

