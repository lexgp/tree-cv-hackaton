<script setup lang="ts">

import ConditionStatistic from '@/components/areas/ConditionStatistic.vue';
import AnnotationItem from '@/views/AnnotationItem.vue';

const props = defineProps({
  checkupData: {
    type: Object as () => any,
    required: true
  }
})

</script>

<template>
  <VRow>
    <ConditionStatistic :condition-statistic="checkupData.condition_statistic" />
  </VRow>

  <v-divider />

  <div class="mt-4 text-center">
    <span class="text-subtitle-1 font-weight-medium text-medium-emphasis">
      Обследование <strong>{{ checkupData.photos.length }} деревьев</strong> завершено
    </span>
  </div>

  <!-- Список деревьев -->
  <div v-for="tree in checkupData.photos" :key="tree.id" class="mb-6">
    <AnnotationItem v-if="tree.annotation" :tree="tree" :annotation="tree.annotation" />
  </div>
</template>
