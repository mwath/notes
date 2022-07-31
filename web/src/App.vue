<template>
    <v-navigation-drawer app permanent>
  <v-app :theme="theme.scheme">
      <v-list>
        <v-list-item
          prepend-avatar="https://randomuser.me/api/portraits/men/78.jpg"
          title="Mitchell Admin"
          subtitle="mitchell@gmail.com"
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

const theme = useThemeStore();
const items = [
  { title: "Home", icon: "mdi-home", url: "/" },
  { title: "Settings", icon: "mdi-cog", bottom: true },
];
</script>

<style>
/* #app {
  height: 100vh;
} */
</style>
