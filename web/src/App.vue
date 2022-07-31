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
          v-for="item in items"
          :key="item.title"
          :title="item.title"
          :prepend-icon="item.icon"
          :to="item.url || `/${item.title.toLowerCase()}`"
        />
      </v-list>
      <v-divider />

      <template #append>
        <v-list>
          <v-list-item
            title="Change Theme"
            prepend-icon="mdi-theme-light-dark"
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
  { title: "Dashboard", icon: "mdi-view-dashboard" },
  { title: "Account", icon: "mdi-account" },
  { title: "Settings", icon: "mdi-cog" },
];
</script>

<style>
/* #app {
  height: 100vh;
} */
</style>
