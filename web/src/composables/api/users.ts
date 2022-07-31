import { ref } from "vue";
import { APIResponse } from "./base";
import requests from "./requests";

export interface UserBase {
  email: string;
  username: string;
}

export interface UserCreation extends UserBase {
  password: string;
}

export interface User extends UserBase {
  id: number;
}

export interface UserInfo extends User {
  has2fa: boolean;
}

export function me(user?: UserInfo): APIResponse<UserInfo> {
  const data = ref(user);
  const error = ref<string>();

  async function load() {
    if (error.value !== undefined) error.value = undefined;
    if (data.value !== undefined) data.value = undefined;

    try {
      let result = await requests.get<UserInfo>("/users/me");
      data.value = result.data;
    } catch (err: any) {
      error.value = err?.response?.data?.detail || err.message;
    }
  }

  return { data, error, load };
}
