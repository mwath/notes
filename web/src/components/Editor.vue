<template>
  <div ref="holder" class="editor" />
</template>

<script lang="ts" setup>
import { Block, useBlockStore } from "$/block";
import { usePageStore } from "$/page";
import EditorJS, { API, BlockAPI } from "@editorjs/editorjs";
import { BlockMutationType } from "@editorjs/editorjs/types/events/block/mutation-type";
import DragDrop from "editorjs-drag-drop";
import Undo from "editorjs-undo";
import { editor_defaults, EditorEvent } from "@/composables/editor";
import { onMounted, onUnmounted, ref, toRef, watch } from "vue";
import { useToast } from "vue-toastification";
import { useGatewayStore } from "@/stores/gateway";

const props = defineProps<{ blocks: Block[]; readonly: boolean }>();
const holder = ref<HTMLElement>();
const editor = ref<EditorJS>();
const page = toRef(usePageStore(), "current");
const toast = useToast();
const $block = useBlockStore();
const $live = useGatewayStore();
const do_not_notify_for_change = new Set<string>();
const emit = defineEmits<{ (e: "reload"): void }>();

$live.on("block_added", (data) => {
  emit("reload");
});
$live.on("block_modified", async (data) => {
  if (!editor.value) return;
  const block = ref<Block>();
  const error = ref<string>();
  await $block.get(data.block_id, block, error);

  if (error.value) {
    toast.error(error.value);
  } else if (block.value) {
    do_not_notify_for_change.add(block.value.id);
    editor.value.blocks.update(block.value.id, block.value.data);
    do_not_notify_for_change.delete(block.value.id);
  }
});
$live.on("block_deleted", (data) => {
  if (!editor.value) return;
  do_not_notify_for_change.add(data.block_id);
  editor.value.blocks.delete(editor.value.blocks.getBlockIndex(data.block_id));
  do_not_notify_for_change.delete(data.block_id);
});
$live.on("block_moved", (data) => {
  if (!editor.value) return;
  do_not_notify_for_change.add(data.block_id);
  editor.value.blocks.move(
    data.dest,
    editor.value.blocks.getBlockIndex(data.block_id)
  );
  do_not_notify_for_change.delete(data.block_id);
});

watch(props, async () => {
  const codex = editor.value;
  if (codex === undefined) return;

  await codex.isReady;
  if (props.blocks.length === 0) codex.clear();
  else await codex.render({ blocks: props.blocks });
});

const onReady = () => {
  // Clear the editor if we have an empty editor:
  // https://github.com/codex-team/editor.js/issues/2010
  if (props.blocks.length === 0) editor.value?.clear();

  new Undo({ editor: editor.value });
  new DragDrop(editor.value);
};

const onChange = async (api: API, evt: EditorEvent) => {
  if (do_not_notify_for_change.has(evt.detail.target.id)) {
    return;
  }
  console.log("change", evt.type, evt.detail.target.id, evt.detail);
  const block = await evt.detail.target.save();
  if (block && page.value) {
    const type = block.tool;
    const data = block.data;

    switch (evt.type) {
      case BlockMutationType.Added:
        await $block.create(block.id, { type, data });
        await $live.send({
          id: "block_added",
          data: { block_id: block.id },
        });
        break;
      case BlockMutationType.Changed:
        await $block.update(block.id, { type, data });
        await $live.send({
          id: "block_modified",
          data: { block_id: block.id },
        });
        break;
      case BlockMutationType.Removed:
        await $block.delete_block(block.id);
        await $live.send({
          id: "block_deleted",
          data: { block_id: block.id },
        });
        break;
      case BlockMutationType.Moved:
        const { fromIndex: src, toIndex: dst } = evt.detail;
        const is_swap = Math.abs(src - dst) === 1;
        const index = is_swap ? src : dst + 1;
        const action = is_swap ? $block.swap : $block.move;
        const other = api.blocks.getBlockByIndex(index);

        await action(block.id, other?.id);
        await $live.send({
          id: "block_moved",
          data: { block_id: block.id, dest: dst },
        });
        break;
      default:
        toast.error(`Unknown block mutation: ${(evt as CustomEvent).type}`);
        break;
    }
  }
};

const loadEditor = () => {
  editor.value?.clear();
  editor.value = new EditorJS({
    holder: holder.value,
    readOnly: props.readonly,
    data: { blocks: props.blocks },
    ...editor_defaults,
    onReady,
    onChange,
  });
};

onMounted(loadEditor);
onUnmounted(() => {
  editor.value?.destroy();
});
</script>

<style lang="css" scoped>
.editor {
  width: 100%;
}
</style>

<style lang="scss">
$surface-hover-light: rgba(
  var(--v-theme-surface-variant),
  calc(0.04 * var(--v-theme-overlay-multiplier))
);
$surface-hover-darker: rgba(
  var(--v-theme-surface-variant),
  calc(0.12 * var(--v-theme-overlay-multiplier))
);

.tc-row > .tc-cell:first-child {
  border-left: 1px solid var(--color-border);
}
.tc-wrap,
.tc-popover {
  --color-border: rgba(var(--v-border-color), var(--v-border-opacity));
  --color-background: rgb(var(--v-theme-surface));
  --color-background-hover: $surface-hover-light;
}
.tc-popover__item-icon {
  --color-background: transparent;
  --color-border: none;

  > svg {
    > path {
      fill: currentColor;
    }
    > rect {
      fill: transparent;
    }
  }
}
.tc-toolbox__toggler > svg > rect {
  fill: transparent;
  &:hover {
    fill: $surface-hover-darker;
  }
}
.tc-toolbox {
  --toggler-dots-color: currentColor;
  --toggler-dots-color-hovered: currentColor;
}
.cdx-checklist__item-checkbox,
.ce-block.ce-block--selected > div {
  border-radius: 3px;
}
.cdx-checklist__item-checkbox,
.cdx-checklist__item--checked .cdx-checklist__item-checkbox,
.ce-popover,
.ce-inline-toolbar,
.ce-conversion-toolbar,
.ce-settings {
  background-color: rgb(var(--v-theme-surface));
  border-color: rgba(var(--v-theme-surface-variant), 0.2);
}
.cdx-settings-button,
.ce-settings__default-zone > div {
  color: currentColor;
}
.cdx-search-field {
  background-color: rgba(var(--v-theme-surface-variant), 0.2);
}
.ce-inline-tool:hover,
.ce-inline-toolbar__dropdown:hover,
.ce-conversion-tool:hover,
.ce-popover__item:hover,
.ce-settings__default-zone > div:hover,
.cdx-settings-button:hover {
  background-color: $surface-hover-light;
}
.ce-toolbar__plus:hover,
.ce-toolbar__settings-btn:hover {
  background-color: $surface-hover-darker;
}

.ce-block.ce-block--selected > div,
.ce-popover__item--focused {
  background-color: $surface-hover-darker !important;
  box-shadow: none;
}
.ce-popover__item-icon,
.ce-conversion-tool__icon {
  background-color: transparent;
  border: none;
}
.ce-toolbar__plus,
.ce-toolbar__settings-btn {
  color: currentColor;
  opacity: 0.8;
  background-color: transparent;
}

.cdx-marker {
  background-color: rgb(var(--v-theme-warning));
  color: rgb(var(--v-theme-on-warning));
}
</style>
