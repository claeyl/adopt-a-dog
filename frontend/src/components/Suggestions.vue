<script setup lang="ts">
import Suggestion from './Suggestion.vue'

const suggestions = [
  { suggestion: 'Good for first-time dog owners', color: 'var(--color-orange)' },
  { suggestion: 'Compatible with cats', color: 'var(--color-purple)' },
  { suggestion: 'Great with young children', color: 'var(--color-green)' },
  { suggestion: 'Prefers to be the only dog', color: 'var(--color-pink)' },
  { suggestion: 'Okay being alone during work hours', color: 'var(--color-darkblue)' },
]
defineEmits<{
  suggestionClick: [content: string]
}>()
</script>

<template>
  <div class="flex flex-wrap gap-4 justify-center">
    <Suggestion
      v-for="(suggestion, i) in suggestions"
      :key="i"
      :content="suggestion.suggestion"
      :color="suggestion.color"
      @click="$emit('suggestionClick', $event)"
    />
  </div>
</template>
