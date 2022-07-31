<template>
  <canvas ref="canvas"></canvas>
</template>

<script lang="ts" setup>
import { onMounted, ref, watch } from "vue";
import QRCode from "qrcode";

const props = defineProps<{ value: string }>();
const canvas = ref<HTMLCanvasElement>();

const render = () => {
  QRCode.toCanvas(canvas.value, props.value);
};

watch(props, render);
onMounted(render);
</script>
