<template>
  <v-card v-if="annotation" class="rounded-lg overflow-hidden" elevation="2">
    <!-- Верхняя панель с двумя мини-фотками -->
    <v-row class="pa-2" dense>
      <v-col cols="6" v-for="(photo, index) in photos" :key="index">
        <v-img :src="baseUrl + photo" aspect-ratio="1" class="rounded-lg" @click="openDialog(photo)"
          style="cursor: pointer;" />
      </v-col>
    </v-row>

    <!-- Диалог для увеличенной фотки -->
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-img v-if="selectedPhoto" :src="baseUrl + selectedPhoto" aspect-ratio="1" cover />
        <v-card-actions>
          <v-spacer />
          <v-btn color="primary" @click="dialog = false">Закрыть</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Информация снизу -->
    <v-card-text>
      <template v-if="annotation.is_tree_finded">
        <h3 class="text-h5 text-capitalize font-weight-bold mb-2">
          {{ annotation.breed }}
        </h3>

        <div class="mb-2">
          <strong>Состояние:</strong> {{ annotation.condition }}
        </div>

        <div v-if="annotation.percentage_dried && annotation.percentage_dried > 0" class="mb-2">
          <strong>Сухие ветви:</strong> {{ annotation.percentage_dried }}%
        </div>

        <div v-if="annotation.artifacts && annotation.artifacts.length" class="mb-2">
          <strong>Дефекты:</strong>
          <ul class="pl-4">
            <li v-for="artifact in annotation.artifacts" :key="artifact">
              {{ artifact }}
            </li>
          </ul>
        </div>
      </template>

      <div v-if="tree.coords && tree.coords.length >= 2" class="mt-2">
        Координаты:
        {{ tree.coords[0].toFixed(4) }},
        {{ tree.coords[1].toFixed(4) }}
      </div>

      <div v-if="annotation.description" class="mt-2">
        <em>{{ annotation.description }}</em>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";

interface Annotation {
  annotated_photo?: string;
  is_tree_finded: boolean;
  breed?: string;
  condition?: string;
  percentage_dried?: number;
  artifacts?: string[];
  description?: string;
}

interface Tree {
  preview: string;
  annotation: Annotation;
  coords?: number[]
}

const props = defineProps<{
  tree: Tree;
  annotation: Annotation;
}>();

// Диалог
const dialog = ref(false)
const selectedPhoto = ref<string | null>(null)

// Функция открытия фотки
function openDialog(photo: string) {
  selectedPhoto.value = photo
  dialog.value = true
}

// Мини-фотки сверху: аннотированная и превью
const photos = computed(() => [
  props.tree.preview,
  props.annotation.annotated_photo || props.tree.preview,
])

const baseUrl = computed(() => {
  return import.meta.env.VITE_BASE_URL.replace('/tapi', '').replace('/api', '')
})

</script>

<style scoped>
/* Если хочешь, чтобы мини-фотки были одинакового размера и с округлыми углами */
.v-img {
  object-fit: cover;
}
</style>
