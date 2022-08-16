import Checklist from "@editorjs/checklist";
import Code from "@editorjs/code";
import Delimiter from "@editorjs/delimiter";
import { BlockAPI, EditorConfig } from "@editorjs/editorjs";
import { BlockMutationType } from "@editorjs/editorjs/types/events/block/mutation-type";
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

export const editor_defaults: EditorConfig = {
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
};

export interface IEditorEvent<
  K extends BlockMutationType = BlockMutationType,
  T = {}
> extends CustomEvent<T & { target: BlockAPI }> {
  type: K;
}

export type EditorAddedEvent = IEditorEvent<
  BlockMutationType.Added,
  { index: number }
>;
export type EditorChangedEvent = IEditorEvent<
  BlockMutationType.Changed,
  { index: number }
>;
export type EditorMovedEvent = IEditorEvent<
  BlockMutationType.Moved,
  { fromIndex: number; toIndex: number }
>;
export type EditorRemovedEvent = IEditorEvent<
  BlockMutationType.Removed,
  { index: number }
>;

export type EditorEvent =
  | EditorAddedEvent
  | EditorChangedEvent
  | EditorMovedEvent
  | EditorRemovedEvent;
