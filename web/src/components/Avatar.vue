<template>
  <v-avatar :color="color">
    {{ initials }}
  </v-avatar>
</template>

<script lang="ts" setup>
import { computed } from "vue";

const props = defineProps<{
  name: string;
  color?: string;
}>();

const initials = computed(() =>
  props.name
    .split(" ", 2)
    .map((str) => str.at(0))
    .filter((el) => el !== undefined)
    .join("")
    .toUpperCase()
);
</script>
