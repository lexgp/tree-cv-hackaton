<script setup lang="ts">
import { useApi } from '@/composables/useApi';
import { ref } from "vue";

// import YandexMapTrees from '@/components/common/YandexMapTrees.vue';
import ConditionStatistic from '@/components/areas/ConditionStatistic.vue';
import pdfReportPdf from '@images/reports/report-example.pdf';

const $api = useApi()
const $route = useRoute()

const areaId = $route.params.id.toString()

const isLoading = ref(false)
const districtArea = ref<any | null>(null)

const loadData = async () => {
  isLoading.value = true

  await $api.get('/areas/' + areaId + '/')
    .then((response) => {
      districtArea.value = response.data
    })

  isLoading.value = false
}

onMounted(() => loadData())


interface Sector {
  id: string
  bounds: [number, number][]
}

interface Tree {
  id: number
  coords: [number, number]
  color?: string
  info?: string
}

const properties = [
  { name: 'Трещина', value: 2 },
  { name: 'Дупло', value: 1 },
  { name: 'Содранная кора', value: 3 },
  { name: 'Обнажены корни', value: 0 },
  { name: 'Грибы', value: 5 },
]

const sectors = [
  { id: 'A12', bounds: [[55.8010, 37.6705], [55.8005, 37.6735], [55.7985, 37.6735], [55.7983, 37.6710], [55.7990, 37.6703]] },
] as Sector[]

const trees = [
  { id: 1, coords: [55.799, 37.671], color: '#ff4444', info: 'Трещина' },
  { id: 2, coords: [55.7985, 37.6725], color: '#ffaa00', info: 'Дупло' },
] as Tree[]
</script>

<template>
  <v-container class="pa-4" style="max-width: 480px">
    <VRow>

      <VCol cols="12" class="mb-4">
        <div class="d-flex">
          <RouterLink to="/areas" style="margin-left: -10px;">
            <IconBtn icon="ri-arrow-left-line" />
            К списку участков
          </RouterLink>

          <VSpacer />

          <VBtn prepend-icon="ri-file-pdf-line" size="small" :href="pdfReportPdf" target="_blank" rel="noopener">Отчёт PDF
          </VBtn>
        </div>

        <h2 class="text-h4 mb-1">
          Участок: {{ districtArea?.title }}
        </h2>
        <em>Последнее обследование: {{ districtArea?.last_checkup_date }}</em>

        <VProgressLinear v-if="isLoading" top indeterminate />
      </VCol>

      <template v-if="districtArea">

        <ConditionStatistic :condition-statistic="districtArea.condition_statistic" />

        <VCol cols="12" class="mt-4">
          <h2 class="text-h5 mb-3">
            Статистика повреждений.
          </h2>

          <v-list density="compact" class="w-64">
            <v-list-item v-for="artifact in districtArea.artifacts_statistic" :key="artifact.title" class="py-1">
              <div class="d-flex justify-space-between items-center w-full text-sm">
                <span class="text-capitalize">{{ artifact.title }}</span>
                <div class="flex-1 border-b mx-2 opacity-30" style="border-bottom: dashed silver 1px; flex: 1"></div>
                <span>{{ artifact.count }}</span>
              </div>
            </v-list-item>
          </v-list>
        </VCol>

        <VCol cols="12" class="mt-4">
          <!-- <YandexMapTrees :sectors="sectors" :trees="trees" /> -->
          <div style="position:relative;overflow:hidden; width: 100%; height: 400px;"><a
              href="https://yandex.ru/maps/org/park_sokolniki/1607357284/?utm_medium=mapframe&utm_source=maps"
              style="color:#eee;font-size:12px;position:absolute;top:0px;">Парк Сокольники</a><a
              href="https://yandex.ru/maps/213/moscow/category/park/184106346/?utm_medium=mapframe&utm_source=maps"
              style="color:#eee;font-size:12px;position:absolute;top:14px;">Парк культуры и отдыха в Москве</a><a
              href="https://yandex.ru/maps/213/moscow/category/amusement_park/184106354/?utm_medium=mapframe&utm_source=maps"
              style="color:#eee;font-size:12px;position:absolute;top:28px;">Парк аттракционов в Москве</a><iframe
              src="https://yandex.ru/map-widget/v1/?l=sat%2Cskl&ll=37.672904%2C55.805778&mode=search&oid=1607357284&ol=biz&z=17"
              width="560" height="400" frameborder="1" allowfullscreen="true" style="position:relative;"></iframe></div>
        </VCol>
      </template>

    </VRow>
  </v-container>
</template>
