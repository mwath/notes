<template>
  <v-container class="fill-height">
    <v-row justify="center" align="center" class="fill-height">
      <v-col cols="12" md="8" lg="4">
        <v-form>
          <v-card
            title="Inscription"
            subtitle="Créez un compte pour accéder à l'application"
          >
            <v-divider />
            <v-card-text class="no-padding">
              <v-alert
                v-if="error"
                type="error"
                variant="outlined"
                icon="mdi-cloud-alert"
                :text="error"
              />
              <v-container>
                <v-row>
                  <v-col class="no-padding">
                    <v-text-field
                      v-model="email"
                      label="Email"
                      required
                      :rules="[rules.required, rules.email]"
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col class="no-padding">
                    <v-text-field
                      v-model="username"
                      label="Nom d'utilisateur"
                      required
                      :rules="[
                        rules.required,
                        rules.username.min,
                        rules.username.max,
                      ]"
                      counter
                      maxlength="20"
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col class="no-padding">
                    <v-text-field
                      v-model="password"
                      type="password"
                      label="Mot de passe"
                      required
                      :rules="[rules.required, rules.password]"
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col class="no-padding">
                    <v-text-field
                      type="password"
                      label="Confirmation du mot de passe"
                      required
                      :rules="[rules.required, rules.password_matches]"
                    />
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
            <v-card-actions>
              <v-spacer />
              <v-btn
                prepend-icon="mdi-lock"
                variant="outlined"
                :loading="loading"
                @click="register()"
              >
                S'inscrire
              </v-btn>
              <v-spacer />
            </v-card-actions>
          </v-card>
          <router-link to="/login" color="teal">Se connecter</router-link>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import { register as registerInit } from "../composables/api/auth/register";

const email = ref("");
const username = ref("");
const password = ref("");
const loading = ref(false);

const EMAIL_PATTERN =
  /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
const PASSWORD_PATTERN = /(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).*/;

const rules = {
  required: (value: string) => !!value || "Requis.",
  email: (value: string) => {
    return EMAIL_PATTERN.test(value) || "Email invalide.";
  },
  password: (value: string) => {
    return (
      PASSWORD_PATTERN.test(value) ||
      "Le mot de passe doit contenir au moins 8 caractères, une majuscule, une minuscule et un chiffre."
    );
  },
  password_matches: (value: string) =>
    value == password.value || "Le mot de passe ne correspond pas.",
  username: {
    min: (value: string) => value.length > 3 || "Min 3 caractères",
    max: (value: string) => value.length <= 20 || "Max 20 caractères",
  },
};

const { data, error, load } = registerInit();

function register() {
  loading.value = true;
  load({
    email: email.value,
    username: username.value,
    password: password.value,
  }).then(() => {
    loading.value = false;
    console.log(data.value);
  });
}
</script>

<style scoped lang="css">
.no-padding {
  padding-bottom: 0;
}
</style>
