import requests from "@/composables/api/requests";
import { defineStore } from "pinia";
import { ref, Ref, watch } from "vue";
import { me, User } from "../composables/api/users";
import router from "../router";
import { loadFromLocal, saveToLocal } from "./base";

function redirectToLogin() {
  const allowed_routes = ["/login", "/register"];
  if (!allowed_routes.includes(router.currentRoute.value.path))
    router.push("/login");
}

export const useUserStore = defineStore("user", () => {
  const users: { [id: number]: Ref<User> } = {};
  const { data: user, error, load } = me(loadFromLocal("user"));
  const reload = async () => {
    await load();

    if (error.value !== undefined) redirectToLogin();
  };

  reload();
  watch(user, (newval, oldval) => {
    if (oldval !== undefined) delete users[oldval.id];
    if (newval == undefined) redirectToLogin();
    else users[newval.id] = user as Ref<User>;
    if (newval == oldval) return;

    saveToLocal("user", newval);
  });

  function getUser(id: number): Ref<User> {
    if (!(id in users)) {
      users[id] = ref({ id, email: "***@***.***", username: `User#${id}` });

      requests.get<User>(`/users/${id}`).then((response) => {
        users[response.data.id].value = response.data;
      });
    }
    return users[id];
  }

  return { user, reload, getUser };
});
