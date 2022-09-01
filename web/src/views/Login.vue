<template>
  <v-container class="fill-height">
    <v-row justify="center" align="center" class="fill-height">
      <v-col cols="12" md="8" lg="4">
        <v-form>
          <v-card title="Se connecter">
            <v-divider />
            <v-card-text class="no-padding">
              <v-alert
                v-if="error"
                type="error"
                variant="outlined"
                icon="mdi-cloud-alert"
                :text="error"
              />
              <v-container v-if="!requires_2fa">
                <v-row>
                  <v-col>
                    <v-text-field
                      v-model="username"
                      label="Email"
                      required
                      hide-details="auto"
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col>
                    <v-text-field
                      v-model="password"
                      type="password"
                      label="Password"
                      required
                      hide-details="auto"
                    />
                  </v-col>
                </v-row>
              </v-container>
              <v-container v-else>
                <v-otp-input
                  ref="otpInput"
                  class="justify-center"
                  input-classes="otp-input"
                  input-type="tel"
                  separator=""
                  :num-inputs="6"
                  should-auto-focus
                  @on-complete="login"
                />
              </v-container>
            </v-card-text>
            <v-card-actions>
              <v-spacer />
              <v-btn
                prepend-icon="mdi-lock"
                variant="outlined"
                :loading="loading"
                @click="login()"
              >
                Se connecter
              </v-btn>
              <v-spacer />
            </v-card-actions>
          </v-card>
          <router-link to="/register" color="teal">S'inscrire</router-link>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import { login as loginInit } from "../composables/api/auth/login";
import { login2fa } from "../composables/api/auth/2fa";
import VOtpInput from "vue3-otp-input";
import { useRouter } from "vue-router";
import { useUserStore } from "../stores/user";

interface VOtpInputDef {
  otp: string[];
  clearInput: () => void;
}

const router = useRouter();

const username = ref("");
const password = ref("");
const requires_2fa = ref(false);
const otpInput = ref<VOtpInputDef | null>(null);

const { data, error, load: _login } = loginInit();
const { load: _login2fa } = login2fa(data, error);
const loading = ref(false);

async function login() {
  loading.value = true;

  if (!requires_2fa.value) {
    await _login({ username: username.value, password: password.value });
    requires_2fa.value = !!data.value?.requires_2fa;
  } else {
    const otp = otpInput.value?.otp.join("");
    if (otp?.length != 6) {
      error.value = "Code invalide";
    } else {
      await _login2fa({ code: otp });
      requires_2fa.value = !data.value;
      otpInput.value?.clearInput();
    }
  }
  loading.value = false;

  if (!requires_2fa.value && !error.value) {
    useUserStore().reload();
    router.push("/");
  }
}
</script>

<style lang="css">
.no-padding {
  padding-bottom: 0;
}
</style>
