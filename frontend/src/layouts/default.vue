<script lang="ts" setup>

import logoPhoto from '@images/logo.png';
import { ref } from "vue";
import { useRouter } from "vue-router";

const isLoading = ref(false)
const router = useRouter()
const drawer = ref(false)

router.beforeEach((to, from, next) => {
  isLoading.value = true
  next()
})

router.afterEach(() => {
  isLoading.value = false
})

</script>

<template>
  <v-app>
    <!-- Верхняя шапка -->
    <v-app-bar app color="primary" elevation="2">
      <v-container class="pa-0" style="max-width: 480px;">
        <v-row align="center" justify="space-between" no-gutters>

          <!-- Логотип и заголовок -->
          <v-row align="center" class="mx-2">
            <v-avatar size="40" class="mr-2">
              <v-img :src="logoPhoto" />
            </v-avatar>
            <h2 class="text-h4 m-0 ml-2 text-white">ЭкоКонтроль</h2>
          </v-row>

          <VSpacer />

          <!-- Кнопка "бутерброд" -->
          <v-btn class="mr-3" color="white" icon @click="drawer = !drawer">
            <v-icon>ri-menu-line</v-icon>
          </v-btn>
        </v-row>
      </v-container>
    </v-app-bar>

    <!-- Боковое меню -->
    <v-navigation-drawer v-model="drawer" app temporary>
      <v-list>
        <v-list-item link prepend-icon="ri-file-list-line" to="/home">
          <v-list-item-title>Мои обследования</v-list-item-title>
        </v-list-item>
        <v-list-item link prepend-icon="ri-map-pin-line" to="/areas">
          <v-list-item-title>Мои участки</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- Индикатор загрузки -->
    <v-progress-linear v-if="isLoading" indeterminate color="success" height="5" absolute top />

    <!-- Основной контент -->
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>
