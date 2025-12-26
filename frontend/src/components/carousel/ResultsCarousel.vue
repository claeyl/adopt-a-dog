<template>
  <div class="carousel" role="carousel">
    <div class="carousel__track">
      <div v-for="(dog, index) in dogs" :key="dog.id" v-show="index === currentIndex">
        <DogCard :dog="dog" />
      </div>
    </div>

    <div class="carousel__nav-dots">
      <button type="button" ariaLabel="previous" class="carousel__nav-btn" @click="onClickPrev">
        <i class="pi pi-caret-left"></i>
      </button>

      <button
        v-for="(dog, idx) in dogs"
        :key="dog.id"
        :class="{ active: idx === currentIndex }"
        @click="currentIndex = idx"
        aria-label="Go to slide"
        class="carousel__dot"
      ></button>

      <button type="button" ariaLabel="next" class="carousel__nav-btn" @click="onClickNext">
        <i class="pi pi-caret-right"></i>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { DogResponse } from '@/types/DogResponse'
import DogCard from '../DogCard.vue'
import { ref } from 'vue'

const props = defineProps<{
  dogs: DogResponse[]
}>()

const currentIndex = ref(0)

const onClickPrev = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--
  }
}

const onClickNext = () => {
  if (currentIndex.value < props.dogs.length - 1) {
    currentIndex.value++
  }
}
</script>

<style scoped>
.carousel {
  position: relative;
}

/* .carousel__track {
  overflow: hidden;
} */

.carousel__nav-btn {
  border: none;
  cursor: pointer;
  border-radius: 50%;
  color: var(--color-primary);
  background-color: transparent;
  font-size: 1.25rem;
  outline: none;
}

.carousel__nav-btn:hover {
  color: var(--color-primary-dark);
}

.carousel__nav-dots {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1rem;
}

.carousel__dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: none;
  background: var(--color-surface-200);
  cursor: pointer;
}

.carousel__dot.active {
  background: white;
}
</style>
