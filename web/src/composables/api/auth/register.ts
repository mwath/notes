import requests from "../requests";
import { APIResponse } from "../base";
import { User } from "../users";
import { ref } from "vue";

interface AccountCreation {
  email: string;
  username: string;
  password: string;
}

export function register(): APIResponse<User, AccountCreation> {
  const data = ref<User>();
  const error = ref<string>();

  async function load(account: AccountCreation) {
    if (error.value !== undefined) error.value = undefined;
    if (data.value !== undefined) data.value = undefined;

    try {
      let result = await requests.post<User>("/users/create", account);
      data.value = result.data;
    } catch (err: any) {
      error.value = err.message;
    }
  }

  return { data, error, load };
}
