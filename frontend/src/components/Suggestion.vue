<template>
  <button
    type="button"
    class="suggestion-btn"
    :style="{ backgroundColor: color }"
    @click="$emit('click', content)"
  >
    <span>{{ content }}</span>
  </button>
</template>

<script setup lang="ts">
defineProps<{
  content: string
  color: string
}>()

defineEmits<{
  click: [content: string]
}>()
</script>

<style scoped>
.suggestion-btn {
  border: 2px solid transparent;
  border-radius: var(--radius-pill);
  padding: calc(0.5 * var(--space-base)) var(--space-2);

  color: inherit;
  font-weight: 500;
  font-size: var(--font-p-lg);
  text-wrap: balance;
  cursor: pointer;

  transition:
    border-color 100ms ease-in,
    filter 100ms ease-in;
}

.suggestion-btn:hover {
  filter: brightness(85%);
  border-color: var(--clr-light);
}
</style>
