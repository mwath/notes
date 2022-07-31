import { defineStore } from "pinia";
import { computed, ComputedRef, Ref, ref, watch } from "vue";
import { loadFromLocal, saveToLocal } from "./base";

type ColorScheme = "dark" | "light";
type SystemColorScheme = ColorScheme | "system";

export const useThemeStore = defineStore("theme", () => {
  const theme = ref<SystemColorScheme>(loadFromLocal("theme") || "system");
  const onSystemChange = (event: MediaQueryListEvent) => {
    systemScheme.value = event.matches ? "dark" : "light";
  };

  let media: MediaQueryList | undefined;
  if (matchMedia) {
    media = matchMedia("(prefers-color-scheme: dark)");
    if (theme.value == "system")
      media.addEventListener("change", onSystemChange);
  }

  const systemScheme = ref<ColorScheme>(media?.matches ? "dark" : "light");
  const scheme = computed<ColorScheme>(() =>
    theme.value === "system" ? systemScheme.value : theme.value
  );

  watch(theme, (newval, oldval) => {
    if (newval == oldval) return;
    if (media) {
      const cb = onSystemChange;
      if (oldval == "system") media.removeEventListener("change", cb);
      if (newval == "system") media.addEventListener("change", cb);
    }

    saveToLocal("theme", newval);
  });

  return { theme, scheme };
});
