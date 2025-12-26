<template>
  <div class="suggestions-container">
    <Suggestion
      v-for="(suggestion, i) in suggestions"
      :key="i"
      :content="suggestion.suggestion"
      :color="suggestion.color"
      @click="$emit('suggestionClick', $event)"
    />
  </div>
</template>

<script setup lang="ts">
import Suggestion from './Suggestion.vue'

const suggestions = [
  { suggestion: 'Good for first-time dog owners', color: 'var(--clr-orange)' },
  { suggestion: 'Compatible with cats', color: 'var(--clr-purple)' },
  { suggestion: 'Great with young children', color: 'var(--clr-green)' },
  { suggestion: 'Prefers to be the only dog', color: 'var(--clr-pink)' },
  { suggestion: 'Okay being alone during work hours', color: 'var(--clr-darkblue)' },
]
defineEmits<{
  suggestionClick: [content: string]
}>()
</script>

<style scoped>
.suggestions-container {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  justify-content: center;
}
</style>
