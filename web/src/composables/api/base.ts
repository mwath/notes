import { Ref } from "vue";

export interface APIResponse<T, K = void> {
  data: Ref<T | undefined>;
  error: Ref<string | undefined>;
  load: { (data: K): Promise<void> };
}
