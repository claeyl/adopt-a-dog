<template>
  <button type="button" class="suggestion-btn" @click="$emit('click', content)">
    {{ content }}
  </button>
</template>

<script setup lang="ts">
defineProps<{
  content: string
}>()

defineEmits<{
  click: [content: string]
}>()
</script>

<style scoped>
.suggestion-btn {
  background-color: var(--color-surface-200);
  border: 1px solid transparent;
  border-radius: 9999px;
  padding: 0.25rem 0.75rem;
  color: inherit;
  cursor: pointer;
  transition:
    background-color 100ms ease-in,
    border-color 100ms ease-in;
  font-size: 1rem;
}

.suggestion-btn:hover {
  background-color: var(--color-surface-100);
  border-color: var(--color-primary);
}
</style>
