<template>
  <v-container>
    <v-row justify="center" no-gutters>
      <h1>Créer une nouvelle page</h1>
    </v-row>
    <v-row v-if="error" no-gutters>
      <v-alert
        type="error"
        variant="outlined"
        icon="mdi-cloud-alert"
        :text="error"
        closable
      />
    </v-row>
    <v-row no-gutters>
      <v-text-field
        v-model="title"
        variant="solo"
        placeholder="Titre"
        counter
        :maxlength="50"
      />
    </v-row>
    <v-row no-gutters>
      <Editor />
    </v-row>
    <v-row justify="center">
      <v-btn color="primary" :loading="loading" @click="create()">
        Créer
      </v-btn>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import { usePageStore, Page } from "$/page";
import Editor from "@/components/Editor.vue";

const store = usePageStore();
const title = ref("");

const data = ref<Page>();
const error = ref<string>();
const loading = ref(false);

const create = () => {
  store.create({ title: title.value }, data, error, loading);
};
</script>
