<template>
  <v-container class="fill-height text-center">
    <v-row justify="center" align="center" class="fill-height">
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>{{ counter }}</v-card-title>
          <v-card-text>
            <v-container>
              <v-row justify="center">
                <v-col>{{ message }}</v-col>
              </v-row>
              <v-row justify="center">
                <v-col>
                  <v-btn color="primary" prepend-icon="mdi-home" to="/">
                    Accueil
                  </v-btn>
                </v-col>
                <v-col>
                  <v-btn
                    variant="outlined"
                    color="secondary"
                    prepend-icon="mdi-arrow-left"
                    @click="router.back()"
                  >
                    Retour en arrière
                  </v-btn>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import { onMounted, onUnmounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

const router = useRouter();
const counter = ref(0);
const message = ref("Cette page n'existe pas.");

let interval: any = undefined;
onMounted(() => {
  interval = setInterval(() => {
    if (counter.value == 404) {
      return clearInterval(interval);
    }

    counter.value += Math.max(Math.ceil((404 - counter.value) / 10), 0);
  }, 20);
});
onUnmounted(() => {
  counter.value = 0;
  if (interval) clearInterval(interval);
});
</script>
