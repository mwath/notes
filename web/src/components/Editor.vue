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
import DragDrop from "editorjs-drag-drop";
import Undo from "editorjs-undo";
import EditorJS from "@editorjs/editorjs";
import { onMounted, onUnmounted, ref } from "vue";

// const props = defineProps<{}>();
const holder = ref<HTMLElement>();
const editor = ref<EditorJS>();

onMounted(() => {
  console.log("mounted");
  editor.value?.destroy();
  editor.value = new EditorJS({
    holder: holder.value,
    defaultBlock: "paragraph",
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
    onReady: function () {
      console.log("ready");
      new Undo({ editor: editor.value });
      new DragDrop(editor.value);
    },
    onChange: function () {
      console.log("change");
    },
  });
});

onUnmounted(() => {
  console.log("unmounted");
  editor.value?.destroy();
});
</script>

<style lang="css" scoped>
.editor {
  width: 100%;
}
</style>

<style lang="css">
.tc-row > .tc-cell:first-child {
  border-left: 1px solid var(--color-border);
}
.tc-wrap,
.tc-popover {
  --color-border: rgba(var(--v-border-color), var(--v-border-opacity));
  --color-background: rgb(var(--v-theme-surface));
  --color-background-hover: rgba(
    var(--v-theme-surface-variant),
    calc(0.04 * var(--v-theme-overlay-multiplier))
  );
}
.tc-popover__item-icon {
  --color-background: transparent;
  --color-border: none;
}
.tc-popover__item-icon > svg > path {
  fill: currentColor;
}
.tc-toolbox__toggler > svg > rect {
  fill: transparent;
}
.tc-toolbox__toggler > svg > rect:hover {
  fill: var(--color-background);
}
.tc-toolbox {
  --toggler-dots-color: currentColor;
  --toggler-dots-color-hovered: currentColor;
}
.cdx-checklist__item-checkbox {
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
.ce-toolbar__plus:hover,
.cdx-settings-button:hover,
.ce-toolbar__settings-btn:hover {
  background-color: rgba(
    var(--v-theme-surface-variant),
    calc(0.04 * var(--v-theme-overlay-multiplier))
  );
}

.ce-block.ce-block--selected > div,
.ce-popover__item--focused {
  background-color: rgba(
    var(--v-theme-surface-variant),
    calc(0.12 * var(--v-theme-overlay-multiplier))
  ) !important;
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
.ce-block.ce-block--selected > div {
  border-radius: 3px;
}
</style>
