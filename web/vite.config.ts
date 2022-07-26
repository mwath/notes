import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { env } from "process";

// https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vite-plugin
import vuetify from "vite-plugin-vuetify";

const API_BASE_URL = env.API_BASE_URL || "";
const WEB_BASE_URL = env.WEB_BASE_URL || "";

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
  define: stringify({
    API_DOMAIN_NAME: env.API_DOMAIN_NAME,
    WEB_DOMAIN_NAME: env.WEB_DOMAIN_NAME,
    API_URL: `https://${env.API_DOMAIN_NAME}:${env.HTTPS_PORT}${API_BASE_URL}`,
    WEB_URL: `https://${env.WEB_DOMAIN_NAME}:${env.HTTPS_PORT}${WEB_BASE_URL}`,
  }),
});
