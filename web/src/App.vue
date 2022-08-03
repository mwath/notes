<template>
  <v-app :theme="theme.scheme">
    <v-navigation-drawer v-if="store.user" app permanent>
      <v-list>
        <v-list-item
          prepend-avatar="https://randomuser.me/api/portraits/men/78.jpg"
          :title="store.user.username"
          :subtitle="store.user.email"
        />
      </v-list>
      <v-divider />
      <v-list nav density="compact">
        <v-list-item
          v-for="item in items.filter((i) => !i.bottom)"
          :key="item.title"
          :title="item.title"
          :prepend-icon="item.icon"
          :to="item.url || `/${item.title.toLowerCase()}`"
        />
      </v-list>
      <v-divider />

      <template #append>
        <v-divider />
        <v-list nav density="compact">
          <v-list-item
            v-for="item in items.filter((i) => i.bottom)"
            :key="item.title"
            :title="item.title"
            :prepend-icon="item.icon"
            :to="item.url || `/${item.title.toLowerCase()}`"
          />
        </v-list>
      </template>
    </v-navigation-drawer>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { RouterView } from "vue-router";
import { useThemeStore } from "./stores/theme";
import { useStore } from "./stores/user";

const store = useStore();
const theme = useThemeStore();
const items = [
  { title: "Home", icon: "mdi-home", url: "/" },
  { title: "Search", icon: "mdi-magnify" },
  { title: "New Page", icon: "mdi-plus", url: "/new" },
  { title: "Settings", icon: "mdi-cog", bottom: true },
];
</script>

<style>
/* #app {
  height: 100vh;
} */
</style>
