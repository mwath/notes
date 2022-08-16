<template>
  <div ref="holder" class="editor" />
</template>

<script lang="ts" setup>
import Checklist from "@editorjs/checklist";
import Code from "@editorjs/code";
import Delimiter from "@editorjs/delimiter";
import Header from "@editorjs/header";
import InlineCode from "@editorjs/inline-code";
import Link from "@editorjs/link";
import Marker from "@editorjs/marker";
import NestedList from "@editorjs/nested-list";
import Paragraph from "@editorjs/paragraph";
import Quote from "@editorjs/quote";
import SimpleImage from "@editorjs/simple-image";
import Table from "@editorjs/table";
import Underline from "@editorjs/underline";
import Warning from "@editorjs/warning";
import { Block, useBlockStore } from "$/block";
import { usePageStore } from "$/page";
import DragDrop from "editorjs-drag-drop";
import Undo from "editorjs-undo";
import EditorJS, { BlockAPI, EditorConfig } from "@editorjs/editorjs";
import { onMounted, onUnmounted, ref, toRef, watch } from "vue";
import { useToast } from "vue-toastification";
import { BlockMutationType } from "@editorjs/editorjs/types/events/block/mutation-type";

// const props = defineProps<{}>();
const holder = ref<HTMLElement>();
const editor = ref<EditorJS>();
const page = toRef(usePageStore(), "current");
const toast = useToast();
const $block = useBlockStore();

type EditorChangeEvent = CustomEvent<{ target: BlockAPI }> & {
  type: BlockMutationType;
};

watch(page, async (value) => {
  if (page === undefined || editor.value === undefined) return;
  await editor.value.isReady;
  editor.value.clear();

  let blocks: Block[] = [];
  let id;

  const get_id = (arr: Block[]) => {
    return arr.length > 0 ? arr[arr.length - 1].id : undefined;
  };

  console.log(editor.value);
  do {
    id = get_id(blocks);
    blocks.push(...(await $block.list_blocks(id)));
  } while ((get_id(blocks) ?? id) != id);
  editor.value.render({ blocks });
});

onMounted(() => {
  editor.value?.destroy();
  editor.value = new EditorJS({
    holder: holder.value,
    placeholder: "paragraph",
    tools: {
      header: {
        class: Header,
        shortcut: "CMD+SHIFT+H",
      },
      list: {
        class: NestedList,
      },
      paragraph: {
        class: Paragraph,
        config: {
          placeholder: ".",
        },
      },
      quote: { class: Quote },
      warning: { class: Warning },
      image: { class: SimpleImage },
      checklist: { class: Checklist },
      code: { class: Code },
      delimiter: { class: Delimiter },
      inlinecode: { class: InlineCode },
      link: { class: Link },
      marker: { class: Marker },
      table: { class: Table },
      underline: { class: Underline },
    },
    onReady: () => {
      editor
        .value!.blocks.getBlockByIndex(0)
        ?.save()
        .then((block) => {
          // if (block)
          //   $block.create(block.id, { type: block.tool, data: block.data });
        });

      new Undo({ editor: editor.value });
      new DragDrop(editor.value);
    },
    onChange: async (api, evt: EditorChangeEvent) => {
      console.log("change", evt.type, evt.detail.target.id);
      const block = await evt.detail.target.save();
      if (block && page.value) {
        const type = block.tool;
        const data = block.data;

        switch (evt.type) {
          case BlockMutationType.Added:
            await $block.create(block.id, { type, data });
            break;
          case BlockMutationType.Changed:
            await $block.update(block.id, { type, data });
            break;
          case BlockMutationType.Removed:
            await $block.delete_block(block.id);
            break;
          case BlockMutationType.Moved:
            console.log(evt, block);
            break;
          default:
            toast.error(`Unknown block mutation: ${evt.type}`);
            break;
        }
      }
    },
  });
});

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
