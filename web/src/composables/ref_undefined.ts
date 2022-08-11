import { Ref } from "vue";

export function isRefNotUndefined<T>(ref: Ref<T | undefined>): ref is Ref<T> {
  return ref.value !== undefined;
}
