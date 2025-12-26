<template>
  <div class="foo">
    <p class="typing-effect">{{ content }}</p>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  content: string
}>()
</script>

<style scoped>
.foo {
  width: max-content;
}
.typing-effect {
  width: 0;
  overflow: hidden;
  white-space: nowrap;
  border-right: 1px solid white;
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
