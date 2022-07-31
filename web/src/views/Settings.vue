<template>
  <v-container>
    <v-row>
      <v-col>
        Thème
        <v-btn-toggle
          v-model="themeStore.theme"
          mandatory
          divided
          color="primary"
        >
          <v-btn value="dark" prepend-icon="mdi-moon-waning-crescent">
            Sombre
          </v-btn>
          <v-btn value="system" prepend-icon="mdi-theme-light-dark">
            Système
          </v-btn>
          <v-btn value="light" prepend-icon="mdi-white-balance-sunny">
            Clair
          </v-btn>
        </v-btn-toggle>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-btn
          color="primary"
          :disabled="userStore.user?.has2fa"
          @click="openModal('enable')"
        >
          Enable 2FA
        </v-btn>
        <v-btn
          color="primary"
          :disabled="!userStore.user?.has2fa"
          @click="openModal('disable')"
        >
          Disable 2FA
        </v-btn>
        <v-dialog v-model="dialog2fa">
          <v-card>
            <v-card-title class="text-center text-capitalize"
              >{{ dialogAction }} 2FA</v-card-title
            >
            <v-card-text>
              <v-alert
                v-if="new2faError || enable2faError || disable2faError"
                type="error"
                variant="outlined"
                icon="mdi-cloud-alert"
                :text="new2faError || enable2faError || disable2faError"
              />
              <v-container v-if="dialogAction == 'enable'">
                <v-row justify="center" no-gutters>
                  Scan the image below with the two-factor authentification app
                  on your phone.
                  <a href="#" @click.prevent="showURI = !showURI">
                    If you can't use a QR code, enter this text code instead
                  </a>
                  .
                </v-row>
                <v-row v-if="showURI" justify="center" no-gutters>
                  {{ new2fa?.uri }}
                </v-row>
                <v-row justify="center" class="ma-6" no-gutters>
                  <qrcode v-if="new2fa" :value="new2fa.uri" />
                  <v-progress-circular v-else indeterminate />
                </v-row>
                <v-row justify="center" no-gutters>
                  <div class="font-weight-bold">
                    Enter the six-digit code from the application.
                  </div>
                  <div>
                    After scanning the QR code image, the app will display a
                    six-digit code that you can enter below.
                  </div>
                </v-row>
              </v-container>
              <v-container v-else>
                <v-row justify="center" no-gutters>
                  To disable the two-factor authentification, enter the
                  six-digit code from the 2FA application on your phone.
                </v-row>
              </v-container>
              <v-otp-input
                ref="otpInput"
                class="justify-center"
                input-classes="otp-input"
                input-type="tel"
                separator=""
                :num-inputs="6"
                should-auto-focus
                @on-complete=""
              />
            </v-card-text>
            <v-card-actions>
              <v-row justify="space-around">
                <v-btn
                  :color="dialogAction == 'enable' ? 'error' : 'success'"
                  @click="dialog2fa = false"
                >
                  Cancel
                </v-btn>
                <v-btn
                  :color="dialogAction == 'enable' ? 'success' : 'error'"
                  @click="dialogAction == 'enable' ? enable2FA() : disable2FA()"
                >
                  {{ dialogAction }}
                </v-btn>
              </v-row>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-btn
          color="red-lighten-1"
          append-icon="mdi-exit-to-app"
          @click="logout()"
        >
          Se déconnecter
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import { useThemeStore } from "../stores/theme";
import { logout as logoutInit } from "../composables/api/auth/logout";
import Qrcode from "../components/Qrcode.vue";
import VOtpInput from "vue3-otp-input";
import { ref } from "vue";
import {
  request2FA as request2FAInit,
  enable2FA as enable2FAInit,
  disable2FA as disable2FAInit,
} from "../composables/api/auth/2fa";
import { useStore } from "@/stores/user";

const dialog2fa = ref(false);
const showURI = ref(false);
const dialogAction = ref<"enable" | "disable">();
const otpInput = ref<{ otp: string[] } | null>(null);
const themeStore = useThemeStore();
const userStore = useStore();
const { load: logout } = logoutInit();

const { data: new2fa, error: new2faError, load: request2FA } = request2FAInit();
const { error: enable2faError, load: _enable2FA } = enable2FAInit();
const { error: disable2faError, load: _disable2FA } = disable2FAInit();

async function enable2FA() {
  const otp = otpInput.value?.otp.join("");
  if (otp?.length == 6) {
    await _enable2FA({ code: otp });

    if (!enable2faError.value) {
      dialog2fa.value = false;
      userStore.reload();
    }
  } else {
    enable2faError.value = "Code invalide";
  }
}

async function disable2FA() {
  const otp = otpInput.value?.otp.join("");
  if (otp?.length == 6) {
    await _disable2FA({ code: otp });

    if (!disable2faError.value) {
      dialog2fa.value = false;
      userStore.reload();
    }
  } else {
    disable2faError.value = "Code invalide";
  }
}

function openModal(action: "enable" | "disable") {
  if (action == "enable") {
    request2FA();
  }
  dialogAction.value = action;
  dialog2fa.value = true;
}
</script>
