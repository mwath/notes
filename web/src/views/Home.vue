<template>
  <v-container>
    <h1 class="text-center">Pages</h1>
    <hr />
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
          v-for="page in $page.pages"
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

<script setup lang="ts">
import { getPageUrl, usePageStore } from "@/stores/page";
import { useUserStore } from "@/stores/user";
import moment from "moment";

const $page = usePageStore();
const $user = useUserStore();
</script>

<style scoped lang="scss"></style>
