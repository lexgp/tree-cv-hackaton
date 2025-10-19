<script setup lang="ts">
import type { PropType } from 'vue';
import { YandexMap } from 'vue-yandex-maps';

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

const props = defineProps({
  sectors: { type: Array as PropType<Sector[]>, default: () => [] },
  trees: { type: Array as PropType<Tree[]>, default: () => [] }
})
</script>

<template>
  <v-card class="rounded-lg overflow-hidden" elevation="2">
    <YandexMap :zoom="15" :coordinates="[55.798, 37.672]" style="width: 100%; height: 400px">
      <template #default="{ ymaps, map }">
        <component v-for="s in sectors" :is="ymaps.Polygon" :key="s.id" :geometry="[s.bounds]" :options="{
          fillColor: '#007aff33',
          strokeColor: '#007aff',
          strokeWidth: 2
        }" :map="map" />
        <component v-for="t in trees" :is="ymaps.Placemark" :key="t.id" :geometry="t.coords"
          :properties="{ balloonContent: t.info ?? 'Дерево' }"
          :options="{ preset: 'islands#circleDotIcon', iconColor: t.color ?? '#00cc44' }" :map="map" />
      </template>
    </YandexMap>
  </v-card>
</template>
