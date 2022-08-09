import { createPinia } from "pinia";
import { createApp } from "vue";
import App from "./App.vue";
import vuetify from "./plugins/vuetify";
import { loadFonts } from "./plugins/webfontloader";
import Toast, { PluginOptions } from "vue-toastification";

import router from "./router";

import "vue-toastification/dist/index.css";
import "./style.css";

loadFonts();

const app = createApp(App);
const pinia = createPinia();

app.use(vuetify).use(router).use(pinia).use(Toast).mount("#app");
