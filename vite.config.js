import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  base: "/build-a-modern-healthcare-management-dashboard-inspired-by-stripe-and-linear-the-ui-must-feature-a-s/",
  build: { outDir: "dist", assetsDir: "assets" },
  server: { port: 3000 },
});
