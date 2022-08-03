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
      if (data) data.value = result.data;
    } catch (err: any) {
      if (data) data.value = undefined;
      if (error) error.value = err?.response?.data?.detail || err.message;
    }

    if (loading) loading.value = false;
  }

  return { create };
});
