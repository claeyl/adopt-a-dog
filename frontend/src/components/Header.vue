<script setup lang="ts">
const emit = defineEmits<{
  (e: 'newSearch'): void
}>()
</script>

<template>
  <header class="fixed inset-0 z-10 p-3 h-15 border-b-1 border-surface-30 bg-surface-0">
    <button class="flex items-center gap-2 transition-brightness" @click="() => emit('newSearch')">
      <img src="../assets/logo.svg" alt="logo" class="w-9 aspect-square" />
    </button>
  </header>
</template>
