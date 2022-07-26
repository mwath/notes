/// <reference types="vite/client" />

declare const API_DOMAIN: string;
declare const WEB_DOMAIN: string;
declare const API_PORT: string;
declare const WEB_PORT: string;
declare const API_URL: string;
declare const WEB_URL: string;

declare module "*.vue" {
  import type { DefineComponent } from "vue";
  const component: DefineComponent<{}, {}, any>;
  export default component;
}
