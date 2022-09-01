<template>
  <v-container id="settings">
    <v-row justify="center">
      <v-divider />
      <h2>Thème</h2>
      <v-divider />
    </v-row>
    <v-row class="my-6" justify="center">
      <v-btn-toggle v-model="$theme.theme" mandatory divided color="primary">
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
    </v-row>
    <v-row class="mt-16 mb-4" justify="center">
      <v-divider />
      <h2>Paramètres du compte</h2>
      <v-divider />
    </v-row>
    <v-row justify="center">
      <h3>Double authentification</h3>
    </v-row>
    <v-row class="my-6" justify="center">
      <v-btn
        color="primary"
        @click="openModal($user.user?.has2fa ? 'disable' : 'enable')"
      >
        {{ $user.user?.has2fa ? "Désactiver" : "Activer" }}
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
                Scan the image below with the two-factor authentification app on
                your phone.
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
                To disable the two-factor authentification, enter the six-digit
                code from the 2FA application on your phone.
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
    </v-row>
    <v-row justify="center">
      <h3>Déconnexion</h3>
    </v-row>
    <v-row justify="center" class="my-6">
      <v-btn
        color="red-lighten-1"
        variant="plain"
        append-icon="mdi-exit-to-app"
        @click="logout()"
      >
        Se déconnecter
      </v-btn>
    </v-row>
    <v-row justify="center">
      <v-expansion-panels>
        <v-expansion-panel>
          <v-expansion-panel-title class="text-center">
            <h2>Plus d'actions</h2>
          </v-expansion-panel-title>
          <v-expansion-panel-text>
            <v-container>
              <v-row justify="center">
                <h3>Suppression du compte</h3>
              </v-row>
              <v-row justify="center" class="my-6">
                <v-alert type="error" variant="outlined" icon="mdi-alert">
                  Attention, cette action est irreversible ! Le compte sera
                  perdu à tout jamais et il sera impossible de le récupérer.
                  <i>Note: Vos pages ne seront pas supprimées.</i>
                </v-alert>
              </v-row>
              <v-row justify="center" class="my-6">
                <v-btn
                  color="red-lighten-1"
                  prepend-icon="mdi-trash-can"
                  @click="dialogDelete = true"
                >
                  Supprimer le compte
                </v-btn>
              </v-row>
            </v-container>
            <v-dialog v-model="dialogDelete">
              <v-card>
                <v-card-title class="text-center">
                  Suppression du compte
                </v-card-title>
                <v-card-text>
                  <v-alert
                    v-if="deleteError"
                    type="error"
                    variant="outlined"
                    icon="mdi-cloud-alert"
                    :text="deleteError"
                  />
                  <v-container>
                    <v-row justify="center" no-gutters>
                      Pour supprimer votre compte, veuillez récrire ci-dessous,
                      votre nom d'utilisateur: <b>{{ $user.user?.username }}</b
                      >.
                    </v-row>
                    <v-row class="my-6">
                      <v-text-field
                        v-model="username"
                        label="Nom d'utilisateur"
                        required
                        hide-details="auto"
                      />
                    </v-row>
                  </v-container>
                  <v-container v-if="$user.user?.has2fa">
                    <v-row class="mb-2">
                      Une confirmation à l'aide de votre code de double
                      authentification est requise pour la suppression de votre
                      compte.
                    </v-row>
                    <v-otp-input
                      :is-disabled="true"
                      ref="otpInput"
                      class="justify-center"
                      input-classes="otp-input"
                      input-type="tel"
                      separator=""
                      :num-inputs="6"
                      @on-complete=""
                    />
                  </v-container>
                </v-card-text>
                <v-card-actions>
                  <v-row justify="space-around">
                    <v-btn color="success" @click="dialogDelete = false">
                      Annuler
                    </v-btn>
                    <v-btn
                      color="error"
                      :disabled="
                        username != $user.user?.username ||
                        (!!otpInput && otpInput?.otp.join('')?.length != 6)
                      "
                      @click="deleteAccount()"
                    >
                      Supprimer
                    </v-btn>
                  </v-row>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-row>
    <v-row class="mt-16 mb-4" justify="center">
      <v-divider />
      <h2>Pages archivées</h2>
      <v-divider />
    </v-row>
    <v-table>
      <thead>
        <tr>
          <th>Auteur</th>
          <th>Titre</th>
          <th>Dernière édition</th>
          <th>Date de création</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="page in $page.pages.filter((page) => !page.active)"
          :key="page.id"
          @click="$router.push(getPageUrl(page))"
        >
          <th>
            {{ $user.getUser(page.author).value.username }}
          </th>
          <th>{{ page.title }}</th>
          <th>{{ moment(page.edited).fromNow() }}</th>
          <th>{{ moment(page.created).fromNow() }}</th>
        </tr>
      </tbody>
    </v-table>
  </v-container>
</template>

<style scoped>
#settings {
  max-width: 1000px;
  padding: 20px;
}
</style>

<script lang="ts" setup>
import { useUserStore } from "$/user";
import requests from "@/composables/api/requests";
import { getPageUrl, usePageStore } from "@/stores/page";
import moment from "moment";
import { ref } from "vue";
import VOtpInput from "vue3-otp-input";
import Qrcode from "../components/Qrcode.vue";
import {
  disable2FA as disable2FAInit,
  enable2FA as enable2FAInit,
  request2FA as request2FAInit,
} from "../composables/api/auth/2fa";
import { logout as logoutInit } from "../composables/api/auth/logout";
import { useThemeStore } from "../stores/theme";

const showURI = ref(false);
const dialog2fa = ref(false);
const dialogDelete = ref(false);
const deleteError = ref<string>();
const username = ref<string>("");
const dialogAction = ref<"enable" | "disable">();
const otpInput = ref<{ otp: string[] } | null>(null);
const $theme = useThemeStore();
const $user = useUserStore();
const $page = usePageStore();
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
      $user.reload();
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
      $user.reload();
    }
  } else {
    disable2faError.value = "Code invalide";
  }
}

async function deleteAccount() {
  let otp = undefined;
  if ($user.user?.has2fa) {
    const otp = otpInput.value?.otp.join("");
    if (otp?.length != 6) {
      deleteError.value = "Code invalide";
      return;
    }
  }

  try {
    await requests.delete("/users/me", { data: { code: otp } });
    dialogDelete.value = false;
    $user.reload();
  } catch (err: any) {
    deleteError.value = err?.response?.data?.detail || err.message;
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
