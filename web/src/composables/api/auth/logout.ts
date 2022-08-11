import requests from "../requests";
import { APIResponse } from "../base";
import { ref } from "vue";
import { useUserStore } from "$/user";

export function logout(): APIResponse<boolean> {
  const data = ref<boolean>();
  const error = ref<string>();

  async function load() {
    if (error.value !== undefined) error.value = undefined;
    if (data.value !== undefined) data.value = undefined;

    try {
      let result = await requests.post<{ success: boolean }>("/auth/logout");
      data.value = result.data.success;
    } catch (err: any) {
      error.value = err?.response?.data?.detail || err.message;
    }

    if (data.value) {
      // Remove the user from the store
      useUserStore().user = undefined;
    }
  }

  return { data, error, load };
}
