<template>
  <v-app :theme="$theme.scheme">
    <v-navigation-drawer v-if="$user.user" app permanent>
      <v-list>
        <v-list-item
          prepend-avatar="https://randomuser.me/api/portraits/men/78.jpg"
          :title="$user.user.username"
          :subtitle="$user.user.email"
        />
      </v-list>
      <v-divider />
      <v-list nav density="compact">
        <v-list-item title="Home" prepend-icon="mdi-home" to="/" />
        <v-list-item title="Search" prepend-icon="mdi-magnify" to="/search" />
        <v-list-item
          title="New Page"
          prepend-icon="mdi-plus"
          @click="create()"
          :disabled="loading"
        />
      </v-list>
      <v-divider />
      <v-list nav density="compact">
        <v-list-item
          v-for="page in $pages.pages"
          :key="page.id"
          :title="page.title"
          :to="getPageUrl(page)"
        />
      </v-list>

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
import { onMounted, ref } from "vue";
import { RouterView, useRouter } from "vue-router";
import { Page, getPageUrl, usePageStore } from "./stores/page";
import { useThemeStore } from "./stores/theme";
import { useUserStore } from "./stores/user";
import { useToast } from "vue-toastification";

const $user = useUserStore();
const $theme = useThemeStore();
const $pages = usePageStore();
const router = useRouter();

const data = ref<Page>();
const error = ref<string>();
const loading = ref(false);
const toast = useToast();

const create = async () => {
  await $pages.create({ title: "Nouvelle Page" }, data, error, loading);

  if (error.value) {
    toast.error(error.value);
  } else if (data.value) {
    router.push(getPageUrl(data.value));
  }
};

onMounted(() => {
  $pages.list_pages();
});
</script>

<style>
/* #app {
  height: 100vh;
} */
</style>
