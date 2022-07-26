import { computed, ComputedRef, Ref, ref } from "vue";

type ColorScheme = "dark" | "light";
type SystemColorScheme = ColorScheme | "system";

class Theme {
  name: Ref<SystemColorScheme>;
  scheme: ComputedRef<ColorScheme>;
  systemTheme: Ref<ColorScheme>;
  media: MediaQueryList | undefined;

  constructor(name: SystemColorScheme) {
    if (matchMedia) {
      this.media = matchMedia("(prefers-color-scheme: dark)");
      if (name == "system")
        this.media.addEventListener("change", this.onSystemChange);
    }

    this.name = ref(name);
    this.systemTheme = ref(this.media?.matches ? "dark" : "light");
    this.scheme = computed(() =>
      this.name.value == "system" ? this.systemTheme.value : this.name.value
    );
  }

  changeTheme(name: SystemColorScheme) {
    if (this.name.value == name) return;
    if (this.media) {
      if (this.name.value == "system") {
        this.media.removeEventListener("change", this.onSystemChange);
      } else if (name == "system") {
        this.media.addEventListener("change", this.onSystemChange);
      }
    }

    this.name.value = name;
  }

  onSystemChange = (event: MediaQueryListEvent) => {
    this.systemTheme.value = event.matches ? "dark" : "light";
  };
}

export const theme = new Theme("system");
