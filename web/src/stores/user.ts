import { defineStore } from "pinia";
import { watch } from "vue";
import { me } from "../composables/api/users";
import router from "../router";
import { loadFromLocal, saveToLocal } from "./base";

function redirectToLogin() {
  const allowed_routes = ["/login", "/register"];
  if (!allowed_routes.includes(router.currentRoute.value.path))
    router.push("/login");
}

export const useUserStore = defineStore("user", () => {
  const { data: user, error, load } = me(loadFromLocal("user"));
  const reload = async () => {
    await load();

    if (error.value !== undefined) redirectToLogin();
  };

  reload();
  watch(user, (newval, oldval) => {
    if (newval == undefined) redirectToLogin();
    if (newval == oldval) return;

    saveToLocal("user", newval);
  });

  return { user, reload };
});
