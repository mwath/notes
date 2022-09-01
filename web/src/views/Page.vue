<template>
  <NotFound v-if="notfound" />
  <v-container v-else-if="showSettings">
    <v-row class="my-4" justify="space-between">
      <v-btn
        prepend-icon="mdi-subdirectory-arrow-left"
        @click="showSettings = !showSettings"
      >
        Retour à l'édition
      </v-btn>

      <v-btn
        v-if="page"
        variant="outlined"
        :color="page.active ? 'error' : 'secondary'"
        :prepend-icon="`mdi-archive-arrow-${
          page.active ? 'down' : 'up'
        }-outline`"
        :disabled="!page"
        @click="(page!.active ? $page.archive : $page.unarchive)(page as Page)"
        title="La page ne sera pas supprimée, mais se trouvera dans les archives."
      >
        {{ page?.active ? "Archiver" : "Désarchiver" }}
      </v-btn>
    </v-row>
    <v-row class="my-4">
      <v-card width="100%" v-if="page">
        <v-card-title class="text-center">{{ page.title }}</v-card-title>
        <v-card-text>
          <v-table>
            <thead>
              <tr>
                <th>Auteur</th>
                <th>Dernière édition</th>
                <th>Date de création</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <th>
                  {{ $user.getUser(page.author).value.username }}
                </th>
                <th>{{ moment(page.edited).fromNow() }}</th>
                <th>{{ moment(page.created).fromNow() }}</th>
              </tr>
            </tbody>
          </v-table>
        </v-card-text>
      </v-card>
    </v-row>
  </v-container>
  <v-container v-else>
    <v-row no-gutters>
      <div style="width: 100%">
        <div class="ce-block__content">
          <v-icon
            class="gutter"
            icon="mdi-pencil"
            @click="showSettings = !showSettings"
          />
          <h1
            class="ce-header"
            style="display: inline-block"
            contenteditable
            ref="titleElement"
            @blur="updateTitle"
            @paste="onPasteTitle"
            @keydown="onKeydownTitle"
          ></h1>
        </div>
      </div>
    </v-row>
    <v-row no-gutters>
      <Editor v-if="blocks" :blocks="blocks" />
    </v-row>
  </v-container>
</template>

<style scoped>
.gutter {
  margin-left: -20px;
  padding-bottom: 10px;
  padding-right: 20px;
}
</style>

<script lang="ts" setup>
import Editor from "@/components/Editor.vue";
import { Block, useBlockStore } from "$/block";
import { usePageStore, Page } from "$/page";
import { computed, onMounted, onUnmounted, ref, toRef, watch } from "vue";
import { useRoute } from "vue-router";
import { useToast } from "vue-toastification";
import NotFound from "../components/NotFound.vue";
import { isRefNotUndefined } from "../composables/ref_undefined";
import moment from "moment";
import { useUserStore } from "@/stores/user";

const toast = useToast();
const $page = usePageStore();
const $block = useBlockStore();
const $user = useUserStore();
const route = useRoute();
const params = computed(() => route.params as { id: string; title?: string });

const page = toRef($page, "current");
const blocks = ref<Block[]>();
const error = ref<string>();
const notfound = ref(false);
const showSettings = ref(false);
const titleElement = ref<HTMLElement>();

function updateTitle() {
  if (
    !isRefNotUndefined(page) ||
    page.value.title === titleElement.value!.innerText
  )
    return;

  $page.changeTitle(page, titleElement.value!.innerText);
}
function onPasteTitle(evt: ClipboardEvent) {
  evt.preventDefault();
  const text = evt.clipboardData
    ?.getData("text/plain")
    .replaceAll(/[\n\r]/g, "");
  const selection = window.getSelection();

  if (text && selection?.rangeCount) {
    selection.deleteFromDocument();
    const range = selection.getRangeAt(0);
    range.insertNode(document.createTextNode(text));
    range.collapse();
  }
}
function onKeydownTitle(evt: KeyboardEvent) {
  if (evt.key == "Enter") {
    evt.preventDefault();
    titleElement.value!.blur();
  }
}

watch(error, (value) => {
  if (value) toast.error(value);
});

watch(page, (value) => {
  if (!value || value.title === titleElement.value?.innerText) return;
  titleElement.value!.innerText = value.title;
});

async function fetchPage() {
  const id = parseInt(params.value.id);

  if (!(notfound.value = isNaN(id))) {
    await $page.get(id, page, error);
    blocks.value = await $block.list_blocks();
  }
}

watch(params, (val, old) => {
  if (!val.id || val.id === old.id) return;
  showSettings.value = false;
  fetchPage();
});
onMounted(fetchPage);
onUnmounted(() => {
  console.log("unmounting");
  $page.current = undefined;
});
</script>
