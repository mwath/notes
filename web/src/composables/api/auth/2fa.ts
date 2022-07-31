import requests from "../requests";
import { APIResponse } from "../base";
import { Ref, ref } from "vue";
import { TokenModel } from "./login";

interface Code2FA {
  code: string;
}

interface New2FA {
  uri: string;
}

export function login2fa(
  data: Ref<TokenModel | undefined>,
  error: Ref<string | undefined>
): APIResponse<TokenModel, Code2FA> {
  async function load(code: Code2FA) {
    if (error.value !== undefined) error.value = undefined;
    if (data.value !== undefined) data.value = undefined;

    try {
      let result = await requests.post<TokenModel>("/auth/2fa/verify", code);
      data.value = result.data;
    } catch (err: any) {
      error.value = err?.response?.data?.detail || err.message;
    }
  }

  return { data, error, load };
}

export function request2FA(): APIResponse<New2FA> {
  const data = ref<New2FA>();
  const error = ref<string>();

  async function load() {
    if (error.value !== undefined) error.value = undefined;
    if (data.value !== undefined) data.value = undefined;

    try {
      let result = await requests.get<New2FA>("/auth/2fa/new");
      data.value = result.data;
    } catch (err: any) {
      error.value = err?.response?.data?.detail || err.message;
    }
  }

  return { data, error, load };
}

export function enable2FA(): APIResponse<void, Code2FA> {
  const error = ref<string>();

  async function load(code: Code2FA) {
    if (error.value !== undefined) error.value = undefined;

    try {
      await requests.post("/auth/2fa/enable", code);
    } catch (err: any) {
      error.value = err?.response?.data?.detail || err.message;
    }
  }

  return { data: ref<void>(), error, load };
}

export function disable2FA(): APIResponse<void, Code2FA> {
  const error = ref<string>();

  async function load(code: Code2FA) {
    if (error.value !== undefined) error.value = undefined;

    try {
      await requests.post("/auth/2fa/disable", code);
    } catch (err: any) {
      error.value = err?.response?.data?.detail || err.message;
    }
  }

  return { data: ref<void>(), error, load };
}
