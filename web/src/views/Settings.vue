<template>
  <v-container>
    <v-row>
      <v-col>
        Thème
        <v-btn-toggle
          v-model="themeStore.theme"
          mandatory
          divided
          color="primary"
        >
          <v-btn value="dark" prepend-icon="mdi-moon-waning-crescent">
            Sombre
          </v-btn>
          <v-btn value="system" prepend-icon="mdi-theme-light-dark">
            Système
          </v-btn>
          <v-btn value="light" prepend-icon="mdi-white-balance-sunny">
            Clair
          </v-btn>
        </v-btn-toggle>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import { useThemeStore } from "../stores/theme";

const themeStore = useThemeStore();
</script>
