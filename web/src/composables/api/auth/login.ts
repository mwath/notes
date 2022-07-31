import requests from "../requests";
import { APIResponse } from "../base";
import { ref } from "vue";

interface OAuth2Password {
  username: string;
  password: string;
}

export interface TokenModel {
  requires_2fa: boolean;
}

export function login(): APIResponse<TokenModel, OAuth2Password> {
  const data = ref<TokenModel>();
  const error = ref<string>();

  async function load(creds: OAuth2Password) {
    if (error.value !== undefined) error.value = undefined;
    if (data.value !== undefined) data.value = undefined;

    try {
      let result = await requests.postForm<TokenModel>("/auth", creds);
      data.value = result.data;
    } catch (err: any) {
      error.value = err?.response?.data?.detail || err.message;
    }
  }

  return { data, error, load };
}
