<script setup lang="ts">
defineProps<{
  content: string
}>()
</script>

<template>
  <div class="w-max">
    <p class="w-0 overflow-hidden whitespace-nowrap border-r typing-effect">{{ content }}</p>
  </div>
</template>

<style scoped>
.typing-effect {
  animation: typing 2s forwards;
}

@keyframes typing {
  from {
    width: 0;
  }
  to {
    width: 100%;
    border-right: 0;
  }
}
</style>
