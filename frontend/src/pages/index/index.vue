<script setup lang="ts">
import { useApi } from '@/composables/useApi';
import emptyProfilePhoto from '@images/avatars/empty-profile-photo.png';

const $api = useApi()
const isLoading = ref(false)
const checkupsData = ref<any | null>(null)
const checkupsTotalCount = ref(0)
const itemsPerPage = ref(10)
const pageNumber = ref(1)

const loadData = () => {
  isLoading.value = true
  $api.get('/checkups/?page=' + pageNumber.value)
    .then((response) => {
      checkupsData.value = response.data.results
      checkupsTotalCount.value = parseInt(response.data.count)
      isLoading.value = false
    })
}

onMounted(() => loadData())
watch(() => pageNumber.value, () => loadData())

</script>

<template>
  <v-container class="pa-4" style="max-width: 480px">
    <VRow class="mt-2">
      <VCol cols="12">
        <VCard class="pa-4 rounded-lg">
          <VCardText class="text-center pt-6">
            <VAvatar :size="100" color="primary" variant="tonal">
              <VImg :src="emptyProfilePhoto" />
            </VAvatar>

            <h5 class="text-h5 mt-4">
              Иванов Петр Сергеевич
            </h5>

            <div class="mt-1">Северное лесничество</div>

            <VChip label color="primary" size="small" class="text-capitalize mt-2">
              Дендролог
            </VChip>
          </VCardText>
        </VCard>
      </VCol>

      <VCol cols="12">
        <VBtn class="ma-auto mb-2" block color="primary" rounded="xl" to="/checkup/new">
          Создать обследование
        </VBtn>
        <VBtn class="ma-auto mb-2" block color="success" rounded="xl" to="/areas">
          Мои участки и отчёты
        </VBtn>
      </VCol>

      <VCol cols="12" class="mt-4">
        <h2 class="text-h4 text-center">Мои обследования</h2>
      </VCol>

      <VCol v-for="checkup in checkupsData" cols="12">
        <VAlert border="start" border-color="primary" style="box-shadow: 0px 4px 4px #ccc;">
          <div class="v-alert-title">
            <RouterLink :to="'/checkup/' + checkup.id">
              {{ 'Участок: ' + checkup.area_detail?.title }}
            </RouterLink>
          </div>

          <ul>
            <li>Дата: {{ checkup.report_date }}</li>
            <li>Количество деревьев: {{ checkup.photos.length }}</li>
          </ul>

          <VChip color="primary" style="position: absolute; right: 10px; bottom: 11px; ">{{
            checkup.status }}</VChip>
        </VAlert>
      </VCol>

      <VCol cols="12" class="my-4">
        <VPagination v-model:page="pageNumber" :items-per-page="itemsPerPage" :total-items="checkupsTotalCount || 0" />
      </VCol>

    </VRow>
  </v-container>
</template>
