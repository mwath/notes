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
        <v-list-item title="Home" prepend-icon="mdi-home" to="/" />
        <v-list-item title="Search" prepend-icon="mdi-magnify" to="/search" />
        <v-list-item
          title="New Page"
          prepend-icon="mdi-plus"
        />
      </v-list>
      <v-divider />

      <template #append>
        <v-divider />
        <v-list nav density="compact">
          <v-list-item title="Settings" prepend-icon="mdi-cog" to="/settings" />
        </v-list>
      </template>
    </v-navigation-drawer>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { RouterView, useRouter } from "vue-router";
import { Page, usePageStore } from "./stores/page";
import { useThemeStore } from "./stores/theme";
import { useStore } from "./stores/user";

const store = useStore();
const theme = useThemeStore();
</script>

<style>
/* #app {
  height: 100vh;
} */
</style>
