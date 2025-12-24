<template>
  <div class="carousel" role="carousel">
    <button type="button" ariaLabel="previous" class="carousel__nav-btn prev" @click="onClickPrev">
      <i class="pi pi-chevron-left"></i>
    </button>
    <button type="button" ariaLabel="next" class="carousel__nav-btn next" @click="onClickNext">
      <i class="pi pi-chevron-right"></i>
    </button>

    <div class="carousel__track">
      <div v-for="(dog, index) in dogs" :key="dog.id" v-show="index === currentIndex">
        <DogCard :dog="dog" />
      </div>
    </div>

    <div class="carousel__nav-dots">
      <button
        v-for="(dog, idx) in dogs"
        :key="dog.id"
        :class="{ active: idx === currentIndex }"
        @click="currentIndex = idx"
        aria-label="Go to slide"
        class="carousel__dot"
      ></button>
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
  padding: 1.05rem;
  font-size: 1.25rem;
  aspect-ratio: 1 / 1;
  cursor: pointer;
  border-radius: 50%;

  background-color: var(--color-primary);
  transition: background-color ease 0.5s;

  position: absolute;
}

.carousel__nav-btn.prev {
  left: 0%;
  top: 50%;
}

.carousel__nav-btn.next {
  right: 0%;
  top: 50%;
}

.carousel__nav-btn:hover {
  background-color: var(--color-primary-dark);
}

.carousel__nav-dots {
  display: flex;
  justify-content: center;
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
