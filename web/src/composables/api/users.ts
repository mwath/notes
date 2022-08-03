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
    try {
      let result = await requests.get<UserInfo>("/users/me");
      error.value = undefined;
      data.value = result.data;
    } catch (err: any) {
      data.value = undefined;
      error.value = err?.response?.data?.detail || err.message;
    }
  }

  return { data, error, load };
}
