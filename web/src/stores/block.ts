import requests from "@/composables/api/requests";
import router from "@/router";
import { defineStore } from "pinia";
import { reactive, Ref, watch } from "vue";
import { usePageStore } from "./page";

export type BlockCreation = Pick<Block, "type" | "data">;
export type BlockUpdate = Partial<BlockCreation>;

export interface Block {
  id: string;
  page_id: number;
  type: string;
  data: object;
  sequence: number;
}

export const useBlockStore = defineStore("block", () => {
  const $page = usePageStore();

  async function get(
    id: string,
    data: Ref<Block | undefined>,
    error?: Ref<string | undefined>
  ) {
    if ($page.current == undefined) return;
    if (error) error.value = undefined;
    data.value = undefined;

    try {
      let result = await requests.get<Block>(
        `/page/${$page.current.id}/block/${id}`
      );
      if (error) error.value = undefined;
      data.value = result.data;
    } catch (err: any) {
      if (data) data.value = undefined;
      if (error) error.value = err?.response?.data?.detail || err.message;
    }
  }

  async function create(
    block_id: string,
    block: BlockCreation,
    data?: Ref<Block | undefined>,
    error?: Ref<string | undefined>
  ) {
    if ($page.current === undefined) return;
    if (error) error.value = undefined;
    if (data) data.value = undefined;

    try {
      let result = await requests.post<Block>(
        `/page/${$page.current.id}/block/${block_id}`,
        block
      );
      if (error) error.value = undefined;
      if (data) data.value = result.data;
    } catch (err: any) {
      if (data) data.value = undefined;
      if (error) error.value = err?.response?.data?.detail || err.message;
    }
  }

  async function update(
    block_id: string,
    block: BlockUpdate,
    data?: Ref<Block | undefined>,
    error?: Ref<string | undefined>
  ) {
    if ($page.current === undefined) return;
    if (error) error.value = undefined;
    if (data) data.value = undefined;

    try {
      let result = await requests.put<Block>(
        `/page/${$page.current.id}/block/${block_id}`,
        block
      );
      if (error) error.value = undefined;
      if (data) data.value = result.data;
    } catch (err: any) {
      if (data) data.value = undefined;
      if (error) error.value = err?.response?.data?.detail || err.message;
    }
  }

  async function list_blocks(start?: string): Promise<Block[]> {
    if ($page.current == undefined) return [];
    const params = start ? { start } : undefined;

    let result = await requests.get<Block[]>(
      `/page/${$page.current.id}/blocks`,
      { params }
    );
    return result.data;
  }

  async function delete_block(blockId: string) {
    if ($page.current === undefined) return;
    const pageId = $page.current.id;

    try {
      let result = await requests.delete<Block>(
        `/page/${pageId}/block/${blockId}`
      );
    } catch (err: any) {}
  }

  async function swap(block1: string, block2: string | undefined) {
    if ($page.current === undefined || block2 === undefined) return;
    const pageId = $page.current.id;

    try {
      await requests.put(`/page/${pageId}/blocks/swap`, [block1, block2]);
    } catch (err: any) {}
  }

  async function move(blockId: string, before: string | undefined) {
    if ($page.current === undefined) return;
    const pageId = $page.current.id;

    try {
      await requests.put(`/page/${pageId}/block/${blockId}/move`, {
        dest: before,
      });
    } catch (err: any) {}
  }

  return {
    get,
    create,
    update,
    list_blocks,
    delete_block,
    move,
    swap,
  };
});
