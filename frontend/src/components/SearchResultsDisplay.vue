<script setup lang="ts">
import type { DogInfoResponse } from '@/types/DogInfoResponse'
import type { HttpError } from '@/types/Error'
import DogCard from './DogCard.vue'
import DogCardSkeleton from './DogCardSkeleton.vue'
import ErrorDisplay from './ErrorDisplay.vue'
import { computed } from 'vue'

const props = defineProps<{
  dogs: DogInfoResponse[]
  loading: boolean
  error: HttpError | undefined
  query: string
}>()

const formatNumOfMatches = computed(() => {
  return props.dogs.length === 1 ? '1 match' : `${props.dogs.length} matches`
})
</script>
<template>
  <!-- If loading, display loading skeleton -->
  <div v-if="loading" class="flex flex-col gap-4">
    <div class="flex flex-col gap-1">
      <h2 class="text-semibold">Searching for your perfect matches</h2>
      <p class="text-sm/6 text-surface-70 border-l-2 border-surface-30 pl-2">{{ query }}</p>
    </div>

    <div class="flex flex-col gap-6">
      <DogCardSkeleton v-for="(_, index) in [...Array(3)]" :key="index" :index="index" />
    </div>
  </div>

  <!-- else if error is not undefined -->
  <div v-else-if="error !== undefined">
    <ErrorDisplay :error="error" />
  </div>

  <!-- else if there are matching dogs -->
  <div v-else-if="dogs.length > 0" class="flex flex-col gap-4">
    <div class="flex flex-col gap-1">
      <h2 class="font-extrabold text-2xl brightness-85">Found {{ formatNumOfMatches }}</h2>
      <p class="text-sm/6 text-surface-70 border-l-2 border-surface-30 pl-2">{{ query }}</p>
    </div>
    <div class="flex flex-col gap-6">
      <DogCard v-for="(dog, index) in dogs" :key="index" :index="index" :dog="dog" />
    </div>
  </div>
</template>
<style scoped></style>
