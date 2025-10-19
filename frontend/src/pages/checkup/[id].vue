<script setup lang="ts">
import { useApi } from '@/composables/useApi';
import DetailsCheckupView from '@/views/DetailsCheckupView.vue';
import UploadPhotosView from '@/views/UploadPhotosView.vue';
import { ref } from "vue";
import { useRoute } from 'vue-router';

const $route = useRoute()
const checkupId = $route.params.id.toString()
const isLoading = ref(false)
const checkupData = ref<any | null>(null)

interface Tree {
  id: number
  photo: string
  title: string
  status: string
  defects: string[]
  dryBranches?: string
}

const $api = useApi()

const loadData = () => {
  isLoading.value = true
  $api.get('/checkups/' + checkupId + '/')
    .then((response) => {
      console.log('API response:', response)
      checkupData.value = response.data
      isLoading.value = false
    })
    .catch((error) => {
      console.error('API request failed:', error)
      // Покажет даже если WebView блокирует
      alert(
        `API request failed\nMessage: ${error.message}\n` +
        `${error.response ? JSON.stringify(error.response.data) : 'No response'}`
      )
      isLoading.value = false
    })

}

onMounted(() => loadData())
</script>

<template>
  <v-container class="pa-4" style="max-width: 480px">
    <div class="mb-4">
      <div class="d-flex">
        <RouterLink to="/" style="margin-left: -10px;">
          <IconBtn icon="ri-arrow-left-line" />
          К списку обследований
        </RouterLink>
      </div>

      <h2 class="text-h4 mb-1">
        Участок: {{ checkupData?.area_detail?.title }}
      </h2>
      <em>Дата: {{ checkupData?.report_date }}</em>
    </div>

    <!-- {{ checkupData.condition_statistic }} -->
    <VProgressLinear v-if="isLoading" top indeterminate />

    <template v-if="checkupData">
      <UploadPhotosView v-if="checkupData.status == 'pending'" v-model:checkup-data="checkupData" />
      <DetailsCheckupView v-else :checkup-data="checkupData" />
    </template>

  </v-container>
</template>
