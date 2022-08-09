import { defineStore } from "pinia";
import { Ref, ref } from "vue";
import requests from "../composables/api/requests";

export interface Page {
  id: number;
  title: string;
  author: number;
  content: string;
  created: Date;
  edited: Date;
}

export interface PageCreation {
  title: string;
}

export const usePageStore = defineStore("page", () => {
  const draft = ref<Page>();

  async function create(
    page: PageCreation,
    data?: Ref<Page | undefined>,
    error?: Ref<string | undefined>,
    loading?: Ref<boolean>
  ) {
    if (loading) loading.value = true;
    if (error) error.value = undefined;
    if (data) data.value = undefined;

    try {
      let result = await requests.post<Page>("/page", page);
      if (error) error.value = undefined;
      if (data) draft.value = data.value = result.data;
    } catch (err: any) {
      if (data) data.value = undefined;
      if (error) error.value = err?.response?.data?.detail || err.message;
    }

    if (loading) loading.value = false;
  }

  async function get(
    id: number,
    data: Ref<Page | undefined>,
    error?: Ref<string | undefined>
  ) {
    if (draft.value?.id == id) {
      const page = draft.value;
      draft.value = undefined;
      return page;
    }

    if (error) error.value = undefined;
    data.value = undefined;

    try {
      let result = await requests.get<Page>(`/page/${id}`);
      if (error) error.value = undefined;
      data.value = result.data;
    } catch (err: any) {
      if (data) data.value = undefined;
      if (error) error.value = err?.response?.data?.detail || err.message;
    }
  }

  return { create, get };
});
