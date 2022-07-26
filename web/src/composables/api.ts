import { Ref } from "vue";

export interface APIResponse<T> {
  data: Ref<T | undefined>;
  error: Ref<string | undefined>;
  load: { (): Promise<void> };
}
