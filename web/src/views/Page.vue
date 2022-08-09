<template>
  <NotFound v-if="notfound" />
  <v-container v-else>
    <v-row no-gutters>
      <h1 contenteditable>
        {{ page?.title }}
      </h1>
    </v-row>
    <v-row no-gutters>
      <Editor />
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import Editor from "@/components/Editor.vue";
import { usePageStore, Page } from "@/stores/page";
import { computed, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { useToast } from "vue-toastification";
import NotFound from "../components/NotFound.vue";

const toast = useToast();
const $page = usePageStore();
const route = useRoute();
const params = computed(() => route.params as { id: string; title?: string });

const page = ref<Page>();
const error = ref<string>();
const notfound = ref(false);

watch(error, (value) => {
  if (value) toast.error(value);
});

onMounted(() => {
  const id = parseInt(params.value.id);

  if (!(notfound.value = isNaN(id))) {
    $page.get(id, page, error);
  }
});
</script>
