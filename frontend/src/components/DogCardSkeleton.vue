<script setup lang="ts">
defineProps<{
  index: number
}>()
</script>

<template>
  <div
    class="bg-surface-10 border border-surface-20 rounded-xl transition-all duration-300 animate-fade-in-up card"
    :style="{ animationDelay: `${index * 100}ms` }"
  >
    <!-- Header -->
    <header class="border-b border-surface-30 flex justify-between items-center p-6">
      <div class="flex gap-2 items-center">
        <div class="w-12 h-12 rounded-xl animate-skeleton-pulse"></div>
        <div>
          <div class="w-30 h-6 mb-2 rounded-md animate-skeleton-pulse"></div>
          <div class="w-20 h-4 rounded-sm animate-skeleton-pulse"></div>
        </div>
      </div>
      <div class="rounded-full px-4 py-1 w-20 h-8 animate-skeleton-pulse"></div>
    </header>

    <!-- Body -->
    <div class="flex flex-col p-6 gap-6">
      <!-- Stats -->
      <div class="grid grid-cols-2 gap-2 sm:grid-cols-4">
        <div
          class="w-20 h-6 rounded-md animate-skeleton-pulse"
          v-for="(_, index) in [...Array(4)]"
          :key="index"
        ></div>
      </div>

      <!-- Tags -->
      <div class="flex flex-wrap gap-2">
        <div
          class="py-1 px-4 rounded-full w-30 h-7 animate-skeleton-pulse"
          v-for="(_, index) in [...Array(4)]"
          :key="index"
        ></div>
      </div>

      <!-- Description -->
      <div class="space-y-4">
        <div class="h-5 w-full rounded-md animate-skeleton-pulse"></div>
        <div class="h-5 w-full rounded-md animate-skeleton-pulse"></div>
        <div class="h-5 w-full rounded-md animate-skeleton-pulse"></div>
        <div class="h-5 w-3/4 rounded-md animate-skeleton-pulse"></div>
      </div>

      <!-- Generated Explanation -->
      <div className="p-4 rounded-xl bg-surface-20/30 space-y-4">
        <div className="h-5 w-50 mb-6 rounded-md animate-skeleton-pulse"></div>
        <div className="h-5 w-full rounded-md animate-skeleton-pulse"></div>
        <div className="h-5 w-full rounded-md animate-skeleton-pulse"></div>
        <div className="h-5 w-5/6 rounded-md animate-skeleton-pulse"></div>
      </div>

      <!-- CTA -->
      <div class="w-full h-10 rounded-xl animate-skeleton-pulse"></div>
    </div>
  </div>
</template>

<style scoped>
@keyframes skeleton-pulse {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

.animate-skeleton-pulse {
  background: linear-gradient(
    90deg,
    var(--color-surface-20) 0%,
    var(--color-surface-30) 50%,
    var(--color-surface-20) 100%
  );
  background-size: 200% 100%;
  animation: skeleton-pulse 1.5s ease-in-out infinite;
}
</style>
