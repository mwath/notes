import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { env } from "process";

// https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vite-plugin
import vuetify from "vite-plugin-vuetify";
import path from "path";

const API_BASE_URL = env.API_BASE_URL || "";
const WEB_BASE_URL = env.WEB_BASE_URL || "";

const PORT = env.HTTPS_PORT ? `:${env.HTTPS_PORT}` : "";
const API_URL = `https://${env.API_DOMAIN_NAME}${PORT}${API_BASE_URL}`;
const WEB_URL = `https://${env.WEB_DOMAIN_NAME}${PORT}${WEB_BASE_URL}`;
const GATEWAY_URL = `wss://${env.API_DOMAIN_NAME}${PORT}${API_BASE_URL}/gateway`;

interface Env {
  [key: string]: string;
}

function stringify(env: Env): Env {
  for (const [key, value] of Object.entries(env))
    env[key] = JSON.stringify(value);

  return env;
}

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(), vuetify({ autoImport: true })],
  server: {
    hmr: {
      protocol: "wss",
      host: env.WEB_DOMAIN_NAME,
      clientPort: parseInt(env.HTTPS_PORT) || 443,
    },
    port: 3000,
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      $: path.resolve(__dirname, "./src/stores"),
    },
  },
  define: stringify({
    API_DOMAIN_NAME: env.API_DOMAIN_NAME,
    WEB_DOMAIN_NAME: env.WEB_DOMAIN_NAME,
    API_URL: API_URL,
    WEB_URL: WEB_URL,
    GATEWAY_URL: GATEWAY_URL,
  }),
});
