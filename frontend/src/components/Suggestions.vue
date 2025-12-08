<template>
  <div class="suggestions-container">
    <Suggestion
      v-for="(suggestion, i) in suggestions"
      :key="i"
      :content="suggestion"
      @click="$emit('suggestionClick', $event)"
    />
  </div>
</template>

<script setup lang="ts">
import Suggestion from './Suggestion.vue'

const suggestions = [
  'Good for first-time dog owners',
  'Compatible with cats',
  'Great with young children',
  'Okay being alone during work hours',
  'Prefers to be the only dog',
]

defineEmits<{
  suggestionClick: [content: string]
}>()
</script>

<style scoped>
.suggestions-container {
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  justify-content: center;
}
</style>
