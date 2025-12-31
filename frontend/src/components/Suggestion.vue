<script setup lang="ts">
defineProps<{
  content: string
  color: string
}>()

defineEmits<{
  click: [content: string]
}>()
</script>

<template>
  <button
    type="button"
    class="font-medium text-balance rounded-full py-2 px-4 border-2 border-transparent border-transition brightness-transition"
    :style="{ backgroundColor: color }"
    @click="$emit('click', content)"
  >
    <span>{{ content }}</span>
  </button>
</template>

<style scoped>
.border-transition {
  transition: border-color 100ms ease-in;
}

.border-transition:hover {
  border-color: var(--clr-light);
}
</style>
