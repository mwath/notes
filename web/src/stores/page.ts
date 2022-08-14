import slugify from "@/composables/slugify";
import router from "@/router";
import { defineStore } from "pinia";
import { reactive, Ref, ref } from "vue";
import { RouteLocationRaw } from "vue-router";
import requests from "../composables/api/requests";

export interface Page {
  id: number;
  title: string;
  author: number;
  created: Date;
  edited: Date;
  active: boolean;
}

export interface PageCreation {
  title: string;
}

export function getPageUrl(page: Page): RouteLocationRaw {
  return {
    name: "Page",
    params: { id: page.id, title: slugify(page.title) },
  };
}

export const usePageStore = defineStore("page", () => {
  const current = ref<Page>();
  const pages = reactive<Page[]>([]);

  function getPageIndex(page: Page): number {
    return pages.map((p) => p.id).indexOf(page.id);
  }
  function updatePage(page: Page) {
    const index = getPageIndex(page);
    if (index > -1) pages[index] = page;
    if (current.value?.id == page.id) current.value = page;
  }

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
      if (data) current.value = data.value = result.data;
      pages.push(result.data);
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
    if (current.value?.id == id) {
      data.value = current.value;
      return;
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

  async function changeTitle(page: Ref<Page>, title: string) {
    if (title.length < 3) return;
    const data = { title };
    try {
      let result = await requests.put<Page>(`/page/${page.value.id}`, data);
      updatePage(result.data);
      router.replace(getPageUrl((page.value = result.data)));
    } catch (err: any) {}
  }

  async function list_pages() {
    try {
      let result = await requests.get<Page[]>("/pages");
      pages.splice(0, pages.length);
      pages.push(...result.data);
    } catch (err: any) {}
  }

  async function delete_page(page: Page): Promise<void>;
  async function delete_page(page: number): Promise<void>;
  async function delete_page(page: Page | number) {
    const pageId: number = typeof page === "number" ? page : page.id;
    try {
      let result = await requests.delete<Page>(`/page/${pageId}`);
      const index = getPageIndex(result.data);
      if (index > -1) pages.splice(index, 1);
    } catch (err: any) {}
  }

  async function archive(page: Page) {
    try {
      let result = await requests.put(`/page/${page.id}/archive`);
      updatePage(result.data);
    } catch (err: any) {}
  }

  async function unarchive(page: Page) {
    try {
      let result = await requests.put(`/page/${page.id}/unarchive`);
      updatePage(result.data);
    } catch (err: any) {}
  }

  return {
    current,
    create,
    get,
    pages,
    list_pages,
    delete_page,
    changeTitle,
    archive,
    unarchive,
  };
});
