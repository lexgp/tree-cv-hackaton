<script setup lang="ts">

import { useApi } from '@/composables/useApi';
import { ref } from "vue";

const $api = useApi()
const $router = useRouter()

const isLoading = ref(false)
const districtAreas = ref<any[] | null>(null)

const loadData = async () => {
  isLoading.value = true

  await $api.get('/areas/')
    .then((response) => {
      districtAreas.value = response.data
    })

  isLoading.value = false
}

onMounted(() => loadData())

</script>


<template>
  <v-container class="pa-4" style="max-width: 480px">
    <VRow class="">

      <VCol cols="12" class="mt-4">
        <RouterLink to="/" style="margin-left: -10px;">
          <IconBtn icon="ri-arrow-left-line" />
          К списку исследований
        </RouterLink>

        <!-- <VBtn variant="text" size="small" prepend-icon="ri-arrow-left-line" to="/">К списку исследований</VBtn> -->
        <h2 class="text-h4 mb-3">
          <!-- <IconBtn icon="ri-arrow-left-line" class="mr-1" /> -->
          Мои участки и отчёты
        </h2>
        <em>Вы можете просмотрить обобщённую статистику по обследуемым участкам.</em>
      </VCol>

      <VCol v-for="area in districtAreas" cols="12">
        <VAlert border="start" border-color="success" style="box-shadow: 0px 4px 4px #ccc;">
          <div class="v-alert-title">
            <RouterLink :to="'/areas/' + area.id">
              {{ area.title }}
            </RouterLink>
          </div>
          <ul>
            <li>Последнее обследование: -</li>
            <li>Количество деревьев: -</li>
          </ul>
        </VAlert>
      </VCol>


    </VRow>
  </v-container>
</template>
