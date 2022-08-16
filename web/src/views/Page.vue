<template>
  <NotFound v-if="notfound" />
  <v-container v-else>
    <v-row no-gutters>
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
    <v-row no-gutters>
      <div style="width: 100%">
        <div class="ce-block__content">
          <h1
            class="ce-header"
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

<script lang="ts" setup>
import Editor from "@/components/Editor.vue";
import { Block, useBlockStore } from "$/block";
import { usePageStore, Page } from "$/page";
import { computed, onMounted, onUnmounted, ref, toRef, watch } from "vue";
import { useRoute } from "vue-router";
import { useToast } from "vue-toastification";
import NotFound from "../components/NotFound.vue";
import { isRefNotUndefined } from "../composables/ref_undefined";

const toast = useToast();
const $page = usePageStore();
const $block = useBlockStore();
const route = useRoute();
const params = computed(() => route.params as { id: string; title?: string });

const page = toRef($page, "current");
const blocks = ref<Block[]>();
const error = ref<string>();
const notfound = ref(false);
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
  fetchPage();
});
onMounted(fetchPage);
onUnmounted(() => {
  console.log("unmounting");
  $page.current = undefined;
});
</script>
