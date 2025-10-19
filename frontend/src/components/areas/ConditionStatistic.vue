<script setup lang="ts">

defineProps({
  conditionStatistic: {
    type: Array as () => any[],
    required: true
  }
})

</script>

<template>
  <VCol cols="6" v-for="condition in conditionStatistic">
    <VAlert border="start" :border-color="condition.color" style="box-shadow: 0px 4px 4px #ccc;">
      <div class="d-flex">
        <h3 class="text-h3 v-alert-title" :class="'text-' + condition.color">
          {{ condition.count }} дер.
        </h3>
        <em class="ml-1 text-secondary" style="margin-top: -5px;">{{ condition.ratio }}%</em>
      </div>
      <ul>
        <li>{{ condition.title }}</li>
      </ul>
    </VAlert>
  </VCol>
</template>
